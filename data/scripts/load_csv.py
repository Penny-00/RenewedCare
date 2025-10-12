import pandas as pd
import numpy as np
from sqlalchemy import inspect
from pathlib import Path
import logging
import json
from datetime import datetime
from database.db_connection import engine

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)  

# Configuration for table naming and CSV processing
CONFIG = {
    'csv_directory': './raw',
    'table_prefix': '',  # Optional prefix for all tables
    'if_exists': 'replace',  # 'fail', 'replace', or 'append'
    'chunksize': 1000,
    'date_columns_pattern': ['date', 'epiwk', 'time', 'created', 'updated'],  # Auto-detect date columns
}

def sanitize_table_name(filename):
    """
    Convert filename to valid PostgreSQL table name
    
    Rules:
    - Lowercase
    - Replace spaces and special chars with underscores
    - Remove file extension
    """
    name = Path(filename).stem.lower()
    name = ''.join(c if c.isalnum() else '_' for c in name)
    name = '_'.join(filter(None, name.split('_')))  # Remove consecutive underscores
    
    # Ensure doesn't start with number
    if name[0].isdigit():
        name = 'table_' + name
    
    return CONFIG['table_prefix'] + name

def detect_date_columns(df):
    """
    Auto-detect columns that should be treated as dates
    """
    date_cols = []
    
    for col in df.columns:
        col_lower = col.lower()
        
        # Check if column name suggests it's a date
        if any(pattern in col_lower for pattern in CONFIG['date_columns_pattern']):
            date_cols.append(col)
            continue
        
        # Check if data looks like dates
        if df[col].dtype == 'object':
            sample = df[col].dropna().head(100)
            if len(sample) > 0:
                try:
                    pd.to_datetime(sample, errors='coerce')
                    non_null_ratio = sample.notna().sum() / len(sample)
                    if non_null_ratio > 0.8:  # 80% successfully parsed
                        date_cols.append(col)
                except:
                    pass
    
    return date_cols

def clean_dataframe(df, csv_name):
    """
    Generic cleaning for any CSV file
    """
    logger.info(f"  Original shape: {df.shape}")
    
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    
    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        # Replace string 'nan', 'None', empty strings with actual NaN
        df[col] = df[col].replace(['nan', 'None', 'NaN', ''], np.nan)
    
    # Handle Inf/-Inf values across all numeric columns
    df = df.replace([np.inf, -np.inf], np.nan)
    
    # Auto-detect and convert date columns
    date_cols = detect_date_columns(df)
    if date_cols:
        logger.info(f"  Detected date columns: {date_cols}")
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Remove completely duplicate rows
    initial_rows = len(df)
    df = df.drop_duplicates()
    if initial_rows > len(df):
        logger.info(f"  Removed {initial_rows - len(df)} duplicate rows")
    
    logger.info(f"  Cleaned shape: {df.shape}")
    
    return df

def get_table_info(table_name):
    """Get information about existing table"""
    inspector = inspect(engine)
    if inspector.has_table(table_name):
        columns = inspector.get_columns(table_name)
        row_count = pd.read_sql(f"SELECT COUNT(*) FROM {table_name}", engine).iloc[0, 0]
        return {
            'exists': True,
            'columns': [col['name'] for col in columns],
            'row_count': row_count
        }
    return {'exists': False}

def load_csv_to_db(csv_path, table_name=None, if_exists=None):
    """
    Load a single CSV file into database with automatic schema detection
    
    Args:
        csv_path: Path to CSV file
        table_name: Custom table name (optional, auto-generated from filename)
        if_exists: 'fail', 'replace', or 'append'
    """
    csv_path = Path(csv_path)
    
    if not csv_path.exists():
        logger.error(f"File not found: {csv_path}")
        return False
    
    # Generate table name if not provided
    if table_name is None:
        table_name = sanitize_table_name(csv_path.name)
    
    if_exists = if_exists or CONFIG['if_exists']
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Processing: {csv_path.name}")
    logger.info(f"Target table: {table_name}")
    
    try:
        # Check existing table
        table_info = get_table_info(table_name)
        if table_info['exists']:
            logger.info(f"  Table exists with {table_info['row_count']} rows")
            logger.info(f"  Action: {if_exists}")
        
        # Load CSV
        df = pd.read_csv(csv_path)
        logger.info(f"  Loaded {len(df)} rows, {len(df.columns)} columns")
        
        # Clean data
        df = clean_dataframe(df, csv_path.name)
        
        # Load to database
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists=if_exists,
            index=False,
            method='multi',
            chunksize=CONFIG['chunksize']
        )
        
        # Verify
        new_count = pd.read_sql(f"SELECT COUNT(*) FROM {table_name}", engine).iloc[0, 0]
        logger.info(f"✓ Success! Table '{table_name}' now has {new_count} rows")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Error loading {csv_path.name}: {e}")
        return False

