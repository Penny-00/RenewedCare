import pandas as pd
import json
from typing import List, Dict
from pathlib import Path


class DataPipeline:
    """Data pipeline for processing patient and facility data"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Create directories if they don't exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def process_patient_data(self, data: List[Dict]) -> pd.DataFrame:
        """Process and clean patient data"""
        df = pd.DataFrame(data)
        
        # Data cleaning and processing
        if not df.empty:
            # Convert symptoms to string representation
            if 'symptoms' in df.columns:
                df['symptoms_str'] = df['symptoms'].apply(
                    lambda x: ','.join(x) if isinstance(x, list) else str(x)
                )
            
            # Standardize gender values
            if 'gender' in df.columns:
                df['gender'] = df['gender'].str.lower()
            
            # Add processing timestamp
            df['processed_at'] = pd.Timestamp.now()
        
        return df
    
    def process_facility_data(self, data: List[Dict]) -> pd.DataFrame:
        """Process and clean facility data"""
        df = pd.DataFrame(data)
        
        # Data cleaning and processing
        if not df.empty:
            # Calculate utilization rate
            if 'capacity' in df.columns and 'available_beds' in df.columns:
                df['utilization_rate'] = (
                    (df['capacity'] - df['available_beds']) / df['capacity'] * 100
                )
            
            # Convert equipment list to string
            if 'equipment' in df.columns:
                df['equipment_str'] = df['equipment'].apply(
                    lambda x: ','.join(x) if isinstance(x, list) else str(x)
                )
            
            # Add processing timestamp
            df['processed_at'] = pd.Timestamp.now()
        
        return df
    
    def save_processed_data(self, df: pd.DataFrame, filename: str):
        """Save processed data to file"""
        filepath = self.processed_dir / filename
        df.to_csv(filepath, index=False)
        return filepath
    
    def load_processed_data(self, filename: str) -> pd.DataFrame:
        """Load processed data from file"""
        filepath = self.processed_dir / filename
        if filepath.exists():
            return pd.read_csv(filepath)
        return pd.DataFrame()
    
    def get_patient_statistics(self) -> Dict:
        """Get statistics from patient data"""
        df = self.load_processed_data('patients.csv')
        
        if df.empty:
            return {}
        
        stats = {
            'total_patients': len(df),
            'avg_age': float(df['age'].mean()) if 'age' in df.columns else 0,
            'gender_distribution': df['gender'].value_counts().to_dict() if 'gender' in df.columns else {},
            'location_distribution': df['location'].value_counts().to_dict() if 'location' in df.columns else {}
        }
        
        return stats
    
    def get_facility_statistics(self) -> Dict:
        """Get statistics from facility data"""
        df = self.load_processed_data('facilities.csv')
        
        if df.empty:
            return {}
        
        stats = {
            'total_facilities': len(df),
            'avg_capacity': float(df['capacity'].mean()) if 'capacity' in df.columns else 0,
            'avg_utilization': float(df['utilization_rate'].mean()) if 'utilization_rate' in df.columns else 0,
            'total_staff': int(df['staff_count'].sum()) if 'staff_count' in df.columns else 0
        }
        
        return stats
