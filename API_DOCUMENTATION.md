# RenewedCare API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### Health Check
Check the system health status.

**Request:**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-06T12:32:20.705816",
  "services": {
    "data_pipeline": "operational",
    "triage_model": "operational"
  }
}
```

---

### Patient Management

#### Add Patient
Add a new patient to the system.

**Request:**
```http
POST /patients
Content-Type: application/json

{
  "patient_id": "P001",
  "age": 35,
  "gender": "male",
  "location": "Lagos, Nigeria",
  "symptoms": ["fever", "headache", "chills"],
  "vital_signs": {
    "temperature": 39.2,
    "heart_rate": 98
  },
  "medical_history": []
}
```

**Response:**
```json
{
  "message": "Patient added successfully",
  "patient_id": "P001"
}
```

#### Get All Patients
Retrieve all patients from the system.

**Request:**
```http
GET /patients
```

**Response:**
```json
[
  {
    "patient_id": "P001",
    "age": 35,
    "gender": "male",
    "location": "Lagos, Nigeria",
    "symptoms": ["fever", "headache", "chills"],
    "vital_signs": {"temperature": 39.2},
    "medical_history": []
  }
]
```

---

### Facility Management

#### Add Facility
Add a new health facility to the system.

**Request:**
```http
POST /facilities
Content-Type: application/json

{
  "facility_id": "F001",
  "name": "Lagos General Hospital",
  "location": "Lagos, Nigeria",
  "type": "General Hospital",
  "capacity": 200,
  "available_beds": 45,
  "equipment": ["X-ray", "Ultrasound", "Laboratory"],
  "staff_count": 120
}
```

**Response:**
```json
{
  "message": "Facility added successfully",
  "facility_id": "F001"
}
```

#### Get All Facilities
Retrieve all facilities from the system.

**Request:**
```http
GET /facilities
```

---

### Symptom Triage

#### Perform Triage
Analyze symptoms and provide triage recommendations.

**Request:**
```http
POST /triage
Content-Type: application/json

{
  "symptoms": ["fever", "headache", "chills", "sweating"],
  "age": 35,
  "gender": "male",
  "vital_signs": {
    "temperature": 39.5,
    "blood_pressure_systolic": 130,
    "heart_rate": 95,
    "oxygen_saturation": 97
  }
}
```

**Response:**
```json
{
  "urgency_level": "high",
  "predicted_conditions": [
    {
      "condition": "Malaria",
      "confidence": 0.78,
      "matching_symptoms": ["fever", "chills", "headache", "sweating"]
    },
    {
      "condition": "Typhoid",
      "confidence": 0.20,
      "matching_symptoms": ["fever", "headache"]
    }
  ],
  "recommended_actions": [
    "Get immediate medical attention",
    "Blood test for confirmation",
    "Start antimalarial treatment"
  ],
  "confidence_score": 0.364
}
```

---

### Insights

#### Patient Insights
Get statistical insights from patient data.

**Request:**
```http
GET /insights/patients
```

**Response:**
```json
{
  "total_patients": 5,
  "avg_age": 37.4,
  "gender_distribution": {
    "male": 3,
    "female": 2
  },
  "location_distribution": {
    "Lagos, Nigeria": 1,
    "Nairobi, Kenya": 1
  },
  "top_symptoms": [
    {"symptom": "fever", "count": 2},
    {"symptom": "cough", "count": 1}
  ]
}
```

#### Facility Insights
Get statistical insights from facility data.

**Request:**
```http
GET /insights/facilities
```

**Response:**
```json
{
  "total_facilities": 3,
  "avg_capacity": 116.67,
  "avg_utilization": 72.5,
  "total_staff": 205
}
```

#### Health Insights
Get overall health metrics and trends.

**Request:**
```http
GET /insights/health
```

**Response:**
```json
[
  {
    "metric_name": "Total Patients",
    "value": 5.0,
    "trend": "stable",
    "timestamp": "2025-10-06T12:32:20.705816"
  },
  {
    "metric_name": "Average Facility Utilization",
    "value": 72.5,
    "trend": "increasing",
    "timestamp": "2025-10-06T12:32:20.705816"
  }
]
```

---

## Data Models

### PatientData
```python
{
  "patient_id": str,          # Unique patient identifier
  "age": int,                 # Age (1-120)
  "gender": str,              # "male", "female", or "other"
  "location": str,            # Patient location
  "symptoms": List[str],      # List of symptoms
  "vital_signs": dict,        # Optional vital signs
  "medical_history": List[str] # Optional medical history
}
```

### FacilityData
```python
{
  "facility_id": str,         # Unique facility identifier
  "name": str,                # Facility name
  "location": str,            # Facility location
  "type": str,                # Facility type
  "capacity": int,            # Total bed capacity
  "available_beds": int,      # Available beds
  "equipment": List[str],     # Available equipment
  "staff_count": int          # Number of staff
}
```

### Vital Signs (Optional)
```python
{
  "temperature": float,              # Body temperature in °C
  "blood_pressure_systolic": int,    # Systolic BP in mmHg
  "heart_rate": int,                 # Heart rate in bpm
  "oxygen_saturation": int           # O2 saturation in %
}
```

---

## Urgency Levels

The triage system classifies cases into four urgency levels:

- **Critical**: Requires immediate emergency intervention
- **High**: Needs urgent medical attention within hours
- **Medium**: Should be seen by a healthcare provider within a day
- **Low**: Can be managed with basic care and monitoring

Urgency is determined by:
1. Symptom matching with disease database
2. Age factors (children <5 and elderly >65 get escalated)
3. Vital signs assessment
4. Medical history considerations

---

## Error Responses

All endpoints may return the following error responses:

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Triage error: [error description]"
}
```

---

## Testing with cURL

### Test Triage
```bash
curl -X POST http://localhost:8000/triage \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["fever", "cough", "chest pain"],
    "age": 45,
    "gender": "female",
    "vital_signs": {
      "temperature": 38.5
    }
  }'
```

### Get Patient Insights
```bash
curl http://localhost:8000/insights/patients
```
