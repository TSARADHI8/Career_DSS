"""
SQLAlchemy ORM Models.
These define the actual tables created in PostgreSQL.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """Stores registered student accounts."""
    __tablename__ = "users"

    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String(100), nullable=False)
    email          = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    profiles    = relationship("StudentProfile", back_populates="owner")
    predictions = relationship("Prediction", back_populates="owner")


class StudentProfile(Base):
    """Stores the academic profile submitted by each student."""
    __tablename__ = "student_profiles"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    skills      = Column(Text, nullable=False)
    backlogs    = Column(Integer, default=0)
    projects    = Column(Integer, default=0)
    internships = Column(Integer, default=0)
    higher_studies_interest = Column(Boolean, default=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    # Computed features (stored for reference)
    skill_count          = Column(Integer)
    experience_level     = Column(String(20))
    academic_risk        = Column(String(20))
    placement_readiness  = Column(String(20))

    owner       = relationship("User", back_populates="profiles")
    predictions = relationship("Prediction", back_populates="profile")


class Prediction(Base):
    """Stores ML + rule-based predictions for each profile."""
    __tablename__ = "predictions"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"), nullable=False)
    profile_id      = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)

    # ML model top recommendation
    ml_recommendation   = Column(String(50))
    ml_confidence       = Column(Float)

    # Rule-based ranked options (stored as JSON string)
    rule_scores         = Column(Text)

    # Final top recommendation shown to user
    top_recommendation  = Column(String(50))

    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    owner   = relationship("User", back_populates="predictions")
    profile = relationship("StudentProfile", back_populates="predictions")
