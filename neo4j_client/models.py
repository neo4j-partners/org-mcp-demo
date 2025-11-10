"""Pydantic models for Neo4j entities."""

from typing import Optional
from pydantic import BaseModel, Field


class Aircraft(BaseModel):
    """Represents an aircraft in the system.
    
    Attributes:
        aircraft_id: Unique identifier for the aircraft
        tail_number: Aircraft registration/tail number
        icao24: ICAO 24-bit address
        model: Aircraft model (e.g., B737-800, A320-200)
        operator: Airline or operator name
        manufacturer: Aircraft manufacturer (e.g., Boeing, Airbus)
    """
    
    aircraft_id: str = Field(..., description="Unique identifier for the aircraft")
    tail_number: str = Field(..., description="Aircraft registration/tail number")
    icao24: str = Field(..., description="ICAO 24-bit address")
    model: str = Field(..., description="Aircraft model")
    operator: str = Field(..., description="Airline or operator name")
    manufacturer: str = Field(..., description="Aircraft manufacturer")


class System(BaseModel):
    """Represents an aircraft system.
    
    Attributes:
        system_id: Unique identifier for the system
        aircraft_id: ID of the aircraft this system belongs to
        name: System name
        type: System type/category
    """
    
    system_id: str = Field(..., description="Unique identifier for the system")
    aircraft_id: str = Field(..., description="ID of the aircraft")
    name: str = Field(..., description="System name")
    type: str = Field(..., description="System type")


class Component(BaseModel):
    """Represents a component within an aircraft system.
    
    Attributes:
        component_id: Unique identifier for the component
        system_id: ID of the system this component belongs to
        name: Component name
        type: Component type/category
    """
    
    component_id: str = Field(..., description="Unique identifier for the component")
    system_id: str = Field(..., description="ID of the system")
    name: str = Field(..., description="Component name")
    type: str = Field(..., description="Component type")


class Sensor(BaseModel):
    """Represents a sensor within an aircraft system.
    
    Attributes:
        sensor_id: Unique identifier for the sensor
        system_id: ID of the system this sensor belongs to
        name: Sensor name
        type: Sensor type
        unit: Unit of measurement
    """
    
    sensor_id: str = Field(..., description="Unique identifier for the sensor")
    system_id: str = Field(..., description="ID of the system")
    name: str = Field(..., description="Sensor name")
    type: str = Field(..., description="Sensor type")
    unit: str = Field(..., description="Unit of measurement")


class Flight(BaseModel):
    """Represents a flight operation.
    
    Attributes:
        flight_id: Unique identifier for the flight
        flight_number: Flight number
        aircraft_id: ID of the aircraft operating this flight
        operator: Airline operator
        origin: Origin airport code
        destination: Destination airport code
        scheduled_departure: Scheduled departure time
        scheduled_arrival: Scheduled arrival time
    """
    
    flight_id: str = Field(..., description="Unique identifier for the flight")
    flight_number: str = Field(..., description="Flight number")
    aircraft_id: str = Field(..., description="ID of the aircraft")
    operator: str = Field(..., description="Airline operator")
    origin: str = Field(..., description="Origin airport code")
    destination: str = Field(..., description="Destination airport code")
    scheduled_departure: str = Field(..., description="Scheduled departure time")
    scheduled_arrival: str = Field(..., description="Scheduled arrival time")


class Airport(BaseModel):
    """Represents an airport.
    
    Attributes:
        airport_id: Unique identifier for the airport
        iata: IATA airport code
        icao: ICAO airport code
        name: Airport name
        city: City name
        country: Country name
        lat: Latitude coordinate
        lon: Longitude coordinate
    """
    
    airport_id: str = Field(..., description="Unique identifier for the airport")
    iata: str = Field(..., description="IATA airport code")
    icao: str = Field(..., description="ICAO airport code")
    name: str = Field(..., description="Airport name")
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country name")
    lat: float = Field(..., description="Latitude coordinate")
    lon: float = Field(..., description="Longitude coordinate")
