"""
Custom exceptions for the Neo4j aviation client.
"""


class Neo4jClientError(Exception):
    """Base exception for all Neo4j client errors."""
    pass


class ConnectionError(Neo4jClientError):
    """Raised when connection to Neo4j database fails."""
    pass


class QueryError(Neo4jClientError):
    """Raised when a Cypher query execution fails."""
    pass


class NotFoundError(Neo4jClientError):
    """Raised when a requested entity is not found in the database."""
    pass
