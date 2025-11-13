"""Neo4j Python Client Library for Aviation Database.

This package provides a clean, type-safe interface to the Neo4j aviation database
using Pydantic models and the repository pattern.
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
    "MaintenanceEventRepository",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