def load_all_csvs(directory=None, pattern='*.csv', mapping_file=None):
    """
    Load all CSV files from directory
    
    Args:
        directory: Directory containing CSV files
        pattern: File pattern to match (default: '*.csv')
        mapping_file: Optional JSON file mapping CSV files to table names
    """
    directory = Path(directory or CONFIG['csv_directory'])
    
    if not directory.exists():
        logger.error(f"Directory not found: {directory}")
        return
    
    # Load custom mapping if provided
    csv_to_table = {}
    if mapping_file and Path(mapping_file).exists():
        with open(mapping_file, 'r') as f:
            csv_to_table = json.load(f)
        logger.info(f"Loaded table name mappings from {mapping_file}")
    
    # Find all CSV files
    csv_files = sorted(list(directory.glob(pattern)))
    logger.info(f"\nFound {len(csv_files)} CSV files in {directory}")
    
    if len(csv_files) == 0:
        logger.warning("No CSV files found!")
        return
    
    # Process each CSV
    results = {
        'success': [],
        'failed': []
    }
    
    for csv_file in csv_files:
        table_name = csv_to_table.get(csv_file.name)  # Use mapping if exists
        
        if load_csv_to_db(csv_file, table_name=table_name):
            results['success'].append(csv_file.name)
        else:
            results['failed'].append(csv_file.name)
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"✓ Successfully loaded: {len(results['success'])} files")
    logger.info(f"✗ Failed: {len(results['failed'])} files")
    
    if results['failed']:
        logger.info("\nFailed files:")
        for filename in results['failed']:
            logger.info(f"  - {filename}")
    
    return results

def list_all_tables():
    """List all tables in the database with row counts"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    logger.info(f"\n{'='*60}")
    logger.info(f"DATABASE TABLES ({len(tables)} total)")
    logger.info(f"{'='*60}")
    
    for table in sorted(tables):
        try:
            count = pd.read_sql(f"SELECT COUNT(*) FROM {table}", engine).iloc[0, 0]
            logger.info(f"  {table}: {count:,} rows")
        except Exception as e:
            logger.info(f"  {table}: Error reading - {e}")

def create_mapping_template(directory=None, output_file='table_mapping.json'):
    """
    Create a template JSON file for custom table name mappings
    """
    directory = Path(directory or CONFIG['csv_directory'])
    csv_files = list(directory.glob('*.csv'))
    
    mapping = {}
    for csv_file in csv_files:
        auto_name = sanitize_table_name(csv_file.name)
        mapping[csv_file.name] = auto_name  # You can manually edit this
    
    with open(output_file, 'w') as f:
        json.dump(mapping, f, indent=2)
    
    logger.info(f"Created mapping template: {output_file}")
    logger.info("Edit this file to customize table names, then use with --mapping flag")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Load CSV files into PostgreSQL')
    parser.add_argument('--dir', default='./csv_files', help='Directory containing CSV files')
    parser.add_argument('--file', help='Load a single CSV file')
    parser.add_argument('--table', help='Table name for single file')
    parser.add_argument('--mapping', help='JSON file with CSV to table name mappings')
    parser.add_argument('--if-exists', choices=['fail', 'replace', 'append'], 
                       default='replace', help='What to do if table exists')
    parser.add_argument('--list-tables', action='store_true', help='List all database tables')
    parser.add_argument('--create-mapping', action='store_true', 
                       help='Create table mapping template')
    
    args = parser.parse_args()
    
    # Update config
    CONFIG['if_exists'] = args.if_exists
    
    if args.list_tables:
        list_all_tables()
    elif args.create_mapping:
        create_mapping_template(args.dir)
    elif args.file:
        # Load single file
        load_csv_to_db(args.file, table_name=args.table, if_exists=args.if_exists)
    else:
        # Load all files from directory
        load_all_csvs(directory=args.dir, mapping_file=args.mapping)
        list_all_tables()