"""Pytest fixtures for Neo4j client tests."""

import pytest
from testcontainers.neo4j import Neo4jContainer

from neo4j_client.connection import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j container for testing.
    
    This fixture creates a Neo4j container that persists for the entire test session.
    """
    container = Neo4jContainer("neo4j:5.15")
    container.start()
    
    yield container
    
    container.stop()


@pytest.fixture(scope="session")
def neo4j_connection(neo4j_container):
    """Provide a Neo4j connection using the test container.
    
    This fixture creates a connection to the test Neo4j container.
    """
    uri = neo4j_container.get_connection_url()
    username = neo4j_container.username
    password = neo4j_container.password
    
    conn = Neo4jConnection(uri, username, password)
    
    yield conn
    
    conn.close()


@pytest.fixture
def neo4j_session(neo4j_connection):
    """Provide a Neo4j session for each test.
    
    This fixture creates a fresh session for each test function.
    The session is automatically cleaned up after the test.
    """
    session = neo4j_connection.session()
    
    yield session
    
    # Cleanup: delete all data after each test
    session.run("MATCH (n) DETACH DELETE n")
    session.close()
