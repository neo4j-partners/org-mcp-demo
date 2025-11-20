"""
Neo4j Aviation Client Library

A Python client library for querying the Aviation Neo4j database.
Provides repository pattern interfaces for aircraft, airports, flights,
components, and maintenance events.
"""

from .connection import Neo4jConnection
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
    AirportRepository,
    FlightRepository,
    ComponentRepository,
    MaintenanceEventRepository,
    SystemRepository,
)
from .exceptions import (
    Neo4jClientError,
    ConnectionError,
    QueryError,
    NotFoundError,
)

__version__ = "0.1.0"

__all__ = [
    # Connection
    "Neo4jConnection",
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
    "AirportRepository",
    "FlightRepository",
    "ComponentRepository",
    "MaintenanceEventRepository",
    "SystemRepository",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
