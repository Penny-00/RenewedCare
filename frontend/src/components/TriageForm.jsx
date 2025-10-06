import React, { useState } from 'react';
import apiService from '../services/api';

const TriageForm = () => {
  const [formData, setFormData] = useState({
    symptoms: '',
    age: '',
    gender: 'male',
    temperature: '',
    bloodPressureSystolic: '',
    heartRate: '',
    oxygenSaturation: ''
  });

  const [triageResult, setTriageResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const symptomsArray = formData.symptoms.split(',').map(s => s.trim()).filter(s => s);
      
      const vitalSigns = {};
      if (formData.temperature) vitalSigns.temperature = parseFloat(formData.temperature);
      if (formData.bloodPressureSystolic) vitalSigns.blood_pressure_systolic = parseInt(formData.bloodPressureSystolic);
      if (formData.heartRate) vitalSigns.heart_rate = parseInt(formData.heartRate);
      if (formData.oxygenSaturation) vitalSigns.oxygen_saturation = parseInt(formData.oxygenSaturation);

      const requestData = {
        symptoms: symptomsArray,
        age: parseInt(formData.age),
        gender: formData.gender,
        vital_signs: Object.keys(vitalSigns).length > 0 ? vitalSigns : null
      };

      const response = await apiService.performTriage(requestData);
      setTriageResult(response.data);
    } catch (err) {
      console.error('Triage error:', err);
      setError('Failed to perform triage. Please check your input and try again.');
    } finally {
      setLoading(false);
    }
  };

  const getUrgencyColor = (urgency) => {
    const colors = {
      critical: '#d32f2f',
      high: '#f57c00',
      medium: '#fbc02d',
      low: '#388e3c'
    };
    return colors[urgency] || '#757575';
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h2 style={{ color: '#1976d2', marginBottom: '20px' }}>Symptom Triage Assessment</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
        {/* Form */}
        <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
          <h3 style={{ marginTop: 0 }}>Patient Information</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                Symptoms (comma-separated):
              </label>
              <input
                type="text"
                value={formData.symptoms}
                onChange={(e) => setFormData({ ...formData, symptoms: e.target.value })}
                placeholder="e.g., fever, headache, cough"
                required
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '14px'
                }}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>Age:</label>
                <input
                  type="number"
                  value={formData.age}
                  onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                  required
                  min="1"
                  max="120"
                  style={{
                    width: '100%',
                    padding: '10px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>Gender:</label>
                <select
                  value={formData.gender}
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                  style={{
                    width: '100%',
                    padding: '10px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>

            <h4 style={{ marginTop: '20px', marginBottom: '10px' }}>Vital Signs (Optional)</h4>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '14px' }}>
                  Temperature (°C):
                </label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.temperature}
                  onChange={(e) => setFormData({ ...formData, temperature: e.target.value })}
                  placeholder="37.0"
                  style={{
                    width: '100%',
                    padding: '8px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '14px' }}>
                  Blood Pressure (Systolic):
                </label>
                <input
                  type="number"
                  value={formData.bloodPressureSystolic}
                  onChange={(e) => setFormData({ ...formData, bloodPressureSystolic: e.target.value })}
                  placeholder="120"
                  style={{
                    width: '100%',
                    padding: '8px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '14px' }}>
                  Heart Rate (bpm):
                </label>
                <input
                  type="number"
                  value={formData.heartRate}
                  onChange={(e) => setFormData({ ...formData, heartRate: e.target.value })}
                  placeholder="75"
                  style={{
                    width: '100%',
                    padding: '8px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '14px' }}>
                  O2 Saturation (%):
                </label>
                <input
                  type="number"
                  value={formData.oxygenSaturation}
                  onChange={(e) => setFormData({ ...formData, oxygenSaturation: e.target.value })}
                  placeholder="98"
                  style={{
                    width: '100%',
                    padding: '8px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              style={{
                marginTop: '20px',
                width: '100%',
                padding: '12px',
                background: loading ? '#ccc' : '#1976d2',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                fontSize: '16px',
                fontWeight: 'bold',
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
            >
              {loading ? 'Analyzing...' : 'Perform Triage'}
            </button>
          </form>

          {error && (
            <div style={{
              marginTop: '15px',
              padding: '10px',
              background: '#ffebee',
              color: '#c62828',
              borderRadius: '4px'
            }}>
              {error}
            </div>
          )}
        </div>

        {/* Results */}
        <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
          <h3 style={{ marginTop: 0 }}>Triage Results</h3>
          
          {!triageResult ? (
            <p style={{ color: '#666', textAlign: 'center', marginTop: '50px' }}>
              Submit patient information to see triage results
            </p>
          ) : (
            <div>
              {/* Urgency Level */}
              <div style={{
                padding: '20px',
                background: getUrgencyColor(triageResult.urgency_level),
                color: 'white',
                borderRadius: '8px',
                marginBottom: '20px',
                textAlign: 'center'
              }}>
                <h2 style={{ margin: 0 }}>
                  {triageResult.urgency_level.toUpperCase()} PRIORITY
                </h2>
                <p style={{ margin: '10px 0 0 0', fontSize: '14px' }}>
                  Confidence: {(triageResult.confidence_score * 100).toFixed(1)}%
                </p>
              </div>

              {/* Predicted Conditions */}
              <div style={{ marginBottom: '20px' }}>
                <h4 style={{ color: '#333' }}>Possible Conditions:</h4>
                {triageResult.predicted_conditions.map((condition, index) => (
                  <div key={index} style={{
                    padding: '10px',
                    background: '#f5f5f5',
                    borderRadius: '4px',
                    marginBottom: '10px'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <strong>{condition.condition}</strong>
                      <span style={{ color: '#1976d2', fontSize: '14px' }}>
                        {(condition.confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                    {condition.matching_symptoms && condition.matching_symptoms.length > 0 && (
                      <div style={{ marginTop: '5px', fontSize: '13px', color: '#666' }}>
                        Matching: {condition.matching_symptoms.join(', ')}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Recommended Actions */}
              <div>
                <h4 style={{ color: '#333' }}>Recommended Actions:</h4>
                <ul style={{ paddingLeft: '20px', margin: 0 }}>
                  {triageResult.recommended_actions.map((action, index) => (
                    <li key={index} style={{ marginBottom: '8px', color: '#555' }}>
                      {action}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TriageForm;
