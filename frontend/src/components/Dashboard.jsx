import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import apiService from '../services/api';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const Dashboard = () => {
  const [patientInsights, setPatientInsights] = useState(null);
  const [facilityInsights, setFacilityInsights] = useState(null);
  const [healthInsights, setHealthInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [patientsRes, facilitiesRes, healthRes] = await Promise.all([
        apiService.getPatientInsights(),
        apiService.getFacilityInsights(),
        apiService.getHealthInsights(),
      ]);

      setPatientInsights(patientsRes.data);
      setFacilityInsights(facilitiesRes.data);
      setHealthInsights(healthRes.data);
      setError(null);
    } catch (err) {
      console.error('Error loading dashboard data:', err);
      setError('Failed to load dashboard data. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const formatGenderData = (genderDist) => {
    if (!genderDist) return [];
    return Object.entries(genderDist).map(([name, value]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value
    }));
  };

  const formatLocationData = (locationDist) => {
    if (!locationDist) return [];
    return Object.entries(locationDist).map(([name, value]) => ({
      name,
      patients: value
    })).slice(0, 10); // Top 10 locations
  };

  const formatTopSymptoms = (symptoms) => {
    if (!symptoms) return [];
    return symptoms.slice(0, 8).map(s => ({
      symptom: s.symptom.charAt(0).toUpperCase() + s.symptom.slice(1),
      count: s.count
    }));
  };

  if (loading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <h2>Loading dashboard...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px', textAlign: 'center', color: '#d32f2f' }}>
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={loadDashboardData} style={{ padding: '10px 20px', marginTop: '10px' }}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1 style={{ marginBottom: '30px', color: '#1976d2' }}>RenewedCare Analytics Dashboard</h1>
      
      {/* Key Metrics */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        <div style={{ background: '#e3f2fd', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#1976d2' }}>Total Patients</h3>
          <p style={{ fontSize: '36px', fontWeight: 'bold', margin: 0 }}>
            {patientInsights?.total_patients || 0}
          </p>
        </div>
        
        <div style={{ background: '#e8f5e9', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#388e3c' }}>Total Facilities</h3>
          <p style={{ fontSize: '36px', fontWeight: 'bold', margin: 0 }}>
            {facilityInsights?.total_facilities || 0}
          </p>
        </div>
        
        <div style={{ background: '#fff3e0', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#f57c00' }}>Avg Patient Age</h3>
          <p style={{ fontSize: '36px', fontWeight: 'bold', margin: 0 }}>
            {patientInsights?.avg_age ? Math.round(patientInsights.avg_age) : 'N/A'}
          </p>
        </div>
        
        <div style={{ background: '#fce4ec', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#c2185b' }}>Facility Utilization</h3>
          <p style={{ fontSize: '36px', fontWeight: 'bold', margin: 0 }}>
            {facilityInsights?.avg_utilization ? `${Math.round(facilityInsights.avg_utilization)}%` : 'N/A'}
          </p>
        </div>
      </div>

      {/* Charts Section */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '30px' }}>
        {/* Gender Distribution */}
        {patientInsights?.gender_distribution && Object.keys(patientInsights.gender_distribution).length > 0 && (
          <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <h3 style={{ marginTop: 0, color: '#333' }}>Gender Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={formatGenderData(patientInsights.gender_distribution)}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {formatGenderData(patientInsights.gender_distribution).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Top Symptoms */}
        {patientInsights?.top_symptoms && patientInsights.top_symptoms.length > 0 && (
          <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <h3 style={{ marginTop: 0, color: '#333' }}>Most Common Symptoms</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={formatTopSymptoms(patientInsights.top_symptoms)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="symptom" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Location Distribution */}
        {patientInsights?.location_distribution && Object.keys(patientInsights.location_distribution).length > 0 && (
          <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <h3 style={{ marginTop: 0, color: '#333' }}>Patients by Location</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={formatLocationData(patientInsights.location_distribution)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="patients" fill="#00C49F" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Health Insights Trend */}
        {healthInsights && healthInsights.length > 0 && (
          <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <h3 style={{ marginTop: 0, color: '#333' }}>Health Metrics Overview</h3>
            <div style={{ marginTop: '20px' }}>
              {healthInsights.map((insight, index) => (
                <div key={index} style={{ marginBottom: '15px', padding: '15px', background: '#f5f5f5', borderRadius: '4px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: 'bold', color: '#333' }}>{insight.metric_name}</span>
                    <span style={{ fontSize: '24px', fontWeight: 'bold', color: '#1976d2' }}>
                      {insight.value.toFixed(1)}
                    </span>
                  </div>
                  <div style={{ marginTop: '5px', fontSize: '12px', color: '#666' }}>
                    Trend: <span style={{ 
                      color: insight.trend === 'increasing' ? '#f57c00' : '#4caf50',
                      fontWeight: 'bold'
                    }}>
                      {insight.trend}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Refresh Button */}
      <div style={{ marginTop: '30px', textAlign: 'center' }}>
        <button 
          onClick={loadDashboardData}
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            background: '#1976d2',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
          }}
          onMouseOver={(e) => e.target.style.background = '#1565c0'}
          onMouseOut={(e) => e.target.style.background = '#1976d2'}
        >
          Refresh Data
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
