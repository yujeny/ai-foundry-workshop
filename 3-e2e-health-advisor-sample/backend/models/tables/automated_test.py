from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Enum as SQLEnum
from database import Base
from models.automated_test import TestResult

class AutomatedTestTable(Base):
    __tablename__ = "automated_tests"

    test_id = Column(String, primary_key=True)
    drug_candidate_id = Column(String, ForeignKey("drug_candidates.id"))
    test_type = Column(String)
    start_time = Column(DateTime)
    completion_time = Column(DateTime, nullable=True)
    result = Column(SQLEnum(TestResult))
    parameters = Column(JSON)
    measurements = Column(JSON)
    ai_analysis = Column(JSON)
    safety_flags = Column(JSON)
