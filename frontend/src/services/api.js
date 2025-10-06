import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Patient endpoints
  getPatients: () => api.get('/patients'),
  addPatient: (patientData) => api.post('/patients', patientData),
  
  // Facility endpoints
  getFacilities: () => api.get('/facilities'),
  addFacility: (facilityData) => api.post('/facilities', facilityData),
  
  // Triage endpoint
  performTriage: (triageData) => api.post('/triage', triageData),
  
  // Insights endpoints
  getPatientInsights: () => api.get('/insights/patients'),
  getFacilityInsights: () => api.get('/insights/facilities'),
  getHealthInsights: () => api.get('/insights/health'),
  
  // Health check
  healthCheck: () => api.get('/health'),
};

export default apiService;
