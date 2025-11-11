"""Pytest configuration and fixtures."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer

from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j testcontainer for the test session."""
    container = Neo4jContainer("neo4j:5.15.0")
    container.start()
    
    yield container
    
    container.stop()


@pytest.fixture(scope="session")
def neo4j_connection_params(neo4j_container):
    """Provide connection parameters for Neo4j testcontainer."""
    return {
        "uri": neo4j_container.get_connection_url(),
        "username": neo4j_container.username,
        "password": neo4j_container.password,
        "database": "neo4j"
    }


@pytest.fixture
def neo4j_client(neo4j_connection_params):
    """Provide a Neo4j client connection for each test."""
    connection = Neo4jConnection(**neo4j_connection_params)
    connection.connect()
    
    yield connection
    
    # Cleanup: delete all data after each test
    with connection.get_session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    
    connection.close()
