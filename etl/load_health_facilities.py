import os
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models.health_facilities import HealthFacility  # adjust import path
from database.models.geo_unit import GeoAdminUnit 
from database.db_connection import SessionLocal

# 🧠 Helper — safe string and number conversions
def safe_str(value):
    if pd.isna(value):
        return None
    return str(value).strip()

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def safe_datetime(value):
    dt = pd.to_datetime(value, errors="coerce")
    return None if pd.isna(dt) else dt


def get_or_create_geo_unit(db: Session, state_name, lga_name=None, ward_name=None,
                           ward_code=None, latitude=None, longitude=None):
    """Ensures unique geo hierarchy row and returns its id."""
    query = (
        db.query(GeoAdminUnit)
        .filter(
            GeoAdminUnit.state_name == state_name,
            GeoAdminUnit.lga_name == lga_name,
            GeoAdminUnit.ward_name == ward_name,
        )
    )
    geo = query.first()
    if not geo:
        geo = GeoAdminUnit(
            state_name=state_name,
            lga_name=lga_name,
            ward_name=ward_name,
            adm_level=3 if ward_name else 2 if lga_name else 1,
            latitude=latitude,
            longitude=longitude,
        )
        db.add(geo)
        db.flush()  # get ID
    return geo.geo_admin_unit_id


def load_health_facilities(csv_path: str, source_name: str):
    df = pd.read_csv(csv_path)
    db = SessionLocal()

    new_records = []
    for _, row in df.iterrows():
        # Normalize cross-dataset fields
        facility_name = (
            row.get("properties_name")
            or row.get("prmry_name")
            or row.get("facility_name")
        )
        facility_type = (
            row.get("properties_type")
            or row.get("type")
            or row.get("facility_type")
        )
        functional_status = (
            row.get("properties_functional_status")
            or row.get("func_stats")
        )
        category = (
            row.get("properties_category")
            or row.get("category")
        )
        lga_name = (
            row.get("properties_lga_name")
            or row.get("lga_name")
        )
        ward_name = (
            row.get("properties_ward_name")
            or row.get("ward_name")
        )
        ward_code = (
            row.get("properties_ward_code")
            or row.get("ward_code")
        )
        state_name = (
            row.get("properties_state_name")
            or row.get("state_name")
        )
        state_code = (
            row.get("properties_state_code")
            or row.get("state_code")
        )

        # Extract coordinates
        latitude = safe_float(row.get("latitude") or None)
        longitude = safe_float(row.get("longitude") or None)
        geo_coordinate = safe_float(row.get("geometry_coordinates"))

        # Get or create geo reference
        geo_id = get_or_create_geo_unit(
            db,
            state_name=safe_str(state_name),
            lga_name=safe_str(lga_name),
            ward_name=safe_str(ward_name),
            ward_code=safe_str(ward_code),
            latitude=latitude,
            longitude=longitude,
        )

        facility = HealthFacility(
            facility_name=safe_str(facility_name),
            facility_type=safe_str(facility_type),
            category=safe_str(category),
            ownership=safe_str(row.get("ownership")),
            functional_status=safe_str(functional_status),
            geo_admin_unit_id=geo_id,
            latitude=latitude,
            longitude=longitude,
            geometry_type=safe_str(row.get("geometry_type")),
            geometry_name=safe_str(row.get("geometry_name")),
        )

        new_records.append(facility)

    db.bulk_save_objects(new_records)
    db.commit()
    db.close()
    print(f"✅ Loaded {len(new_records)} facilities from {source_name}")



def load_all_facility_files(folder_path: str):
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            source_name = filename.split("_")[0].capitalize()
            file_path = os.path.join(folder_path, filename)
            print(f"Loading disease indicators for {source_name} from {filename}")
            load_health_facilities(file_path, source_name)
