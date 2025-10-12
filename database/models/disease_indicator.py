from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db_connection import Base

class DiseaseIndicator(Base):
    __tablename__ = "disease_indicators"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"))
    geo_admin_unit_id = Column(Integer, ForeignKey("geo_admin_unit.id", ondelete="SET NULL"), nullable=True, index=True)
    indicator_code = Column(String, index=True)
    indicator_name = Column(String)
    year = Column(Integer, index=True)
    start_year = Column(Integer)
    end_year = Column(Integer)
    dimension_type = Column(String)
    dimension_code = Column(String)
    dimension_name = Column(String)
    numeric = Column(Float, nullable=True)
    value = Column(String, nullable=True)

    disease = relationship("Disease", back_populates="indicators")
    geo_admin_unit = relationship("GeoAdminUnit", back_populates="indicators")
