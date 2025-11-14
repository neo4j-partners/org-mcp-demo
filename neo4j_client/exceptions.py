"""Custom exception classes for Neo4j client."""


class Neo4jClientError(Exception):
    """Base exception class for Neo4j client errors."""
    pass


class ConnectionError(Neo4jClientError):
    """Exception raised when connection to Neo4j fails."""
    pass


class QueryError(Neo4jClientError):
    """Exception raised when a Cypher query fails."""
    pass


class NotFoundError(Neo4jClientError):
    """Exception raised when an entity is not found."""
    pass
