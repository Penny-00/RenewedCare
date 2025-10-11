from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db_connection import Base

class DiseaseIndicator(Base):
    __tablename__ = "disease_indicators"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"))
    indicator_code = Column(String, index=True)
    indicator_name = Column(String)
    year = Column(Integer, index=True)
    start_year = Column(Integer)
    end_year = Column(Integer)
    sex_type = Column(String)
    sex_code = Column(String)
    sex_name = Column(String)
    numeric = Column(Float, nullable=True)
    value = Column(String, nullable=True)
    lower_bound = Column(Float, nullable=True)
    upper_bound = Column(Float, nullable=True)

    disease = relationship("Disease", back_populates="indicators")
