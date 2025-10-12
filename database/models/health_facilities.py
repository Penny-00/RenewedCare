from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Index,
    Text,
    JSON,
    ForeignKey
)
from database.db_connection import Base
from sqlalchemy.orm import declarative_base, relationship


class HealthFacility(Base):
    """
    Master facility table (merged GRID3 + NHFR).
    """
    __tablename__ = "health_facilities_master"
    facility_id = Column(Integer, primary_key=True, autoincrement=True)
    facility_name = Column(Text, nullable=False, index=True)
    facility_type = Column(String(64), nullable=True)  # Primary, Secondary, Tertiary
    category = Column(String(128), nullable=True)  # Dispensary, PHC, Hospital, etc.
    ownership = Column(String(128), nullable=True)  # Public, Private, NGO, etc.
    functional_status = Column(String(64), nullable=True)  # Functional, Not Functional, Partially

    geo_admin_unit_id = Column(Integer, ForeignKey("geo_admin_unit.id", ondelete="SET NULL"), nullable=True, index=True)
    latitude = Column(Float, nullable=True, index=True)
    longitude = Column(Float, nullable=True, index=True)

    properties = Column(JSON, nullable=True)  # raw properties JSON if you want to keep original row

    # relationships
    geo_admin_unit = relationship("GeoAdminUnit", back_populates="facilities")

    #__table_args__ = (
     #   Index("ix_facility_name_state_lga", "facility_name", "latitude", "longitude"),
    #)

    #def __repr__(self):
     #   return f"<Facility(id={self.facility_id} name={self.facility_name} global_id={self.global_id})>"
