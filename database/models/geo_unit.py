from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Index,
)
from database.db_connection import Base
from sqlalchemy.orm import declarative_base, relationship

# If you plan to use PostGIS spatial types, uncomment the next import and use Geometry in geo columns
# from geoalchemy2 import Geometery



class GeoAdminUnit(Base):
    """
    Geographic administrative unit (country/state/LGA/ward).
    adm_level: 0 = country, 1 = state, 2 = LGA, 3 = ward
    """
    __tablename__ = "geo_admin_unit"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_code = Column(String(8), nullable=False, default="NGA", index=True)
    state_name = Column(String(128), nullable=True, index=True)
    lga_name = Column(String(128), nullable=True, index=True)
    ward_name = Column(String(128), nullable=True)
    adm_level = Column(Integer, nullable=False, default=0)  # 0 country, 1 state, 2 lga, 3 ward
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    # If using PostGIS, consider:
   #geometry = Column(Geometry("POINT", srid=4326), nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # relationships
    facilities = relationship("HealthFacility", back_populates="geo_admin_unit", lazy="select")
    indicators = relationship("DiseaseIndicator", back_populates="geo_admin_unit", lazy="select")
    mortalities = relationship("MortalityStatistic", back_populates="geo_admin_unit", lazy="select")

    #__table_args__ = (
    #    Index("ix_geo_country_state_lga", "country_code", "state_name", "lga_name"),
    #)

    #def __repr__(self):
     #   return f"<GeoAdminUnit(id={self.geo_admin_unit_id} country={self.country_code} state={self.state_name} lga={self.lga_name})>"
