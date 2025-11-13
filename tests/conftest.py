"""Pytest fixtures for Neo4j aircraft client tests."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer
from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j test container for the session.
    
    Yields:
        Neo4jContainer: Running Neo4j container
    """
    with Neo4jContainer("neo4j:5.14") as container:
        yield container


@pytest.fixture(scope="session")
def neo4j_connection(neo4j_container):
    """Provide a Neo4j connection for the session.
    
    Args:
        neo4j_container: Neo4j container fixture
        
    Yields:
        Neo4jConnection: Connected Neo4j client
    """
    uri = neo4j_container.get_connection_url()
    username = "neo4j"
    password = "test"
    
    with Neo4jConnection(uri, username, password) as conn:
        yield conn


@pytest.fixture
def session(neo4j_connection):
    """Provide a Neo4j session for each test.
    
    Args:
        neo4j_connection: Neo4j connection fixture
        
    Yields:
        Session: Neo4j session, cleaned up after test
    """
    session = neo4j_connection.get_session()
    yield session
    
    # Cleanup: delete all nodes and relationships after each test
    session.run("MATCH (n) DETACH DELETE n")
    session.close()
