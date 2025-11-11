"""Pydantic data models for Neo4j aviation database entities."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Aircraft(BaseModel):
    """Represents an aircraft in the database."""
    
    aircraft_id: str = Field(..., description="Unique identifier for the aircraft")
    tail_number: str = Field(..., description="Aircraft tail number/registration")
    icao24: str = Field(..., description="ICAO 24-bit address")
    model: str = Field(..., description="Aircraft model")
    operator: str = Field(..., description="Operating airline/company")
    manufacturer: str = Field(..., description="Aircraft manufacturer")


class Airport(BaseModel):
    """Represents an airport in the database."""
    
    airport_id: str = Field(..., description="Unique identifier for the airport")
    iata: str = Field(..., description="IATA airport code")
    icao: str = Field(..., description="ICAO airport code")
    name: str = Field(..., description="Airport name")
    city: str = Field(..., description="City where airport is located")
    country: str = Field(..., description="Country where airport is located")
    lat: float = Field(..., description="Latitude coordinate")
    lon: float = Field(..., description="Longitude coordinate")


class Flight(BaseModel):
    """Represents a flight in the database."""
    
    flight_id: str = Field(..., description="Unique identifier for the flight")
    flight_number: str = Field(..., description="Flight number")
    aircraft_id: str = Field(..., description="ID of aircraft operating this flight")
    operator: str = Field(..., description="Operating airline")
    origin: str = Field(..., description="Origin airport code")
    destination: str = Field(..., description="Destination airport code")
    scheduled_departure: str = Field(..., description="Scheduled departure time")
    scheduled_arrival: str = Field(..., description="Scheduled arrival time")


class System(BaseModel):
    """Represents an aircraft system in the database."""
    
    system_id: str = Field(..., description="Unique identifier for the system")
    aircraft_id: str = Field(..., description="ID of aircraft this system belongs to")
    name: str = Field(..., description="System name")
    type: str = Field(..., description="System type")


class Component(BaseModel):
    """Represents a component within an aircraft system."""
    
    component_id: str = Field(..., description="Unique identifier for the component")
    system_id: str = Field(..., description="ID of system this component belongs to")
    name: str = Field(..., description="Component name")
    type: str = Field(..., description="Component type")


class Sensor(BaseModel):
    """Represents a sensor within an aircraft system."""
    
    sensor_id: str = Field(..., description="Unique identifier for the sensor")
    system_id: str = Field(..., description="ID of system this sensor belongs to")
    name: str = Field(..., description="Sensor name")
    type: str = Field(..., description="Sensor type")
    unit: str = Field(..., description="Measurement unit")


class Reading(BaseModel):
    """Represents a sensor reading."""
    
    reading_id: str = Field(..., description="Unique identifier for the reading")
    sensor_id: str = Field(..., description="ID of sensor that took this reading")
    timestamp: str = Field(..., description="When the reading was taken")
    value: float = Field(..., description="Sensor reading value")


class MaintenanceEvent(BaseModel):
    """Represents a maintenance event for an aircraft."""
    
    event_id: str = Field(..., description="Unique identifier for the event")
    aircraft_id: str = Field(..., description="ID of affected aircraft")
    system_id: str = Field(..., description="ID of affected system")
    component_id: str = Field(..., description="ID of affected component")
    fault: str = Field(..., description="Description of the fault")
    severity: str = Field(..., description="Severity level of the fault")
    reported_at: str = Field(..., description="When the event was reported")
    corrective_action: str = Field(..., description="Action taken to correct the issue")


class Delay(BaseModel):
    """Represents a flight delay."""
    
    delay_id: str = Field(..., description="Unique identifier for the delay")
    flight_id: str = Field(..., description="ID of affected flight")
    cause: str = Field(..., description="Cause of the delay")
    minutes: int = Field(..., description="Duration of delay in minutes")
