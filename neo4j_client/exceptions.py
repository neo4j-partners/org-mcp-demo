"""Custom exceptions for the Neo4j client."""


class Neo4jClientError(Exception):
    """Base exception for all Neo4j client errors."""
    pass


class ConnectionError(Neo4jClientError):
    """Raised when unable to connect to Neo4j database."""
    pass


class QueryError(Neo4jClientError):
    """Raised when a query execution fails."""
    pass


class NotFoundError(Neo4jClientError):
    """Raised when a requested entity is not found."""
    pass


class ValidationError(Neo4jClientError):
    """Raised when input validation fails."""
    pass
