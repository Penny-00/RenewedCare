# RenewedCare Setup Guide

This guide will help you set up and run the RenewedCare system on your local machine.

## System Requirements

- **Python**: 3.8 or higher
- **Node.js**: 16.x or higher
- **npm**: 7.x or higher
- **Git**: For cloning the repository

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Penny-00/RenewedCare.git
cd RenewedCare
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Run the Backend Server

```bash
python run.py
```

The backend API will be available at `http://localhost:8000`

You can verify it's running by visiting:
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 3. Frontend Setup

Open a new terminal window:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Quick Test

### Option 1: Use the Web Interface

1. Open your browser and go to `http://localhost:3000`
2. You'll see the RenewedCare dashboard
3. Click on the "Symptom Triage" tab
4. Enter patient symptoms (e.g., "fever, headache, chills")
5. Fill in age and vital signs
6. Click "Perform Triage" to see AI-powered recommendations

### Option 2: Use the Test Script

From the project root directory:

```bash
python test_system.py
```

This will:
- Add sample patient data
- Add sample facility data
- Run triage tests
- Display insights

## Project Structure

```
RenewedCare/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # API endpoints
│   │   ├── models.py    # Data models
│   │   ├── data_pipeline.py  # Data processing
│   │   └── triage_model.py   # AI model
│   └── requirements.txt
│
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   └── TriageForm.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   └── App.jsx
│   └── package.json
│
├── data/               # Data storage
│   ├── raw/           # Raw data
│   └── processed/     # Processed data
│
└── models/            # Model artifacts
```

## Usage Examples

### Adding a Patient via API

```bash
curl -X POST http://localhost:8000/patients \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P001",
    "age": 35,
    "gender": "male",
    "location": "Lagos, Nigeria",
    "symptoms": ["fever", "headache"],
    "vital_signs": {"temperature": 38.5}
  }'
```

### Performing Triage

```bash
curl -X POST http://localhost:8000/triage \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["fever", "cough", "difficulty breathing"],
    "age": 65,
    "gender": "female",
    "vital_signs": {
      "temperature": 39.0,
      "oxygen_saturation": 92
    }
  }'
```

### Getting Insights

```bash
# Patient insights
curl http://localhost:8000/insights/patients

# Facility insights
curl http://localhost:8000/insights/facilities

# Health metrics
curl http://localhost:8000/insights/health
```

## Common Issues and Solutions

### Issue: Backend won't start

**Solution**: Make sure you have activated the virtual environment and installed all dependencies:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Issue: Frontend shows CORS errors

**Solution**: Ensure the backend is running on port 8000. The frontend is configured to proxy API requests to `http://localhost:8000`.

### Issue: Module not found errors

**Solution**: 
- For Python: Ensure you're in the backend directory and virtual environment is activated
- For Node: Run `npm install` in the frontend directory

### Issue: Port already in use

**Solution**: 
- Change the backend port in `backend/run.py` (line with `port=8000`)
- Change the frontend port in `frontend/vite.config.js` (line with `port: 3000`)

## Development Workflow

### Running in Development Mode

1. **Backend** (with auto-reload):
   ```bash
   cd backend
   python run.py  # Uses uvicorn with reload=True
   ```

2. **Frontend** (with hot-reload):
   ```bash
   cd frontend
   npm run dev
   ```

### Building for Production

#### Backend
The backend can be deployed using any ASGI server:
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### Frontend
Build the optimized production bundle:
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

## Environment Variables

Create a `.env` file in the backend directory for configuration:

```env
# Backend settings
API_HOST=0.0.0.0
API_PORT=8000

# CORS settings (for production)
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## Next Steps

1. **Customize the AI Model**: Edit `backend/app/triage_model.py` to add more diseases or adjust urgency levels
2. **Add More Visualizations**: Extend `frontend/src/components/Dashboard.jsx` with additional charts
3. **Implement Authentication**: Add user authentication for multi-tenancy
4. **Deploy to Cloud**: Consider deploying to AWS, Azure, or Google Cloud Platform

## Support

For issues and questions:
- Check the [API Documentation](./API_DOCUMENTATION.md)
- Review the [README](./README.md)
- Open an issue on GitHub

---

**Happy coding! Let's strengthen primary health care in Africa together! 🏥🌍**
