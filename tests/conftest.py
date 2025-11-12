"""Test fixtures and configuration for pytest."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client.connection import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j test container for the entire test session.
    
    Yields:
        Neo4jContainer instance with connection details
    """
    # Create container with specified password using constructor parameter
    with Neo4jContainer(image="neo4j:5.15", password="testpassword") as container:
        yield container


@pytest.fixture(scope="session")
def neo4j_connection_params(neo4j_container):
    """Extract connection parameters from the Neo4j container.
    
    Args:
        neo4j_container: Neo4j test container
        
    Returns:
        Dictionary with connection parameters
    """
    return {
        "uri": neo4j_container.get_connection_url(),
        "username": "neo4j",
        "password": "testpassword",
        "database": "neo4j"
    }


@pytest.fixture
def connection(neo4j_connection_params):
    """Provide a fresh Neo4j connection for each test.
    
    Args:
        neo4j_connection_params: Connection parameters from container
        
    Yields:
        Neo4jConnection instance
    """
    conn = Neo4jConnection(**neo4j_connection_params)
    yield conn
    
    # Cleanup: clear database after each test
    try:
        with conn.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
    except:
        pass  # Ignore cleanup errors
    
    conn.close()
