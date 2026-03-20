from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    class Config:
        from_attributes = True

class ProfileCreate(BaseModel):
    skills: str
    backlogs: int
    projects: int
    internships: int
    higher_studies_interest: bool = False

class ProfileOut(BaseModel):
    id: int
    skills: str
    backlogs: int
    projects: int
    internships: int
    higher_studies_interest: bool
    skill_count: int
    experience_level: str
    academic_risk: str
    placement_readiness: str
    created_at: datetime
    class Config:
        from_attributes = True

class RankedOption(BaseModel):
    option: str
    score: int

class PredictionOut(BaseModel):
    id: int
    ml_recommendation: str
    ml_confidence: float
    top_recommendation: str
    rule_scores: List[RankedOption]
    created_at: datetime
    class Config:
        from_attributes = True
