from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, Enum as SQLEnum
from database import Base
from models.clinical_trial import TrialPhase, TrialStatus

class ClinicalTrialTable(Base):
    __tablename__ = "clinical_trials"

    trial_id = Column(String, primary_key=True)
    drug_candidate_id = Column(String, ForeignKey("drug_candidates.id"))
    phase = Column(SQLEnum(TrialPhase))
    status = Column(SQLEnum(TrialStatus))
    start_date = Column(DateTime)
    estimated_completion_date = Column(DateTime)
    actual_completion_date = Column(DateTime, nullable=True)
    participant_count = Column(Integer)
    target_participant_count = Column(Integer)
    locations = Column(JSON)
    primary_endpoint = Column(String)
    secondary_endpoints = Column(JSON)
    inclusion_criteria = Column(JSON)
    exclusion_criteria = Column(JSON)
    adverse_events = Column(JSON)  # Store as JSON for flexibility
    interim_analyses = Column(JSON)
    real_time_metrics = Column(JSON)
