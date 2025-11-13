"""Neo4j Aircraft Client - Python client for working with aircraft data in Neo4j.

This package provides a clean, type-safe interface for working with aviation
data stored in Neo4j, including aircraft, flights, maintenance events, and more.

Example:
    >>> from neo4j_client import Neo4jConnection, AircraftRepository
    >>> 
    >>> with Neo4jConnection(uri, username, password) as conn:
    ...     session = conn.get_session()
    ...     aircraft_repo = AircraftRepository(session)
    ...     aircraft = aircraft_repo.find_by_tail_number("N12345")
"""

from .connection import Neo4jConnection
from .exceptions import (
    Neo4jClientError,
    ConnectionError,
    QueryError,
    NotFoundError,
)
from .models import (
    Aircraft,
    Airport,
    Flight,
    System,
    Component,
    Sensor,
    Reading,
    MaintenanceEvent,
    Delay,
)
from .repository import (
    AircraftRepository,
    FlightRepository,
    MaintenanceEventRepository,
    SystemRepository,
    AirportRepository,
)

__all__ = [
    # Connection
    "Neo4jConnection",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
    # Models
    "Aircraft",
    "Airport",
    "Flight",
    "System",
    "Component",
    "Sensor",
    "Reading",
    "MaintenanceEvent",
    "Delay",
    # Repositories
    "AircraftRepository",
    "FlightRepository",
    "MaintenanceEventRepository",
    "SystemRepository",
    "AirportRepository",
]
