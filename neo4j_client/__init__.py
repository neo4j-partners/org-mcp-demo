"""Neo4j Aviation Database Client Library.

A simple, well-structured Python client for the Neo4j aviation database.
"""

from neo4j_client.connection import Neo4jConnection
from neo4j_client.exceptions import (
    Neo4jClientError,
    ConnectionError,
    QueryError,
    NotFoundError,
)
from neo4j_client.models import (
    Aircraft,
    Airport,
    Flight,
    System,
    Component,
    Sensor,
    MaintenanceEvent,
    Delay,
)
from neo4j_client.repository import (
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    SystemRepository,
    ComponentRepository,
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
    "MaintenanceEvent",
    "Delay",
    # Repositories
    "AircraftRepository",
    "AirportRepository",
    "FlightRepository",
    "SystemRepository",
    "ComponentRepository",
    "MaintenanceEventRepository",
    "DelayRepository",
]
