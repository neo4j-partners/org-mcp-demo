"""
Neo4j Aircraft Client - A Python client library for working with aircraft data in Neo4j.

This package provides a simple, type-safe interface for interacting with an aviation
database stored in Neo4j. It includes Pydantic models for data validation, repository
pattern for clean query organization, and parameterized Cypher queries for security.

Example:
    >>> from neo4j_aircraft_client import Neo4jConnection, AircraftRepository
    >>> 
    >>> # Connect to Neo4j
    >>> conn = Neo4jConnection("bolt://localhost:7687", "neo4j", "password")
    >>> 
    >>> # Use the repository pattern
    >>> with conn.session() as session:
    ...     aircraft_repo = AircraftRepository(session)
    ...     aircraft = aircraft_repo.find_by_tail_number("N12345")
    ...     print(aircraft.model)
    >>> 
    >>> conn.close()
"""

from .models import (
    Aircraft,
    Airport,
    Flight,
    System,
    Component,
    Sensor,
    MaintenanceEvent,
    Delay,
)
from .connection import Neo4jConnection
from .repository import (
    AircraftRepository,
    FlightRepository,
    AirportRepository,
    SystemRepository,
    MaintenanceEventRepository,
)
from .exceptions import (
    Neo4jClientError,
    ConnectionError,
    QueryError,
    NotFoundError,
)

__version__ = "0.1.0"

__all__ = [
    # Models
    "Aircraft",
    "Airport",
    "Flight",
    "System",
    "Component",
    "Sensor",
    "MaintenanceEvent",
    "Delay",
    # Connection
    "Neo4jConnection",
    # Repositories
    "AircraftRepository",
    "FlightRepository",
    "AirportRepository",
    "SystemRepository",
    "MaintenanceEventRepository",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
