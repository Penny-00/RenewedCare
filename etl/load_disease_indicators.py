import os
import pandas as pd
from sqlalchemy.orm import Session
from database.models.disease_dim import Disease
from database.models.disease_indicator import DiseaseIndicator
from database.db_connection import SessionLocal

def load_disease_indicators(csv_path: str, disease_name: str):
    df = pd.read_csv(csv_path)
    db = SessionLocal()

    # 🧹 Clear previous records
    #db.execute("TRUNCATE TABLE outbreak_reports RESTART IDENTITY CASCADE;")
    #db.commit()

    # Cache known diseases
    known_diseases = {d.name: d.id for d in db.query(Disease).all()}

    # Check or create the disease
    if disease_name not in known_diseases:
        disease = Disease(name=disease_name)
        db.add(disease)
        db.commit()
        db.refresh(disease)
        known_diseases[disease_name] = disease.id
    disease_id = known_diseases[disease_name]

    # Cache existing indicators for idempotency (by unique fields)
    existing = set(
        (i.indicator_code, i.year)
        for i in db.query(DiseaseIndicator.indicator_code, DiseaseIndicator.year)
        .filter(DiseaseIndicator.disease_id == disease_id)
        .all()
    )

    new_records = []
    for _, row in df.iterrows():
         # Normalize cross-dataset fields
        dimension_type = (
            row.get("DIMENSION (TYPE)")
            or row.get("sex_type")
        )
        dimension_code = (
            row.get("DIMENSION (CODE)")
            or row.get("sex_code")
        )
        dimension_name = (
            row.get("DIMENSION (NAME)")
            or row.get("sex_name")
        )
        indicator_code=(row.get("indicator_code")
            or row.get("GHO (CODE)")
        )
        indicator_name=(row.get("indicator_name")
            or row.get("GHO (DISPLAY)")
        ),
        key = (row.get("indicator_code"), row.get("year"))
        if key in existing:
            continue  # skip duplicate rows


        indicator = DiseaseIndicator(
            disease_id=disease_id,
            indicator_code=(indicator_code),
            indicator_name=(indicator_name),
            year=row.get("year"),
            start_year=row.get("start_year"),
            end_year=row.get("end_year"),
            dimension_type=( dimension_type),
            dimension_code=( dimension_code),
            dimension_name=( dimension_name),
            numeric=row.get("numeric"),
            value=row.get("value"),
        )
        new_records.append(indicator)

    db.bulk_save_objects(new_records)
    db.commit()
    db.close()
    print(f"Loaded {len(new_records)} new indicators for {disease_name}")


def load_all_disease_files(folder_path: str):
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            disease_name = filename.split("_")[0].capitalize()
            file_path = os.path.join(folder_path, filename)
            print(f"Loading disease indicators for {disease_name} from {filename}")
            load_disease_indicators(file_path, disease_name)