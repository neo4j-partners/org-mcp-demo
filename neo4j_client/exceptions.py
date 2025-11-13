"""Custom exception classes for Neo4j client."""


class Neo4jClientError(Exception):
    """Base exception for all Neo4j client errors."""
    pass


class ConnectionError(Neo4jClientError):
    """Raised when connection to Neo4j fails."""
    pass


class QueryError(Neo4jClientError):
    """Raised when a query execution fails."""
    pass


class NotFoundError(Neo4jClientError):
    """Raised when a requested entity is not found."""
    pass
