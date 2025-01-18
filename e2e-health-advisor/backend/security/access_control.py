"""Access control and authorization utilities."""

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from typing import Dict, List, Optional
import jwt
import time
import os
from datetime import datetime, timedelta

class AccessControl:
    def __init__(self, secret_key: str):
        """Initialize with secret key for JWT."""
        self.secret_key = secret_key
        self.api_key_header = APIKeyHeader(name="X-API-Key")
    
    def create_access_token(
        self,
        user_id: str,
        roles: List[str],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token with roles."""
        to_encode = {
            "sub": user_id,
            "roles": roles,
            "iat": datetime.utcnow()
        }
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        
        return jwt.encode(to_encode, self.secret_key, algorithm="HS256")
    
    def verify_token(self, token: str) -> Dict:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=["HS256"]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired"
            )
        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
    
    def check_role(self, token: str, required_role: str) -> bool:
        """Check if user has required role."""
        payload = self.verify_token(token)
        return required_role in payload.get("roles", [])
    
    async def get_current_user(
        self,
        api_key: str = Security(APIKeyHeader(name="X-API-Key"))
    ) -> Dict:
        """Validate API key and return user info."""
        try:
            payload = self.verify_token(api_key)
            return {
                "user_id": payload["sub"],
                "roles": payload["roles"]
            }
        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )
    
    def require_role(self, required_role: str):
        """Decorator to require specific role for endpoint."""
        async def role_checker(
            current_user: Dict = Security(lambda: self.get_current_user())
        ):
            if required_role not in current_user["roles"]:
                raise HTTPException(
                    status_code=403,
                    detail=f"Role {required_role} required"
                )
            return current_user
        return role_checker

class RoleBasedAccess:
    """Role-based access control for research data."""
    
    ROLES = {
        "admin": [
            "read:all",
            "write:all",
            "delete:all"
        ],
        "researcher": [
            "read:molecules",
            "read:trials",
            "write:molecules",
            "write:trials"
        ],
        "clinician": [
            "read:patients",
            "write:patients",
            "read:trials"
        ],
        "analyst": [
            "read:molecules",
            "read:trials",
            "read:analytics"
        ]
    }
    
    @staticmethod
    def has_permission(user_roles: List[str], required_permission: str) -> bool:
        """Check if user has required permission."""
        user_permissions = []
        for role in user_roles:
            user_permissions.extend(RoleBasedAccess.ROLES.get(role, []))
        
        # Check for direct permission or wildcard
        return (
            required_permission in user_permissions or
            "write:all" in user_permissions or
            (
                required_permission.startswith("read:") and
                "read:all" in user_permissions
            )
        )
    
    @staticmethod
    def get_user_permissions(roles: List[str]) -> List[str]:
        """Get all permissions for given roles."""
        permissions = set()
        for role in roles:
            permissions.update(RoleBasedAccess.ROLES.get(role, []))
        return list(permissions)

# Initialize global instances
jwt_secret = os.getenv("JWT_SECRET_KEY")
if not jwt_secret:
    raise ValueError("JWT_SECRET_KEY environment variable must be set")
access_control = AccessControl(jwt_secret)
role_based_access = RoleBasedAccess()
