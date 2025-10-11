from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db_connection import Base

class CauseOfDeath(Base):
    __tablename__ = "causes_of_death"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    statistics = relationship("MortalityStatistic", back_populates="cause_obj")
