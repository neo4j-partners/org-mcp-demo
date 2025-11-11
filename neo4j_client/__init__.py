"""Neo4j Python client for airplane/aviation data."""

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
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    DelayRepository,
)

__version__ = "0.1.0"

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
    "AirportRepository",
    "FlightRepository",
    "MaintenanceEventRepository",
    "DelayRepository",
]
