"""Pytest configuration and fixtures."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """
    Provide a Neo4j container for testing.
    
    Yields:
        Neo4jContainer instance
    """
    container = Neo4jContainer("neo4j:5.14")
    container.with_env("NEO4J_AUTH", "neo4j/testpassword")
    container.start()
    
    yield container
    
    container.stop()


@pytest.fixture(scope="session")
def neo4j_uri(neo4j_container):
    """Get Neo4j connection URI from container."""
    return neo4j_container.get_connection_url()


@pytest.fixture(scope="session")
def neo4j_credentials():
    """Get Neo4j credentials for testing."""
    return {
        "username": "neo4j",
        "password": "testpassword"
    }


@pytest.fixture
def neo4j_connection(neo4j_uri, neo4j_credentials):
    """
    Provide a Neo4j connection for testing.
    
    Yields:
        Connected Neo4jConnection instance
    """
    connection = Neo4jConnection(
        uri=neo4j_uri,
        username=neo4j_credentials["username"],
        password=neo4j_credentials["password"]
    )
    connection.connect()
    
    yield connection
    
    # Cleanup: remove all data after each test
    with connection.get_session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    
    connection.close()
