"""
Custom exceptions for the Neo4j aircraft client.

This module defines a hierarchy of exceptions for error handling in the client library.
"""


class Neo4jClientError(Exception):
    """Base exception class for all Neo4j client errors."""
    pass


class ConnectionError(Neo4jClientError):
    """Raised when there's an error connecting to the Neo4j database."""
    pass


class QueryError(Neo4jClientError):
    """Raised when there's an error executing a Cypher query."""
    pass


class NotFoundError(Neo4jClientError):
    """Raised when a requested entity is not found in the database."""
    pass
