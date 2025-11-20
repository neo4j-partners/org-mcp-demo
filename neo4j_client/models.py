"""
Pydantic data models for the Aviation Neo4j database.

This module defines type-safe models for aircraft, airports, flights,
systems, components, sensors, maintenance events, and delays.
"""

from typing import Optional
from pydantic import BaseModel, Field


class Aircraft(BaseModel):
    """Represents a commercial aircraft in the fleet."""
    
    aircraft_id: str = Field(..., description="Unique aircraft identifier")
    tail_number: str = Field(..., description="Aircraft registration/tail number")
    icao24: str = Field(..., description="ICAO 24-bit address")
    model: str = Field(..., description="Aircraft model (e.g., Boeing 737-800)")
    operator: str = Field(..., description="Operating airline")
    manufacturer: str = Field(..., description="Aircraft manufacturer")


class Airport(BaseModel):
    """Represents an airport with location and identification codes."""
    
    airport_id: str = Field(..., description="Unique airport identifier")
    iata: str = Field(..., description="IATA airport code (e.g., LAX)")
    icao: str = Field(..., description="ICAO airport code (e.g., KLAX)")
    name: str = Field(..., description="Airport name")
    city: str = Field(..., description="City location")
    country: str = Field(..., description="Country location")
    lat: float = Field(..., description="Latitude coordinate")
    lon: float = Field(..., description="Longitude coordinate")


class Flight(BaseModel):
    """Represents a scheduled flight operation."""
    
    flight_id: str = Field(..., description="Unique flight identifier")
    flight_number: str = Field(..., description="Flight number (e.g., AA100)")
    aircraft_id: str = Field(..., description="ID of operating aircraft")
    operator: str = Field(..., description="Operating airline")
    origin: str = Field(..., description="Origin airport code")
    destination: str = Field(..., description="Destination airport code")
    scheduled_departure: str = Field(..., description="Scheduled departure time (ISO format)")
    scheduled_arrival: str = Field(..., description="Scheduled arrival time (ISO format)")


class System(BaseModel):
    """Represents a major aircraft system (e.g., hydraulics, avionics, engines)."""
    
    system_id: str = Field(..., description="Unique system identifier")
    aircraft_id: str = Field(..., description="Parent aircraft ID")
    name: str = Field(..., description="System name")
    type: str = Field(..., description="System type")


class Component(BaseModel):
    """Represents a component within an aircraft system."""
    
    component_id: str = Field(..., description="Unique component identifier")
    system_id: str = Field(..., description="Parent system ID")
    name: str = Field(..., description="Component name")
    type: str = Field(..., description="Component type")


class Sensor(BaseModel):
    """Represents a sensor that monitors a system or component."""
    
    sensor_id: str = Field(..., description="Unique sensor identifier")
    system_id: str = Field(..., description="Parent system ID")
    name: str = Field(..., description="Sensor name")
    type: str = Field(..., description="Sensor type")
    unit: str = Field(..., description="Measurement unit (e.g., celsius, psi)")


class Reading(BaseModel):
    """Represents a time-series sensor reading."""
    
    reading_id: str = Field(..., description="Unique reading identifier")
    sensor_id: str = Field(..., description="Parent sensor ID")
    timestamp: str = Field(..., description="Reading timestamp (ISO format)")
    value: float = Field(..., description="Sensor reading value")


class MaintenanceEvent(BaseModel):
    """Represents a maintenance event or fault report."""
    
    event_id: str = Field(..., description="Unique event identifier")
    aircraft_id: str = Field(..., description="Affected aircraft ID")
    system_id: str = Field(..., description="Affected system ID")
    component_id: str = Field(..., description="Affected component ID")
    fault: str = Field(..., description="Fault description")
    severity: str = Field(..., description="Severity level (e.g., CRITICAL, WARNING)")
    reported_at: str = Field(..., description="Event timestamp (ISO format)")
    corrective_action: str = Field(..., description="Action taken")


class Delay(BaseModel):
    """Represents a flight delay incident."""
    
    delay_id: str = Field(..., description="Unique delay identifier")
    flight_id: str = Field(..., description="Affected flight ID")
    cause: str = Field(..., description="Delay cause")
    minutes: int = Field(..., description="Delay duration in minutes")
