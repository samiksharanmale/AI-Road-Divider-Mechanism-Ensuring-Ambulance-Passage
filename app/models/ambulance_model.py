from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Ambulance(Base):
    """
    Represents an ambulance entity in the system.

    Attributes:
        id (int): Unique identifier for the ambulance record.
        ambulance_id (str): Unique ID assigned to the ambulance.
        current_location (str): Current location of the ambulance.
        destination (str): Destination location of the ambulance.
        status (str): Status of the ambulance (e.g., "Available", "On Duty").
        latitude (float): Current latitude of the ambulance.
        longitude (float): Current longitude of the ambulance.
        is_emergency (bool): Indicates whether the ambulance is in an emergency state.
        last_updated (datetime): Timestamp of the last update.
    """
    __tablename__ = 'ambulances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ambulance_id = Column(String(50), nullable=False, unique=True)
    current_location = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default="Available")  # "Available", "On Duty", etc.
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_emergency = Column(Boolean, default=False)
    last_updated = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (f"<Ambulance(id={self.id}, ambulance_id={self.ambulance_id}, "
                f"current_location={self.current_location}, status={self.status}, "
                f"is_emergency={self.is_emergency}, last_updated={self.last_updated})>")
