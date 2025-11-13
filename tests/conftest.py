"""Pytest configuration and fixtures for Neo4j client tests."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """
    Session-scoped Neo4j test container.
    
    Yields:
        Neo4jContainer instance
    """
    with Neo4jContainer("neo4j:5.14") as container:
        yield container


@pytest.fixture(scope="session")
def neo4j_uri(neo4j_container):
    """
    Get Neo4j connection URI from container.
    
    Args:
        neo4j_container: Neo4j container fixture
        
    Returns:
        Connection URI string
    """
    return neo4j_container.get_connection_url()


@pytest.fixture(scope="function")
def neo4j_connection(neo4j_container):
    """
    Function-scoped Neo4j connection.
    
    Args:
        neo4j_container: Neo4j container fixture
        
    Yields:
        Connected Neo4jConnection instance
    """
    connection = Neo4jConnection(
        uri=neo4j_container.get_connection_url(),
        username="neo4j",
        password="test12345",
        database="neo4j"
    )
    connection.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def neo4j_session(neo4j_connection):
    """
    Function-scoped Neo4j session with cleanup.
    
    Args:
        neo4j_connection: Neo4j connection fixture
        
    Yields:
        Neo4j session object
    """
    session = neo4j_connection.get_session()
    yield session
    # Clean up test data after each test
    session.run("MATCH (n) DETACH DELETE n")
    session.close()
