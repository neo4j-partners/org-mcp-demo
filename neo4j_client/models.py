"""Pydantic models for Neo4j airplane entities."""

from typing import Optional
from pydantic import BaseModel, Field


class Aircraft(BaseModel):
    """Represents an aircraft in the fleet."""
    
    aircraft_id: str = Field(..., description="Unique identifier for the aircraft")
    tail_number: str = Field(..., description="Aircraft registration/tail number")
    manufacturer: str = Field(..., description="Aircraft manufacturer")
    model: str = Field(..., description="Aircraft model")
    operator: str = Field(..., description="Operating airline/company")
    icao24: Optional[str] = Field(None, description="ICAO 24-bit address")


class Flight(BaseModel):
    """Represents a flight operation."""
    
    flight_id: str = Field(..., description="Unique identifier for the flight")
    flight_number: str = Field(..., description="Flight number (e.g., UA123)")
    aircraft_id: str = Field(..., description="Aircraft operating this flight")
    operator: str = Field(..., description="Operating airline")
    origin: str = Field(..., description="Origin airport code")
    destination: str = Field(..., description="Destination airport code")
    scheduled_departure: str = Field(..., description="Scheduled departure time (ISO format)")
    scheduled_arrival: str = Field(..., description="Scheduled arrival time (ISO format)")


class Airport(BaseModel):
    """Represents an airport."""
    
    airport_id: str = Field(..., description="Unique identifier for the airport")
    name: str = Field(..., description="Airport name")
    iata: str = Field(..., description="IATA 3-letter code")
    icao: str = Field(..., description="ICAO 4-letter code")
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country name")
    lat: float = Field(..., description="Latitude coordinate")
    lon: float = Field(..., description="Longitude coordinate")


class MaintenanceEvent(BaseModel):
    """Represents a maintenance event for an aircraft."""
    
    event_id: str = Field(..., description="Unique identifier for the event")
    aircraft_id: str = Field(..., description="Aircraft affected by this event")
    system_id: Optional[str] = Field(None, description="System affected")
    component_id: Optional[str] = Field(None, description="Component affected")
    fault: str = Field(..., description="Fault description")
    severity: str = Field(..., description="Severity level")
    corrective_action: str = Field(..., description="Corrective action taken")
    reported_at: str = Field(..., description="When the event was reported (ISO format)")


class Delay(BaseModel):
    """Represents a flight delay."""
    
    delay_id: str = Field(..., description="Unique identifier for the delay")
    flight_id: str = Field(..., description="Flight affected by this delay")
    cause: str = Field(..., description="Delay cause")
    minutes: int = Field(..., description="Delay duration in minutes")
