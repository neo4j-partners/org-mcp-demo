"""Pytest fixtures for Neo4j client tests."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client.connection import Neo4jConnection
from neo4j_client.repository import (
    AircraftRepository,
    FlightRepository,
    SystemRepository,
    MaintenanceEventRepository,
    AirportRepository,
)


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j test container for the entire test session."""
    container = Neo4jContainer("neo4j:5.14")
    container.start()
    yield container
    container.stop()


@pytest.fixture(scope="session")
def neo4j_connection(neo4j_container):
    """Provide a Neo4j connection for the test session."""
    uri = neo4j_container.get_connection_url()
    # Neo4j testcontainer password attribute
    connection = Neo4jConnection(
        uri=uri,
        username="neo4j",
        password=neo4j_container.password,
        database="neo4j"
    )
    connection.connect()
    yield connection
    connection.close()


@pytest.fixture
def session(neo4j_connection):
    """Provide a fresh Neo4j session for each test."""
    session = neo4j_connection.get_session()
    yield session
    # Clean up data after each test
    session.run("MATCH (n) DETACH DELETE n")
    session.close()


@pytest.fixture
def aircraft_repo(session):
    """Provide an AircraftRepository instance."""
    return AircraftRepository(session)


@pytest.fixture
def flight_repo(session):
    """Provide a FlightRepository instance."""
    return FlightRepository(session)


@pytest.fixture
def system_repo(session):
    """Provide a SystemRepository instance."""
    return SystemRepository(session)


@pytest.fixture
def maintenance_repo(session):
    """Provide a MaintenanceEventRepository instance."""
    return MaintenanceEventRepository(session)


@pytest.fixture
def airport_repo(session):
    """Provide an AirportRepository instance."""
    return AirportRepository(session)
