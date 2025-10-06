from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PatientData(BaseModel):
    """Patient information schema"""
    patient_id: str
    age: int = Field(gt=0, lt=120)
    gender: str = Field(pattern="^(male|female|other)$")
    location: str
    symptoms: List[str]
    vital_signs: Optional[dict] = None
    medical_history: Optional[List[str]] = None


class FacilityData(BaseModel):
    """Health facility information schema"""
    facility_id: str
    name: str
    location: str
    type: str
    capacity: int = Field(gt=0)
    available_beds: int = Field(ge=0)
    equipment: List[str]
    staff_count: int = Field(ge=0)


class SymptomTriageRequest(BaseModel):
    """Request for symptom triage"""
    symptoms: List[str]
    age: int = Field(gt=0, lt=120)
    gender: str
    vital_signs: Optional[dict] = None


class TriageResponse(BaseModel):
    """Response from triage system"""
    urgency_level: str
    predicted_conditions: List[dict]
    recommended_actions: List[str]
    confidence_score: float


class HealthInsight(BaseModel):
    """Health insights and analytics"""
    metric_name: str
    value: float
    trend: str
    timestamp: datetime
