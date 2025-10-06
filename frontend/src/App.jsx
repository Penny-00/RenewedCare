import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import TriageForm from './components/TriageForm';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const tabStyle = (isActive) => ({
    padding: '12px 24px',
    border: 'none',
    background: isActive ? '#1976d2' : '#e0e0e0',
    color: isActive ? 'white' : '#333',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: isActive ? 'bold' : 'normal',
    borderRadius: '4px 4px 0 0',
    marginRight: '5px'
  });

  return (
    <div style={{ minHeight: '100vh', background: '#f5f5f5' }}>
      {/* Header */}
      <header style={{
        background: '#1976d2',
        color: 'white',
        padding: '20px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h1 style={{ margin: 0, fontSize: '28px' }}>
          🏥 RenewedCare - Primary Health Care System
        </h1>
        <p style={{ margin: '5px 0 0 0', fontSize: '14px', opacity: 0.9 }}>
          AI-driven solution for strengthening primary health care in Africa
        </p>
      </header>

      {/* Navigation Tabs */}
      <div style={{ background: 'white', padding: '0 20px', borderBottom: '2px solid #ddd' }}>
        <button
          onClick={() => setActiveTab('dashboard')}
          style={tabStyle(activeTab === 'dashboard')}
        >
          📊 Dashboard
        </button>
        <button
          onClick={() => setActiveTab('triage')}
          style={tabStyle(activeTab === 'triage')}
        >
          🩺 Symptom Triage
        </button>
      </div>

      {/* Main Content */}
      <main>
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'triage' && <TriageForm />}
      </main>

      {/* Footer */}
      <footer style={{
        background: '#333',
        color: 'white',
        textAlign: 'center',
        padding: '20px',
        marginTop: '40px'
      }}>
        <p style={{ margin: 0 }}>
          RenewedCare © 2025 - Built for DataFest Hackathon
        </p>
      </footer>
    </div>
  );
}

export default App;
