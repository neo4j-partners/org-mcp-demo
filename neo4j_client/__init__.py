"""Neo4j Python client library for aviation data."""

from .models import (
    Aircraft,
    Airport,
    Flight,
    Delay,
    MaintenanceEvent,
    System,
    Component,
    Sensor,
    Reading,
)
from .connection import Neo4jConnection
from .repository import (
    AircraftRepository,
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
    # Models
    "Aircraft",
    "Airport",
    "Flight",
    "Delay",
    "MaintenanceEvent",
    "System",
    "Component",
    "Sensor",
    "Reading",
    # Connection
    "Neo4jConnection",
    # Repositories
    "AircraftRepository",
    "FlightRepository",
    "MaintenanceEventRepository",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
