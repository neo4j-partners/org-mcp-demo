"""Neo4j Aircraft Data Client."""

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
from .connection import Neo4jConnection
from .repository import (
    AircraftRepository,
    FlightRepository,
    SystemRepository,
    MaintenanceEventRepository,
    AirportRepository,
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
    "Reading",
    "MaintenanceEvent",
    "Delay",
    # Connection
    "Neo4jConnection",
    # Repositories
    "AircraftRepository",
    "FlightRepository",
    "SystemRepository",
    "MaintenanceEventRepository",
    "AirportRepository",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
