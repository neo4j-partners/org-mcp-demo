"""Pydantic data models for Neo4j entities."""

from typing import Optional
from pydantic import BaseModel, Field


class Aircraft(BaseModel):
    """Represents an aircraft entity in the Neo4j database."""
    
    aircraft_id: str
    tail_number: str
    icao24: str
    model: str
    operator: str
    manufacturer: str


class Airport(BaseModel):
    """Represents an airport entity in the Neo4j database."""
    
    airport_id: str
    name: str
    iata: str
    icao: str
    city: str
    country: str
    lat: float
    lon: float


class Flight(BaseModel):
    """Represents a flight entity in the Neo4j database."""
    
    flight_id: str
    flight_number: str
    aircraft_id: str
    operator: str
    origin: str
    destination: str
    scheduled_departure: str
    scheduled_arrival: str


class Delay(BaseModel):
    """Represents a flight delay entity in the Neo4j database."""
    
    delay_id: str
    flight_id: str
    cause: str
    minutes: int


class MaintenanceEvent(BaseModel):
    """Represents a maintenance event entity in the Neo4j database."""
    
    event_id: str
    aircraft_id: str
    system_id: str
    component_id: str
    fault: str
    severity: str
    corrective_action: str
    reported_at: str


class System(BaseModel):
    """Represents an aircraft system entity in the Neo4j database."""
    
    system_id: str
    aircraft_id: str
    name: str
    type: str


class Component(BaseModel):
    """Represents a system component entity in the Neo4j database."""
    
    component_id: str
    system_id: str
    name: str
    type: str


class Sensor(BaseModel):
    """Represents a sensor entity in the Neo4j database."""
    
    sensor_id: str
    system_id: str
    name: str
    type: str
    unit: str


class Reading(BaseModel):
    """Represents a sensor reading entity in the Neo4j database."""
    
    reading_id: str
    sensor_id: str
    timestamp: str
    value: float
