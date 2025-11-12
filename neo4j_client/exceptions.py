"""Custom exceptions for the Neo4j client."""


class Neo4jClientError(Exception):
    """Base exception for all Neo4j client errors."""
    pass


class ConnectionError(Neo4jClientError):
    """Raised when there is a connection error to the Neo4j database."""
    pass


class QueryError(Neo4jClientError):
    """Raised when a Cypher query fails."""
    pass


class NotFoundError(Neo4jClientError):
    """Raised when a requested entity is not found."""
    pass
