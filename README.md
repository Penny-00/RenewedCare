# RenewedCare

AI-driven solution to strengthen primary health care in Africa. Combines data analytics, predictive modeling, and a clinician-friendly dashboard to enhance diagnosis, triage, and decision support in under-resourced communities. Built for the DataFest Hackathon.

## 🌍 Overview

RenewedCare is a comprehensive health care system designed to support primary health care delivery in African communities. The system features:

- **AI-Powered Symptom Triage**: Intelligent symptom analysis and urgency assessment
- **Data Analytics Pipeline**: Processing and analysis of patient and facility data
- **Clinician Dashboard**: Real-time insights and visualization for health care providers
- **RESTful API**: FastAPI-based backend for seamless integration

## 🏗️ Architecture

The project follows a clean separation of concerns:

```
RenewedCare/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── main.py           # API endpoints
│   │   ├── models.py         # Pydantic data models
│   │   ├── data_pipeline.py  # Data processing
│   │   └── triage_model.py   # AI triage model
│   ├── requirements.txt
│   └── run.py
├── frontend/          # React dashboard
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   └── TriageForm.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   └── App.jsx
│   └── package.json
├── data/             # Data storage
│   ├── raw/         # Raw data files
│   └── processed/   # Processed data
└── models/          # Model artifacts
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The dashboard will be available at `http://localhost:3000`

## 📊 Features

### 1. Symptom Triage System
- AI-powered symptom analysis
- Urgency level classification (Critical, High, Medium, Low)
- Disease prediction with confidence scores
- Recommended actions for clinicians
- Vital signs assessment

### 2. Data Analytics Pipeline
- Patient data processing and storage
- Health facility data management
- Statistical analysis and aggregation
- Data visualization preparation

### 3. Clinician Dashboard
- Real-time health metrics
- Patient demographics visualization
- Common symptoms analysis
- Facility utilization tracking
- Interactive charts and graphs

## 🔌 API Endpoints

### Health Check
- `GET /health` - System health status

### Patient Management
- `POST /patients` - Add new patient data
- `GET /patients` - Retrieve all patients

### Facility Management
- `POST /facilities` - Add new facility data
- `GET /facilities` - Retrieve all facilities

### Triage
- `POST /triage` - Perform symptom-based triage

### Insights
- `GET /insights/patients` - Patient statistics
- `GET /insights/facilities` - Facility statistics
- `GET /insights/health` - Overall health insights

## 🧪 Testing the System

### Sample Triage Request

Use the web interface or send a POST request to `/triage`:

```json
{
  "symptoms": ["fever", "headache", "chills"],
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

### Sample Patient Data

```json
{
  "patient_id": "P001",
  "age": 45,
  "gender": "female",
  "location": "Lagos, Nigeria",
  "symptoms": ["cough", "fever", "chest pain"],
  "vital_signs": {
    "temperature": 38.5,
    "blood_pressure_systolic": 140
  },
  "medical_history": ["hypertension"]
}
```

## 🏥 Disease Detection

The AI model can identify and triage the following conditions:
- Malaria
- Typhoid
- Pneumonia
- Tuberculosis
- Diarrheal diseases
- Hypertension crisis
- Diabetes complications
- Asthma attacks
- Common cold
- Migraine

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Pydantic**: Data validation
- **Pandas**: Data processing
- **NumPy**: Numerical computations
- **scikit-learn**: ML model components

### Frontend
- **React**: UI library
- **Vite**: Build tool
- **Recharts**: Data visualization
- **Axios**: HTTP client

## 📈 Future Enhancements

- [ ] Machine learning model training on real African health data
- [ ] Multi-language support (English, Swahili, French, etc.)
- [ ] Mobile application
- [ ] Offline mode for rural areas
- [ ] Integration with electronic health records (EHR)
- [ ] Telemedicine capabilities
- [ ] SMS-based triage for feature phones

## 🤝 Contributing

This project was built for the DataFest Hackathon. Contributions are welcome to improve the system for real-world deployment.

## 📄 License

MIT License - see LICENSE file for details

## 👥 Authors

Built for DataFest Hackathon to strengthen primary health care in Africa.

## 🙏 Acknowledgments

- African health care workers for their invaluable insights
- DataFest Hackathon organizers
- Open-source community for the amazing tools and libraries
