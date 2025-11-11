"""Neo4j Python client for aviation database.

A simple, high-quality Python client library for interacting with a Neo4j
aviation/aircraft maintenance database.
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
    AirportRepository,
    FlightRepository,
    SystemRepository,
    SensorRepository,
    ReadingRepository,
    MaintenanceEventRepository,
    DelayRepository,
)
from .connection import Neo4jConnection
from .exceptions import (
    Neo4jClientError,
    ConnectionError,
    QueryError,
    NotFoundError,
    ValidationError,
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
    "AirportRepository",
    "FlightRepository",
    "SystemRepository",
    "SensorRepository",
    "ReadingRepository",
    "MaintenanceEventRepository",
    "DelayRepository",
    # Connection
    "Neo4jConnection",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
    "ValidationError",
]
