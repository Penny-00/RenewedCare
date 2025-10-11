import os
import pandas as pd
from sqlalchemy.orm import Session
from database.models.outbreak_reports import OutbreakReport
from database.db_connection import SessionLocal


def safe_datetime(value):
    dt = pd.to_datetime(value, errors="coerce")
    return None if pd.isna(dt) else dt

def load_outbreak_reports(csv_path: str, disease_name: str):
    df = pd.read_csv(csv_path)
    db = SessionLocal()

    # 🧹 Clear previous records
    #db.execute("TRUNCATE TABLE outbreak_reports RESTART IDENTITY CASCADE;")
    #db.commit()

    new_records = []
    for _, row in df.iterrows():
        new_records.append(
            OutbreakReport(
                disease_name=disease_name,
                country_name=row.get("country_name"),
                region=row.get("region"),
                country_code=row.get("country_code"),
                first_epiwk=safe_datetime(row.get("first_epiwk")),
                last_epiwk=safe_datetime(row.get("last_epiwk")),
                case_total=int(row.get("case_total")) if pd.notna(row.get("case_total")) else None,
                death_total=int(row.get("death_total")) if pd.notna(row.get("death_total")) else None,
            )
        )

    db.bulk_save_objects(new_records)
    db.commit()
    db.close()
    print(f"✅ Loaded outbreak reports for {disease_name}")


def load_all_outbreak_files(folder_path: str):
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            disease_name = filename.split("_")[0].capitalize()
            file_path = os.path.join(folder_path, filename)
            print(f"Loading outbreak data for {disease_name} from {filename}")
            load_outbreak_reports(file_path, disease_name)