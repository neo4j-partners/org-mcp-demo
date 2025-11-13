"""Neo4j Aircraft Data Client Library.

A simple Python client for working with aircraft data in Neo4j databases.
Provides Pydantic models, repository pattern for queries, and connection management.
"""

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
    SystemRepository,
    MaintenanceEventRepository,
    SensorRepository,
    AirportRepository,
)
from .connection import Neo4jConnection
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
    "Reading",
    "MaintenanceEvent",
    "Delay",
    # Repositories
    "AircraftRepository",
    "FlightRepository",
    "SystemRepository",
    "MaintenanceEventRepository",
    "SensorRepository",
    "AirportRepository",
    # Connection
    "Neo4jConnection",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
