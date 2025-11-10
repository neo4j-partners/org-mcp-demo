"""Pytest configuration and fixtures for Neo4j client tests."""

import os
import pytest
from testcontainers.neo4j import Neo4jContainer

from neo4j_client.connection import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_container():
    """Provide a Neo4j test container for the test session.
    
    This fixture starts a Neo4j container and provides connection details.
    The container is shared across all tests in the session.
    """
    container = Neo4jContainer("neo4j:5.15")
    container.start()
    
    yield container
    
    container.stop()


@pytest.fixture(scope="session")
def neo4j_connection(neo4j_container):
    """Provide a Neo4j connection for the test session.
    
    Returns:
        Neo4jConnection instance connected to the test container
    """
    connection = Neo4jConnection(
        uri=neo4j_container.get_connection_url(),
        username="neo4j",
        password=neo4j_container.password,
        database="neo4j"
    )
    
    yield connection
    
    connection.close()


@pytest.fixture
def clean_database(neo4j_connection):
    """Clean the database before each test.
    
    This fixture deletes all nodes and relationships before each test
    to ensure test isolation.
    """
    with neo4j_connection.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    
    yield
    
    # Clean up after test as well
    with neo4j_connection.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
