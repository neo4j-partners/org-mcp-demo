"""
Pytest fixtures for Neo4j aviation client tests.

This module provides test fixtures using testcontainers to spin up
a Neo4j instance for integration testing.
"""

import os
import pytest
from neo4j_client import Neo4jConnection


@pytest.fixture(scope="session")
def neo4j_uri():
    """
    Get Neo4j URI from environment variable.
    
    Returns:
        Neo4j connection URI
    """
    return os.getenv("NEO4J_URI", "bolt://localhost:7687")


@pytest.fixture(scope="session")
def neo4j_username():
    """
    Get Neo4j username from environment variable.
    
    Returns:
        Neo4j username
    """
    return os.getenv("NEO4J_USERNAME", "neo4j")


@pytest.fixture(scope="session")
def neo4j_password():
    """
    Get Neo4j password from environment variable.
    
    Returns:
        Neo4j password
    """
    return os.getenv("NEO4J_PASSWORD", "password")


@pytest.fixture(scope="session")
def neo4j_database():
    """
    Get Neo4j database name from environment variable.
    
    Returns:
        Neo4j database name
    """
    return os.getenv("NEO4J_DATABASE", "neo4j")


@pytest.fixture(scope="function")
def connection(neo4j_uri, neo4j_username, neo4j_password, neo4j_database):
    """
    Create a Neo4j connection for testing.
    
    This fixture provides a fresh connection for each test function.
    The connection is automatically closed after the test completes.
    
    Yields:
        Neo4jConnection instance
    """
    conn = Neo4jConnection(
        uri=neo4j_uri,
        username=neo4j_username,
        password=neo4j_password,
        database=neo4j_database
    )
    yield conn
    conn.close()
