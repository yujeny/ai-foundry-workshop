"""Data encryption and security utilities for handling sensitive research data."""

from cryptography.fernet import Fernet
from typing import Dict, Any, Union
import os
import json
import base64
import logging
from logging.handlers import RotatingFileHandler
import hashlib
import hmac

class DataEncryption:
    def __init__(self):
        """Initialize encryption with key from environment or generate new one."""
        key = os.getenv("ENCRYPTION_KEY")
        if not key:
            key = Fernet.generate_key()
            print("Warning: No encryption key found in environment. Generated new key.")
        elif isinstance(key, str):
            # Convert string key to bytes if needed
            key = key.encode('utf-8')
        self.fernet = Fernet(key)
    
    def encrypt_patient_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt sensitive patient information."""
        encrypted_data = data.copy()
        
        # Encrypt sensitive fields
        sensitive_fields = [
            "genetic_markers",
            "biomarkers",
            "demographics",
            "adverse_events"
        ]
        
        for field in sensitive_fields:
            if field in encrypted_data:
                # Convert to string and encrypt
                field_data = json.dumps(encrypted_data[field])
                encrypted_data[field] = self.fernet.encrypt(
                    field_data.encode()
                ).decode()
        
        return encrypted_data
    
    def decrypt_patient_data(self, encrypted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt patient information for authorized access."""
        decrypted_data = encrypted_data.copy()
        
        # Decrypt sensitive fields
        sensitive_fields = [
            "genetic_markers",
            "biomarkers",
            "demographics",
            "adverse_events"
        ]
        
        for field in sensitive_fields:
            if field in decrypted_data:
                # Decrypt and parse JSON
                decrypted_field = self.fernet.decrypt(
                    decrypted_data[field].encode()
                ).decode()
                decrypted_data[field] = json.loads(decrypted_field)
        
        return decrypted_data
    
    def encrypt_molecule_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt sensitive molecular research data."""
        encrypted_data = data.copy()
        
        # Encrypt proprietary research fields
        sensitive_fields = [
            "target_proteins",
            "mechanism_of_action",
            "development_timeline",
            "properties"
        ]
        
        for field in sensitive_fields:
            if field in encrypted_data:
                field_data = json.dumps(encrypted_data[field])
                encrypted_data[field] = self.fernet.encrypt(
                    field_data.encode()
                ).decode()
        
        return encrypted_data
    
    def decrypt_molecule_data(self, encrypted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt molecular data for authorized access."""
        decrypted_data = encrypted_data.copy()
        
        # Decrypt proprietary research fields
        sensitive_fields = [
            "target_proteins",
            "mechanism_of_action",
            "development_timeline",
            "properties"
        ]
        
        for field in sensitive_fields:
            if field in decrypted_data:
                decrypted_field = self.fernet.decrypt(
                    decrypted_data[field].encode()
                ).decode()
                decrypted_data[field] = json.loads(decrypted_field)
        
        return decrypted_data

class DataAuditing:
    def __init__(self, log_file: str = "data_access.log"):
        """Initialize auditing with rotating log file."""
        self.logger = logging.getLogger("data_audit")
        self.logger.setLevel(logging.INFO)
        
        handler = RotatingFileHandler(
            log_file,
            maxBytes=10000000,  # 10MB
            backupCount=5
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_access(
        self,
        user_id: str,
        data_type: str,
        action: str,
        resource_id: str,
        success: bool
    ):
        """Log data access attempts for audit trails."""
        self.logger.info(
            f"Access - User: {user_id}, Type: {data_type}, "
            f"Action: {action}, Resource: {resource_id}, "
            f"Success: {success}"
        )
    
    def log_modification(
        self,
        user_id: str,
        data_type: str,
        action: str,
        resource_id: str,
        changes: Dict[str, Any]
    ):
        """Log data modifications for audit trails."""
        self.logger.info(
            f"Modification - User: {user_id}, Type: {data_type}, "
            f"Action: {action}, Resource: {resource_id}, "
            f"Changes: {json.dumps(changes)}"
        )

class DataAnonymization:
    @staticmethod
    def anonymize_patient_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize patient data for research use."""
        anonymized = data.copy()
        
        # Remove direct identifiers
        identifiers = [
            "name",
            "address",
            "phone",
            "email",
            "ssn",
            "medical_record_number"
        ]
        for field in identifiers:
            anonymized.pop(field, None)
        
        # Hash patient ID
        if "patient_id" in anonymized:
            anonymized["patient_id"] = hashlib.sha256(
                anonymized["patient_id"].encode()
            ).hexdigest()
        
        # Generalize demographics
        if "demographics" in anonymized:
            demographics = anonymized["demographics"]
            if "age" in demographics:
                # Convert exact age to range
                age = demographics["age"]
                demographics["age_range"] = f"{(age // 5) * 5}-{((age // 5) * 5) + 4}"
                del demographics["age"]
            if "zip_code" in demographics:
                # Keep only first 3 digits
                demographics["zip_code"] = demographics["zip_code"][:3] + "XX"
        
        return anonymized
    
    @staticmethod
    def generate_research_id(original_id: str, study_id: str) -> str:
        """Generate research ID that can't be traced back to patient."""
        # Create HMAC using study_id as key
        h = hmac.new(
            study_id.encode(),
            original_id.encode(),
            hashlib.sha256
        )
        # Return first 8 characters of hex digest
        return h.hexdigest()[:8]

# Initialize global instances
data_encryption = DataEncryption()
data_auditing = DataAuditing()
data_anonymization = DataAnonymization()
