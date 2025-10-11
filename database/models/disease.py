from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db_connection import Base

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # e.g., Tuberculosis, Cholera

    indicators = relationship("DiseaseIndicator", back_populates="disease")
