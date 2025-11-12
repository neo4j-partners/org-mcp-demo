"""
Pytest configuration and fixtures for Neo4j aircraft client tests.

This module provides test fixtures using testcontainers to set up a temporary
Neo4j database for integration testing.
"""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_aircraft_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """
    Provide a Neo4j container for the test session.
    
    This fixture starts a Neo4j container and provides connection details.
    The container is automatically cleaned up after the test session.
    """
    # Check if we should use an existing Neo4j instance
    existing_uri = os.getenv("NEO4J_URI")
    existing_user = os.getenv("NEO4J_USERNAME")
    existing_pass = os.getenv("NEO4J_PASSWORD")
    existing_db = os.getenv("NEO4J_DATABASE", "neo4j")
    
    if existing_uri and existing_user and existing_pass:
        # Use existing Neo4j instance
        yield {
            "uri": existing_uri,
            "username": existing_user,
            "password": existing_pass,
            "database": existing_db,
        }
    else:
        # Start a new container for testing
        with Neo4jContainer("neo4j:5.15", password="testpassword") as container:
            yield {
                "uri": container.get_connection_url(),
                "username": "neo4j",
                "password": "testpassword",
                "database": "neo4j",
            }


@pytest.fixture
def connection(neo4j_container):
    """
    Provide a Neo4j connection for each test.
    
    This fixture creates a new connection for each test and ensures
    it's properly closed after the test completes.
    """
    conn = Neo4jConnection(
        uri=neo4j_container["uri"],
        username=neo4j_container["username"],
        password=neo4j_container["password"],
        database=neo4j_container["database"],
    )
    yield conn
    conn.close()


@pytest.fixture
def session(connection):
    """
    Provide a Neo4j session for each test.
    
    This fixture creates a new session for each test and ensures
    it's properly closed after the test completes.
    """
    with connection.session() as session:
        yield session
