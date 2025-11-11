"""Pytest configuration and fixtures."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j test container for the test session."""
    container = Neo4jContainer("neo4j:5.13")
    container.start()
    yield container
    container.stop()


@pytest.fixture(scope="session")
def neo4j_connection(neo4j_container):
    """Provide a Neo4j connection for the test session."""
    # Get password from Neo4jContainer
    password = neo4j_container.password
    connection = Neo4jConnection(
        uri=neo4j_container.get_connection_url(),
        username="neo4j",
        password=password
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
