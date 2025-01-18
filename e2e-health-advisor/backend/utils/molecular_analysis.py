"""Utility functions for molecular analysis and patient response prediction."""

from sqlalchemy.orm import Session
from datetime import datetime
import asyncio
from models.tables import DrugCandidateTable
from models.drug_candidate import DrugCandidate

def analyze_genetic_compatibility(target_proteins: list, genetic_markers: list) -> float:
    """Analyze compatibility between drug target proteins and patient genetic markers."""
    # Simplified implementation - replace with actual ML model
    matching_markers = len(set(target_proteins).intersection(genetic_markers))
    total_targets = len(target_proteins)
    return matching_markers / total_targets if total_targets > 0 else 0.0

def analyze_biomarker_interaction(drug_biomarkers: dict, patient_biomarkers: dict) -> dict:
    """Analyze interaction between drug and patient biomarkers."""
    analysis = {
        "compatibility_score": 0.0,
        "risk_factors": [],
        "positive_indicators": []
    }
    
    # Analyze each biomarker interaction
    for marker, value in drug_biomarkers.items():
        if marker in patient_biomarkers:
            if abs(value - patient_biomarkers[marker]) < 0.2:
                analysis["positive_indicators"].append(marker)
            else:
                analysis["risk_factors"].append(marker)
    
    # Calculate overall compatibility
    total_markers = len(drug_biomarkers)
    positive_count = len(analysis["positive_indicators"])
    analysis["compatibility_score"] = positive_count / total_markers if total_markers > 0 else 0.0
    
    return analysis

def calculate_patient_response(
    base_efficacy: float,
    genetic_compatibility: float,
    biomarker_analysis: dict
) -> float:
    """Calculate predicted patient response based on multiple factors."""
    # Weighted combination of factors
    weights = {
        "base_efficacy": 0.4,
        "genetic_compatibility": 0.3,
        "biomarker_compatibility": 0.3
    }
    
    return (
        base_efficacy * weights["base_efficacy"] +
        genetic_compatibility * weights["genetic_compatibility"] +
        biomarker_analysis["compatibility_score"] * weights["biomarker_compatibility"]
    )

def identify_patient_risks(
    drug_side_effects: list,
    patient_demographics: dict,
    patient_biomarkers: dict
) -> list:
    """Identify potential risks based on patient characteristics."""
    risks = []
    
    # Age-related risks
    age = patient_demographics.get("age", 0)
    if age > 65:
        risks.append("Increased monitoring required due to age")
    
    # Biomarker-based risks
    for side_effect in drug_side_effects:
        if any(marker in patient_biomarkers for marker in ["liver_function", "kidney_function"]):
            risks.append(f"Monitor {side_effect} due to biomarker profile")
    
    return risks

def generate_patient_recommendations(
    therapeutic_area: str,
    patient_demographics: dict
) -> list:
    """Generate patient-specific treatment recommendations."""
    recommendations = [
        "Regular monitoring of key biomarkers",
        f"Specific considerations for {therapeutic_area} treatment"
    ]
    
    # Add demographic-specific recommendations
    age = patient_demographics.get("age", 0)
    if age > 65:
        recommendations.append("Adjusted dosing schedule for elderly patients")
    
    return recommendations

async def perform_detailed_analysis(molecule_ids: list, db: Session):
    """Background task for detailed molecular analysis."""
    for molecule_id in molecule_ids:
        try:
            # Simulate intensive computation
            await asyncio.sleep(1)
            
            # Update molecule analysis in database
            molecule = db.query(DrugCandidateTable).filter(
                DrugCandidateTable.id == molecule_id
            ).first()
            
            if molecule:
                # Update with detailed analysis results
                molecule.properties = {
                    **molecule.properties,
                    "detailed_analysis_completed": True,
                    "analysis_timestamp": datetime.now().isoformat()
                }
                db.commit()
                
        except Exception as e:
            print(f"Error in detailed analysis for molecule {molecule_id}: {str(e)}")
            continue

def analyze_single_molecule(molecule: DrugCandidate, db: Session) -> dict:
    """Analyze a single molecule for batch processing."""
    try:
        # Store the analyzed molecule
        db_molecule = DrugCandidateTable(
            id=molecule.id,
            molecule_type=molecule.molecule_type,
            molecular_weight=molecule.molecular_weight,
            therapeutic_area=molecule.therapeutic_area,
            predicted_efficacy=molecule.predicted_efficacy,
            predicted_safety=molecule.predicted_safety,
            creation_date=datetime.now(),
            target_proteins=molecule.target_proteins,
            side_effects=molecule.side_effects,
            development_stage=molecule.development_stage,
            ai_confidence=molecule.ai_confidence
        )
        db.add(db_molecule)
        db.commit()
        db.refresh(db_molecule)
        
        return {
            "molecule_id": molecule.id,
            "status": "success",
            "analysis": {
                "efficacy_score": molecule.predicted_efficacy,
                "safety_score": molecule.predicted_safety,
                "confidence": molecule.ai_confidence,
                "recommendations": [
                    f"Target proteins identified: {', '.join(molecule.target_proteins)}",
                    f"Development stage: {molecule.development_stage}",
                    f"Potential side effects: {', '.join(molecule.side_effects)}"
                ]
            }
        }
    except Exception as e:
        return {
            "molecule_id": molecule.id,
            "status": "error",
            "error": str(e)
        }
