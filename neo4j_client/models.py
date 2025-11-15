"""Pydantic models for Neo4j entities."""

from typing import Optional
from pydantic import BaseModel, Field


class Aircraft(BaseModel):
    """Represents a commercial aircraft in the fleet.
    
    Properties:
        aircraft_id: Unique identifier
        tail_number: Aircraft registration/tail number
        icao24: ICAO 24-bit address
        model: Aircraft model (e.g., "Boeing 737-800")
        operator: Operating airline
        manufacturer: Aircraft manufacturer
    """
    aircraft_id: str
    tail_number: str
    icao24: str
    model: str
    operator: str
    manufacturer: str


class Airport(BaseModel):
    """Represents an airport with location and identification codes.
    
    Properties:
        airport_id: Unique identifier
        iata: IATA airport code (e.g., "LAX")
        icao: ICAO airport code (e.g., "KLAX")
        name: Airport name
        city: City location
        country: Country location
        lat: Latitude coordinate
        lon: Longitude coordinate
    """
    airport_id: str
    iata: str
    icao: str
    name: str
    city: str
    country: str
    lat: float
    lon: float


class Flight(BaseModel):
    """Represents a scheduled flight operation.
    
    Properties:
        flight_id: Unique identifier
        flight_number: Flight number (e.g., "AA100")
        aircraft_id: ID of operating aircraft
        operator: Operating airline
        origin: Origin airport code
        destination: Destination airport code
        scheduled_departure: Scheduled departure time (ISO format)
        scheduled_arrival: Scheduled arrival time (ISO format)
    """
    flight_id: str
    flight_number: str
    aircraft_id: str
    operator: str
    origin: str
    destination: str
    scheduled_departure: str
    scheduled_arrival: str


class System(BaseModel):
    """Represents a major aircraft system (e.g., hydraulics, avionics, engines).
    
    Properties:
        system_id: Unique identifier
        aircraft_id: Parent aircraft ID
        name: System name
        type: System type
    """
    system_id: str
    aircraft_id: str
    name: str
    type: str


class Component(BaseModel):
    """Represents a component within an aircraft system.
    
    Properties:
        component_id: Unique identifier
        system_id: Parent system ID
        name: Component name
        type: Component type
    """
    component_id: str
    system_id: str
    name: str
    type: str


class Sensor(BaseModel):
    """Represents a sensor that monitors a system or component.
    
    Properties:
        sensor_id: Unique identifier
        system_id: Parent system ID
        name: Sensor name
        type: Sensor type
        unit: Measurement unit (e.g., "celsius", "psi")
    """
    sensor_id: str
    system_id: str
    name: str
    type: str
    unit: str


class Reading(BaseModel):
    """Represents a time-series sensor reading.
    
    Properties:
        reading_id: Unique identifier
        sensor_id: Parent sensor ID
        timestamp: Reading timestamp (ISO format)
        value: Sensor reading value
    """
    reading_id: str
    sensor_id: str
    timestamp: str
    value: float


class MaintenanceEvent(BaseModel):
    """Represents a maintenance event or fault report.
    
    Properties:
        event_id: Unique identifier
        aircraft_id: Affected aircraft ID
        system_id: Affected system ID
        component_id: Affected component ID
        fault: Fault description
        severity: Severity level (e.g., "CRITICAL", "WARNING")
        reported_at: Event timestamp (ISO format)
        corrective_action: Action taken
    """
    event_id: str
    aircraft_id: str
    system_id: str
    component_id: str
    fault: str
    severity: str
    reported_at: str
    corrective_action: str


class Delay(BaseModel):
    """Represents a flight delay incident.
    
    Properties:
        delay_id: Unique identifier
        flight_id: Affected flight ID
        cause: Delay cause
        minutes: Delay duration in minutes
    """
    delay_id: str
    flight_id: str
    cause: str
    minutes: int
