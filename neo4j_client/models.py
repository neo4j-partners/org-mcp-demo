"""Pydantic models for Neo4j aircraft data entities."""

from typing import Optional
from pydantic import BaseModel, Field


class Aircraft(BaseModel):
    """Represents a commercial aircraft in the fleet.
    
    Attributes:
        aircraft_id: Unique identifier for the aircraft
        tail_number: Aircraft registration/tail number
        icao24: ICAO 24-bit address
        model: Aircraft model (e.g., "Boeing 737-800")
        operator: Operating airline
        manufacturer: Aircraft manufacturer
    """
    aircraft_id: str = Field(..., description="Unique identifier")
    tail_number: str = Field(..., description="Aircraft registration/tail number")
    icao24: str = Field(..., description="ICAO 24-bit address")
    model: str = Field(..., description="Aircraft model")
    operator: str = Field(..., description="Operating airline")
    manufacturer: str = Field(..., description="Aircraft manufacturer")


class Airport(BaseModel):
    """Represents an airport with location and identification codes.
    
    Attributes:
        airport_id: Unique identifier for the airport
        iata: IATA airport code (e.g., "LAX")
        icao: ICAO airport code (e.g., "KLAX")
        name: Airport name
        city: City location
        country: Country location
        lat: Latitude coordinate
        lon: Longitude coordinate
    """
    airport_id: str = Field(..., description="Unique identifier")
    iata: str = Field(..., description="IATA airport code")
    icao: str = Field(..., description="ICAO airport code")
    name: str = Field(..., description="Airport name")
    city: str = Field(..., description="City location")
    country: str = Field(..., description="Country location")
    lat: float = Field(..., description="Latitude coordinate")
    lon: float = Field(..., description="Longitude coordinate")


class Flight(BaseModel):
    """Represents a scheduled flight operation.
    
    Attributes:
        flight_id: Unique identifier for the flight
        flight_number: Flight number (e.g., "AA100")
        aircraft_id: ID of operating aircraft
        operator: Operating airline
        origin: Origin airport code
        destination: Destination airport code
        scheduled_departure: Scheduled departure time (ISO format)
        scheduled_arrival: Scheduled arrival time (ISO format)
    """
    flight_id: str = Field(..., description="Unique identifier")
    flight_number: str = Field(..., description="Flight number")
    aircraft_id: str = Field(..., description="ID of operating aircraft")
    operator: str = Field(..., description="Operating airline")
    origin: str = Field(..., description="Origin airport code")
    destination: str = Field(..., description="Destination airport code")
    scheduled_departure: str = Field(..., description="Scheduled departure time (ISO format)")
    scheduled_arrival: str = Field(..., description="Scheduled arrival time (ISO format)")


class System(BaseModel):
    """Represents a major aircraft system (e.g., hydraulics, avionics, engines).
    
    Attributes:
        system_id: Unique identifier for the system
        aircraft_id: Parent aircraft ID
        name: System name
        type: System type
    """
    system_id: str = Field(..., description="Unique identifier")
    aircraft_id: str = Field(..., description="Parent aircraft ID")
    name: str = Field(..., description="System name")
    type: str = Field(..., description="System type")


class Component(BaseModel):
    """Represents a component within an aircraft system.
    
    Attributes:
        component_id: Unique identifier for the component
        system_id: Parent system ID
        name: Component name
        type: Component type
    """
    component_id: str = Field(..., description="Unique identifier")
    system_id: str = Field(..., description="Parent system ID")
    name: str = Field(..., description="Component name")
    type: str = Field(..., description="Component type")


class Sensor(BaseModel):
    """Represents a sensor that monitors a system or component.
    
    Attributes:
        sensor_id: Unique identifier for the sensor
        system_id: Parent system ID
        name: Sensor name
        type: Sensor type
        unit: Measurement unit (e.g., "celsius", "psi")
    """
    sensor_id: str = Field(..., description="Unique identifier")
    system_id: str = Field(..., description="Parent system ID")
    name: str = Field(..., description="Sensor name")
    type: str = Field(..., description="Sensor type")
    unit: str = Field(..., description="Measurement unit")


class Reading(BaseModel):
    """Represents a time-series sensor reading.
    
    Attributes:
        reading_id: Unique identifier for the reading
        sensor_id: Parent sensor ID
        timestamp: Reading timestamp (ISO format)
        value: Sensor reading value
    """
    reading_id: str = Field(..., description="Unique identifier")
    sensor_id: str = Field(..., description="Parent sensor ID")
    timestamp: str = Field(..., description="Reading timestamp (ISO format)")
    value: float = Field(..., description="Sensor reading value")


class MaintenanceEvent(BaseModel):
    """Represents a maintenance event or fault report.
    
    Attributes:
        event_id: Unique identifier for the event
        aircraft_id: Affected aircraft ID
        system_id: Affected system ID
        component_id: Affected component ID
        fault: Fault description
        severity: Severity level (e.g., "CRITICAL", "WARNING")
        reported_at: Event timestamp (ISO format)
        corrective_action: Action taken
    """
    event_id: str = Field(..., description="Unique identifier")
    aircraft_id: str = Field(..., description="Affected aircraft ID")
    system_id: str = Field(..., description="Affected system ID")
    component_id: str = Field(..., description="Affected component ID")
    fault: str = Field(..., description="Fault description")
    severity: str = Field(..., description="Severity level")
    reported_at: str = Field(..., description="Event timestamp (ISO format)")
    corrective_action: str = Field(..., description="Action taken")


class Delay(BaseModel):
    """Represents a flight delay incident.
    
    Attributes:
        delay_id: Unique identifier for the delay
        flight_id: Affected flight ID
        cause: Delay cause
        minutes: Delay duration in minutes
    """
    delay_id: str = Field(..., description="Unique identifier")
    flight_id: str = Field(..., description="Affected flight ID")
    cause: str = Field(..., description="Delay cause")
    minutes: int = Field(..., description="Delay duration in minutes")
