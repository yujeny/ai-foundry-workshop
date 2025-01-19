from sqlalchemy import Column, String, Float, DateTime, JSON, Enum as SQLEnum
from database import Base
from models.drug_candidate import MoleculeType
import enum

class DrugCandidateTable(Base):
    __tablename__ = "drug_candidates"

    id = Column(String, primary_key=True)
    molecule_type = Column(SQLEnum(MoleculeType))
    molecular_weight = Column(Float)
    therapeutic_area = Column(String)
    predicted_efficacy = Column(Float)
    predicted_safety = Column(Float)
    creation_date = Column(DateTime)
    target_proteins = Column(JSON)
    side_effects = Column(JSON)
    development_stage = Column(String)
    ai_confidence = Column(Float)
    # Store additional molecular properties as JSON
    properties = Column(JSON)
