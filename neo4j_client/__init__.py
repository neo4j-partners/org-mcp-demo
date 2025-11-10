"""Neo4j Python Client for Airplane Information Management.

This package provides a clean, type-safe interface for managing airplane-related
data in a Neo4j database. It includes Pydantic models, repository patterns, and
connection management.
"""

from .models import Aircraft, Flight, Airport, MaintenanceEvent, Delay
from .connection import Neo4jConnection
from .repository import (
    AircraftRepository,
    FlightRepository,
    AirportRepository,
    MaintenanceEventRepository
)
from .exceptions import (
    Neo4jClientError,
    ConnectionError,
    QueryError,
    NotFoundError
)

__version__ = "0.1.0"

__all__ = [
    # Models
    "Aircraft",
    "Flight",
    "Airport",
    "MaintenanceEvent",
    "Delay",
    # Connection
    "Neo4jConnection",
    # Repositories
    "AircraftRepository",
    "FlightRepository",
    "AirportRepository",
    "MaintenanceEventRepository",
    # Exceptions
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
]
