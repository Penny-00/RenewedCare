import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SymptomTriageModel:
    """AI model for symptom-based triage and health insights"""
    
    def __init__(self):
        # Disease knowledge base with symptoms and urgency levels
        self.disease_database = {
            'malaria': {
                'symptoms': ['fever', 'chills', 'headache', 'sweating', 'fatigue', 'nausea', 'vomiting'],
                'urgency': 'high',
                'actions': ['Get immediate medical attention', 'Blood test for confirmation', 'Start antimalarial treatment']
            },
            'typhoid': {
                'symptoms': ['fever', 'weakness', 'abdominal pain', 'headache', 'loss of appetite'],
                'urgency': 'high',
                'actions': ['Blood culture test', 'Start antibiotics', 'Monitor hydration']
            },
            'common_cold': {
                'symptoms': ['runny nose', 'sore throat', 'cough', 'sneezing', 'mild fever'],
                'urgency': 'low',
                'actions': ['Rest and hydration', 'Over-the-counter medication', 'Monitor symptoms']
            },
            'pneumonia': {
                'symptoms': ['cough', 'fever', 'chest pain', 'difficulty breathing', 'fatigue'],
                'urgency': 'high',
                'actions': ['Immediate medical attention', 'Chest X-ray', 'Antibiotics if bacterial']
            },
            'tuberculosis': {
                'symptoms': ['persistent cough', 'chest pain', 'coughing blood', 'fever', 'night sweats', 'weight loss'],
                'urgency': 'high',
                'actions': ['Sputum test', 'Chest X-ray', 'Start TB treatment if positive', 'Isolation measures']
            },
            'diarrheal_disease': {
                'symptoms': ['diarrhea', 'abdominal pain', 'nausea', 'vomiting', 'dehydration'],
                'urgency': 'medium',
                'actions': ['Oral rehydration solution', 'Monitor hydration', 'Stool test if severe']
            },
            'hypertension_crisis': {
                'symptoms': ['severe headache', 'chest pain', 'difficulty breathing', 'dizziness', 'blurred vision'],
                'urgency': 'critical',
                'actions': ['Emergency medical attention', 'Blood pressure monitoring', 'Immediate medication']
            },
            'diabetes_complication': {
                'symptoms': ['extreme thirst', 'frequent urination', 'fatigue', 'blurred vision', 'confusion'],
                'urgency': 'high',
                'actions': ['Blood glucose test', 'Immediate medical attention', 'Insulin adjustment if needed']
            },
            'asthma_attack': {
                'symptoms': ['difficulty breathing', 'wheezing', 'chest tightness', 'coughing'],
                'urgency': 'high',
                'actions': ['Use rescue inhaler', 'Seek immediate medical attention if severe', 'Avoid triggers']
            },
            'migraine': {
                'symptoms': ['severe headache', 'nausea', 'sensitivity to light', 'visual disturbances'],
                'urgency': 'medium',
                'actions': ['Rest in dark room', 'Pain medication', 'Monitor severity']
            }
        }
        
        # Initialize vectorizer for symptom matching
        self.vectorizer = TfidfVectorizer()
        self._prepare_model()
    
    def _prepare_model(self):
        """Prepare the symptom matching model"""
        # Create corpus of all disease symptoms
        self.disease_names = list(self.disease_database.keys())
        self.disease_symptom_texts = [
            ' '.join(self.disease_database[disease]['symptoms']) 
            for disease in self.disease_names
        ]
        
        # Fit vectorizer
        self.disease_vectors = self.vectorizer.fit_transform(self.disease_symptom_texts)
    
    def predict_triage(
        self, 
        symptoms: List[str], 
        age: int, 
        gender: str, 
        vital_signs: Dict = None
    ) -> Dict:
        """
        Predict triage urgency and likely conditions based on symptoms
        """
        # Convert symptoms to text
        symptom_text = ' '.join([s.lower() for s in symptoms])
        
        # Vectorize input symptoms
        symptom_vector = self.vectorizer.transform([symptom_text])
        
        # Calculate similarity with all diseases
        similarities = cosine_similarity(symptom_vector, self.disease_vectors)[0]
        
        # Get top 3 matches
        top_indices = np.argsort(similarities)[::-1][:3]
        
        predicted_conditions = []
        max_urgency = 'low'
        all_actions = set()
        
        urgency_priority = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Threshold for relevance
                disease_name = self.disease_names[idx]
                disease_info = self.disease_database[disease_name]
                
                predicted_conditions.append({
                    'condition': disease_name.replace('_', ' ').title(),
                    'confidence': float(similarities[idx]),
                    'matching_symptoms': self._get_matching_symptoms(symptoms, disease_info['symptoms'])
                })
                
                # Update urgency level (take the highest)
                if urgency_priority.get(disease_info['urgency'], 0) > urgency_priority.get(max_urgency, 0):
                    max_urgency = disease_info['urgency']
                
                # Collect recommended actions
                all_actions.update(disease_info['actions'])
        
        # Age and vital signs adjustments
        if age < 5 or age > 65:
            max_urgency = self._escalate_urgency(max_urgency)
            all_actions.add('Consider age-specific complications')
        
        if vital_signs:
            vital_urgency = self._assess_vital_signs(vital_signs)
            if urgency_priority.get(vital_urgency, 0) > urgency_priority.get(max_urgency, 0):
                max_urgency = vital_urgency
        
        # Calculate overall confidence
        avg_confidence = float(np.mean([c['confidence'] for c in predicted_conditions])) if predicted_conditions else 0.0
        
        return {
            'urgency_level': max_urgency,
            'predicted_conditions': predicted_conditions,
            'recommended_actions': list(all_actions),
            'confidence_score': avg_confidence
        }
    
    def _get_matching_symptoms(self, input_symptoms: List[str], disease_symptoms: List[str]) -> List[str]:
        """Find which symptoms match the disease"""
        input_lower = [s.lower() for s in input_symptoms]
        matches = []
        
        for ds in disease_symptoms:
            for inp in input_lower:
                if ds in inp or inp in ds:
                    matches.append(ds)
                    break
        
        return matches
    
    def _escalate_urgency(self, current_urgency: str) -> str:
        """Escalate urgency level"""
        escalation = {
            'low': 'medium',
            'medium': 'high',
            'high': 'critical',
            'critical': 'critical'
        }
        return escalation.get(current_urgency, current_urgency)
    
    def _assess_vital_signs(self, vital_signs: Dict) -> str:
        """Assess urgency based on vital signs"""
        urgency = 'low'
        
        # Temperature assessment
        if 'temperature' in vital_signs:
            temp = vital_signs['temperature']
            if temp > 39.5 or temp < 35:
                urgency = 'high'
            elif temp > 38.5 or temp < 36:
                urgency = 'medium'
        
        # Blood pressure assessment
        if 'blood_pressure_systolic' in vital_signs:
            systolic = vital_signs['blood_pressure_systolic']
            if systolic > 180 or systolic < 90:
                return 'critical'
            elif systolic > 140 or systolic < 100:
                urgency = 'medium'
        
        # Heart rate assessment
        if 'heart_rate' in vital_signs:
            hr = vital_signs['heart_rate']
            if hr > 120 or hr < 50:
                urgency = 'high'
            elif hr > 100 or hr < 60:
                urgency = 'medium' if urgency == 'low' else urgency
        
        # Oxygen saturation assessment
        if 'oxygen_saturation' in vital_signs:
            o2 = vital_signs['oxygen_saturation']
            if o2 < 90:
                return 'critical'
            elif o2 < 95:
                urgency = 'high'
        
        return urgency
    
    def get_health_insights(self, patient_data: List[Dict]) -> Dict:
        """Generate health insights from patient data"""
        if not patient_data:
            return {}
        
        # Aggregate symptoms
        all_symptoms = {}
        urgency_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for patient in patient_data:
            # Count symptom frequencies
            for symptom in patient.get('symptoms', []):
                symptom_lower = symptom.lower()
                all_symptoms[symptom_lower] = all_symptoms.get(symptom_lower, 0) + 1
        
        # Get top symptoms
        top_symptoms = sorted(all_symptoms.items(), key=lambda x: x[1], reverse=True)[:10]
        
        insights = {
            'total_cases': len(patient_data),
            'top_symptoms': [{'symptom': s[0], 'count': s[1]} for s in top_symptoms],
            'urgency_distribution': urgency_counts
        }
        
        return insights
