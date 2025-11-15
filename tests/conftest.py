"""Pytest fixtures for Neo4j client tests."""

import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j test container for the session.
    
    Yields:
        Neo4jContainer instance with Neo4j running
    """
    with Neo4jContainer("neo4j:5.13", password="testpassword") as container:
        yield container


@pytest.fixture(scope="session")
def neo4j_uri(neo4j_container):
    """Get the Neo4j connection URI from the container.
    
    Args:
        neo4j_container: Neo4j test container
        
    Returns:
        Connection URI string
    """
    return neo4j_container.get_connection_url()


@pytest.fixture(scope="session")
def neo4j_credentials():
    """Provide Neo4j authentication credentials.
    
    Returns:
        Tuple of (username, password)
    """
    return ("neo4j", "testpassword")


@pytest.fixture
def neo4j_connection(neo4j_uri, neo4j_credentials):
    """Provide a Neo4j connection for tests.
    
    Args:
        neo4j_uri: Connection URI
        neo4j_credentials: Auth credentials tuple
        
    Yields:
        Neo4jConnection instance
    """
    username, password = neo4j_credentials
    with Neo4jConnection(neo4j_uri, username, password) as conn:
        yield conn


@pytest.fixture
def clean_database(neo4j_connection):
    """Clean the database before each test.
    
    Args:
        neo4j_connection: Active Neo4j connection
        
    Yields:
        Neo4j session ready for testing
    """
    session = neo4j_connection.get_session()
    
    # Clean database before test
    session.run("MATCH (n) DETACH DELETE n")
    
    yield session
    
    # Clean database after test
    session.run("MATCH (n) DETACH DELETE n")
    session.close()
