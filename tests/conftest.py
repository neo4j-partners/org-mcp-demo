"""Pytest configuration and fixtures."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j test container for the session."""
    container = Neo4jContainer("neo4j:5.15")
    container.start()
    
    yield container
    
    container.stop()


@pytest.fixture(scope="session")
def neo4j_connection_params(neo4j_container):
    """Provide connection parameters for the test Neo4j instance."""
    return {
        "uri": neo4j_container.get_connection_url(),
        "username": neo4j_container.username,
        "password": neo4j_container.password,
        "database": "neo4j"
    }


@pytest.fixture
def neo4j_connection(neo4j_connection_params):
    """Provide a Neo4j connection for each test."""
    connection = Neo4jConnection(**neo4j_connection_params)
    connection.connect()
    
    yield connection
    
    # Clean up all data after each test
    with connection.get_session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    
    connection.close()
