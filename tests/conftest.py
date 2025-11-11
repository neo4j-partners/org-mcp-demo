"""Pytest fixtures for Neo4j client tests."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer

from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """
    Provide a Neo4j test container for the test session.
    
    Yields:
        Neo4jContainer instance
    """
    # Use environment variables if available (for CI/existing instance)
    use_existing = os.getenv("NEO4J_URI") is not None
    
    if use_existing:
        # Use existing Neo4j instance from environment
        yield None
    else:
        # Start a new container for testing
        with Neo4jContainer("neo4j:5.15") as container:
            yield container


@pytest.fixture(scope="session")
def neo4j_credentials(neo4j_container):
    """
    Provide Neo4j connection credentials.
    
    Args:
        neo4j_container: Neo4j container fixture
        
    Returns:
        Dictionary with connection credentials
    """
    if neo4j_container:
        # Use container credentials
        return {
            "uri": neo4j_container.get_connection_url(),
            "username": "neo4j",
            "password": "password",
            "database": "neo4j"
        }
    else:
        # Use environment credentials
        return {
            "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            "username": os.getenv("NEO4J_USERNAME", "neo4j"),
            "password": os.getenv("NEO4J_PASSWORD", "password"),
            "database": os.getenv("NEO4J_DATABASE", "neo4j")
        }


@pytest.fixture
def neo4j_connection(neo4j_credentials):
    """
    Provide a Neo4j connection for each test.
    
    Args:
        neo4j_credentials: Connection credentials fixture
        
    Yields:
        Neo4jConnection instance
    """
    connection = Neo4jConnection(**neo4j_credentials)
    connection.connect()
    yield connection
    connection.close()


@pytest.fixture
def neo4j_session(neo4j_connection):
    """
    Provide a Neo4j session for each test.
    
    Args:
        neo4j_connection: Connection fixture
        
    Yields:
        Neo4j session instance
    """
    session = neo4j_connection.get_session()
    yield session
    
    # Cleanup: Delete any test data created during the test
    # This only cleans up nodes created with test IDs (starting with 'test_')
    session.run("""
        MATCH (n)
        WHERE n.aircraft_id STARTS WITH 'test_'
           OR n.airport_id STARTS WITH 'test_'
           OR n.flight_id STARTS WITH 'test_'
           OR n.event_id STARTS WITH 'test_'
           OR n.delay_id STARTS WITH 'test_'
        DETACH DELETE n
    """)
    
    session.close()
