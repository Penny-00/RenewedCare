#!/usr/bin/env python3
"""
Test script to populate the system with sample data
"""
import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test API health endpoint"""
    print("Testing health check...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Health check: {response.json()}")
    return response.status_code == 200

def add_sample_patients():
    """Add sample patient data"""
    print("\nAdding sample patients...")
    
    patients = [
        {
            "patient_id": "P001",
            "age": 35,
            "gender": "male",
            "location": "Lagos, Nigeria",
            "symptoms": ["fever", "chills", "headache", "sweating"],
            "vital_signs": {"temperature": 39.2, "heart_rate": 98},
            "medical_history": []
        },
        {
            "patient_id": "P002",
            "age": 68,
            "gender": "female",
            "location": "Nairobi, Kenya",
            "symptoms": ["cough", "fever", "chest pain", "difficulty breathing"],
            "vital_signs": {"temperature": 38.8, "oxygen_saturation": 92},
            "medical_history": ["asthma"]
        },
        {
            "patient_id": "P003",
            "age": 25,
            "gender": "female",
            "location": "Accra, Ghana",
            "symptoms": ["runny nose", "sore throat", "mild fever"],
            "vital_signs": {"temperature": 37.8},
            "medical_history": []
        },
        {
            "patient_id": "P004",
            "age": 52,
            "gender": "male",
            "location": "Addis Ababa, Ethiopia",
            "symptoms": ["severe headache", "chest pain", "dizziness"],
            "vital_signs": {"blood_pressure_systolic": 185, "heart_rate": 110},
            "medical_history": ["hypertension"]
        },
        {
            "patient_id": "P005",
            "age": 7,
            "gender": "male",
            "location": "Kampala, Uganda",
            "symptoms": ["diarrhea", "vomiting", "abdominal pain"],
            "vital_signs": {"temperature": 37.5},
            "medical_history": []
        }
    ]
    
    for patient in patients:
        response = requests.post(f"{API_BASE_URL}/patients", json=patient)
        print(f"Added patient {patient['patient_id']}: {response.json()}")

def add_sample_facilities():
    """Add sample facility data"""
    print("\nAdding sample facilities...")
    
    facilities = [
        {
            "facility_id": "F001",
            "name": "Lagos General Hospital",
            "location": "Lagos, Nigeria",
            "type": "General Hospital",
            "capacity": 200,
            "available_beds": 45,
            "equipment": ["X-ray", "Ultrasound", "Laboratory", "ICU"],
            "staff_count": 120
        },
        {
            "facility_id": "F002",
            "name": "Nairobi Health Center",
            "location": "Nairobi, Kenya",
            "type": "Health Center",
            "capacity": 100,
            "available_beds": 30,
            "equipment": ["Laboratory", "Pharmacy", "Delivery Room"],
            "staff_count": 60
        },
        {
            "facility_id": "F003",
            "name": "Accra Medical Clinic",
            "location": "Accra, Ghana",
            "type": "Clinic",
            "capacity": 50,
            "available_beds": 15,
            "equipment": ["Basic Lab", "Pharmacy"],
            "staff_count": 25
        }
    ]
    
    for facility in facilities:
        response = requests.post(f"{API_BASE_URL}/facilities", json=facility)
        print(f"Added facility {facility['facility_id']}: {response.json()}")

def test_triage():
    """Test triage functionality"""
    print("\nTesting triage system...")
    
    test_cases = [
        {
            "name": "Suspected Malaria",
            "data": {
                "symptoms": ["fever", "chills", "headache", "sweating"],
                "age": 35,
                "gender": "male",
                "vital_signs": {"temperature": 39.5}
            }
        },
        {
            "name": "Suspected Pneumonia",
            "data": {
                "symptoms": ["cough", "fever", "chest pain", "difficulty breathing"],
                "age": 68,
                "gender": "female",
                "vital_signs": {"temperature": 38.8, "oxygen_saturation": 92}
            }
        },
        {
            "name": "Common Cold",
            "data": {
                "symptoms": ["runny nose", "sore throat", "cough"],
                "age": 25,
                "gender": "female"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}:")
        response = requests.post(f"{API_BASE_URL}/triage", json=test_case['data'])
        result = response.json()
        print(f"  Urgency: {result['urgency_level']}")
        print(f"  Confidence: {result['confidence_score']:.2%}")
        print(f"  Conditions: {[c['condition'] for c in result['predicted_conditions']]}")

def get_insights():
    """Get system insights"""
    print("\n\nGetting system insights...")
    
    # Patient insights
    response = requests.get(f"{API_BASE_URL}/insights/patients")
    print("\nPatient Insights:")
    print(json.dumps(response.json(), indent=2))
    
    # Facility insights
    response = requests.get(f"{API_BASE_URL}/insights/facilities")
    print("\nFacility Insights:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("RenewedCare System Test Script")
    print("=" * 50)
    
    try:
        if test_health_check():
            add_sample_patients()
            add_sample_facilities()
            test_triage()
            get_insights()
            print("\n" + "=" * 50)
            print("✅ All tests completed successfully!")
            print("Visit http://localhost:3000 to view the dashboard")
        else:
            print("❌ Health check failed. Is the backend running?")
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to the API.")
        print("Please ensure the backend is running:")
        print("  cd backend")
        print("  python run.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
