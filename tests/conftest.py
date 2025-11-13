"""Pytest configuration and fixtures."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """
    Session-scoped Neo4j test container.
    
    Provides a clean Neo4j instance for all tests.
    """
    container = Neo4jContainer("neo4j:5.14")
    container.start()
    
    yield container
    
    container.stop()


@pytest.fixture(scope="session")
def neo4j_uri(neo4j_container):
    """Get Neo4j connection URI from container."""
    return neo4j_container.get_connection_url()


@pytest.fixture(scope="session")
def neo4j_auth(neo4j_container):
    """Get Neo4j authentication credentials."""
    return ("neo4j", neo4j_container.password)


@pytest.fixture
def neo4j_connection(neo4j_uri, neo4j_auth):
    """
    Function-scoped Neo4j connection.
    
    Provides a fresh connection for each test and ensures cleanup.
    """
    connection = Neo4jConnection(
        uri=neo4j_uri,
        username=neo4j_auth[0],
        password=neo4j_auth[1]
    )
    connection.connect()
    
    yield connection
    
    # Cleanup: delete all nodes and relationships after each test
    with connection.get_session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    
    connection.close()


@pytest.fixture
def session(neo4j_connection):
    """
    Get a database session for testing.
    
    Auto-closes after test completion.
    """
    session = neo4j_connection.get_session()
    yield session
    session.close()
