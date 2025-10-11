from sqlalchemy import Column, Integer, String, Date
from database.db_connection import Base

class OutbreakReport(Base):
    __tablename__ = "outbreak_reports"

    id = Column(Integer, primary_key=True, index=True)
    disease_name = Column(String, index=True)       # e.g., 'Cholera'
    country_name = Column(String, index=True)
    region = Column(String)
    country_code = Column(String, index=True)
    first_epiwk = Column(Date)
    last_epiwk = Column(Date)
    case_total = Column(Integer)
    death_total = Column(Integer)
