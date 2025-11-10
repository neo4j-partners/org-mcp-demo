"""Neo4j Client for Aircraft Information Management.

This package provides a simple Python client for managing aircraft data
in a Neo4j database using the repository pattern and Pydantic models.
"""

from neo4j_client.connection import Neo4jConnection
from neo4j_client.exceptions import (
    Neo4jClientError,
    ConnectionError,
    QueryError,
    NotFoundError,
)
from neo4j_client.models import Aircraft, System, Component, Sensor, Flight, Airport
from neo4j_client.repository import AircraftRepository

__all__ = [
    "Neo4jConnection",
    "Neo4jClientError",
    "ConnectionError",
    "QueryError",
    "NotFoundError",
    "Aircraft",
    "System",
    "Component",
    "Sensor",
    "Flight",
    "Airport",
    "AircraftRepository",
]
