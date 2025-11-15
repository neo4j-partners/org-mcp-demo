"""Neo4j Python Client Library.

A high-quality Python client for Neo4j databases with:
- Pydantic models for type safety
- Repository pattern for clean query organization
- Parameterized Cypher queries for security
- Type hints throughout
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
    FlightRepository,
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
    "FlightRepository",
    "MaintenanceEventRepository",
    "AirportRepository",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
