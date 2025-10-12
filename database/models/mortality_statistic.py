from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db_connection import Base

class MortalityStatistic(Base):
    __tablename__ = "mortality_statistics"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, index=True)
    cause_id = Column(Integer, ForeignKey("causes_of_death.id"))
    geo_admin_unit_id = Column(Integer, ForeignKey("geo_admin_unit.id", ondelete="SET NULL"), nullable=True, index=True)
    year = Column(Integer, index=True)
    gender = Column(String, index=True)
    deaths = Column(Float, nullable=True)

    cause_obj = relationship("CauseOfDeath", back_populates="statistics")
    geo_admin_unit = relationship("GeoAdminUnit", back_populates="mortalities")