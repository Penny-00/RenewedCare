import os
import pandas as pd
from sqlalchemy.orm import Session
from database.models.causes_of_death import CauseOfDeath
from database.models.mortality_statistic import MortalityStatistic
from database.db_connection import SessionLocal

def load_mortality_data(csv_path: str, gender: str):
    df = pd.read_csv(csv_path)
    db = SessionLocal()

        # 🧹 Clear previous records
    #db.execute("TRUNCATE TABLE outbreak_reports RESTART IDENTITY CASCADE;")
    #db.commit()
    
    # Cache known causes
    known_causes = {c.name: c.id for c in db.query(CauseOfDeath).all()}

    # Cache existing records for idempotency
    existing = set(
        (m.country, m.cause_id, m.year, m.gender)
        for m in db.query(MortalityStatistic.country,
                          MortalityStatistic.cause_id,
                          MortalityStatistic.year,
                          MortalityStatistic.gender).all()
    )

    new_records = []
    for _, row in df.iterrows():
        cause_name = row.get("diseases") or row.get("cause")
        if not cause_name:
            continue

        if cause_name not in known_causes:
            cause = CauseOfDeath(name=cause_name)
            db.add(cause)
            db.commit()
            db.refresh(cause)
            known_causes[cause_name] = cause.id

        cause_id = known_causes[cause_name]
        key = (row.get("country_code"), cause_id, row.get("year"), gender)
        if key in existing:
            continue

        stat = MortalityStatistic(
            country=row.get("country_code"),
            cause_id=cause_id,
            year=row.get("year"),
            gender=gender,
            deaths=row.get("death_rate"),
        )
        new_records.append(stat)

    db.bulk_save_objects(new_records)
    db.commit()
    db.close()
    print(f"Loaded {len(new_records)} new mortality records for gender={gender}")


def load_all_mortality_files(folder_path: str):
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            if "mle" in filename.upper():
                gender = "MLE"
            elif "fmle" in filename.upper():
                gender = "FMLE"
            else:
                gender = "BTSX"
            file_path = os.path.join(folder_path, filename)
            print(f"Loading mortality data ({gender}) from {filename}")
            load_mortality_data(file_path, gender)
