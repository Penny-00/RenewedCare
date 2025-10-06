from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime

from .models import (
    PatientData, 
    FacilityData, 
    SymptomTriageRequest, 
    TriageResponse,
    HealthInsight
)
from .data_pipeline import DataPipeline
from .triage_model import SymptomTriageModel

# Initialize FastAPI app
app = FastAPI(
    title="RenewedCare API",
    description="AI-driven primary health care system for Africa",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
data_pipeline = DataPipeline()
triage_model = SymptomTriageModel()

# In-memory storage (for prototype)
patients_store = []
facilities_store = []


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Welcome to RenewedCare API",
        "version": "1.0.0",
        "endpoints": {
            "patients": "/patients",
            "facilities": "/facilities",
            "triage": "/triage",
            "insights": "/insights"
        }
    }


@app.post("/patients", response_model=dict)
async def add_patient(patient: PatientData):
    """Add new patient data"""
    patient_dict = patient.model_dump()
    patients_store.append(patient_dict)
    
    # Process data through pipeline
    df = data_pipeline.process_patient_data(patients_store)
    data_pipeline.save_processed_data(df, 'patients.csv')
    
    return {"message": "Patient added successfully", "patient_id": patient.patient_id}


@app.get("/patients", response_model=List[PatientData])
async def get_patients():
    """Get all patients"""
    return patients_store


@app.post("/facilities", response_model=dict)
async def add_facility(facility: FacilityData):
    """Add new facility data"""
    facility_dict = facility.model_dump()
    facilities_store.append(facility_dict)
    
    # Process data through pipeline
    df = data_pipeline.process_facility_data(facilities_store)
    data_pipeline.save_processed_data(df, 'facilities.csv')
    
    return {"message": "Facility added successfully", "facility_id": facility.facility_id}


@app.get("/facilities", response_model=List[FacilityData])
async def get_facilities():
    """Get all facilities"""
    return facilities_store


@app.post("/triage", response_model=TriageResponse)
async def perform_triage(request: SymptomTriageRequest):
    """Perform symptom-based triage"""
    try:
        result = triage_model.predict_triage(
            symptoms=request.symptoms,
            age=request.age,
            gender=request.gender,
            vital_signs=request.vital_signs
        )
        
        return TriageResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage error: {str(e)}")


@app.get("/insights/patients", response_model=dict)
async def get_patient_insights():
    """Get patient data insights and statistics"""
    stats = data_pipeline.get_patient_statistics()
    
    # Get health insights from AI model
    if patients_store:
        ai_insights = triage_model.get_health_insights(patients_store)
        stats.update(ai_insights)
    
    return stats


@app.get("/insights/facilities", response_model=dict)
async def get_facility_insights():
    """Get facility data insights and statistics"""
    stats = data_pipeline.get_facility_statistics()
    return stats


@app.get("/insights/health", response_model=List[HealthInsight])
async def get_health_insights():
    """Get overall health insights"""
    insights = []
    
    # Get patient statistics
    patient_stats = data_pipeline.get_patient_statistics()
    
    if patient_stats:
        insights.append(HealthInsight(
            metric_name="Total Patients",
            value=float(patient_stats.get('total_patients', 0)),
            trend="stable",
            timestamp=datetime.now()
        ))
        
        insights.append(HealthInsight(
            metric_name="Average Patient Age",
            value=float(patient_stats.get('avg_age', 0)),
            trend="stable",
            timestamp=datetime.now()
        ))
    
    # Get facility statistics
    facility_stats = data_pipeline.get_facility_statistics()
    
    if facility_stats:
        insights.append(HealthInsight(
            metric_name="Average Facility Utilization",
            value=float(facility_stats.get('avg_utilization', 0)),
            trend="increasing" if facility_stats.get('avg_utilization', 0) > 70 else "stable",
            timestamp=datetime.now()
        ))
    
    return insights


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "data_pipeline": "operational",
            "triage_model": "operational"
        }
    }
