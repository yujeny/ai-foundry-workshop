from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey
from database import Base

class PatientDataTable(Base):
    __tablename__ = "patient_data"

    patient_id = Column(String, primary_key=True)
    cohort_id = Column(String, ForeignKey("patient_cohorts.cohort_id"))
    enrollment_date = Column(DateTime)
    demographics = Column(JSON)
    genetic_markers = Column(JSON)
    biomarkers = Column(JSON)
    adverse_events = Column(JSON)
    treatment_response = Column(Float, nullable=True)
    withdrawal_date = Column(DateTime, nullable=True)
    withdrawal_reason = Column(String, nullable=True)

class PatientCohortTable(Base):
    __tablename__ = "patient_cohorts"

    cohort_id = Column(String, primary_key=True)
    trial_id = Column(String, ForeignKey("clinical_trials.trial_id"))
    creation_date = Column(DateTime)
    stratification_factors = Column(JSON)
    inclusion_criteria = Column(JSON)
    biomarker_analysis = Column(JSON)
    efficacy_metrics = Column(JSON)
    safety_metrics = Column(JSON)
