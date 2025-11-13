"""Custom exceptions for Neo4j aircraft client."""


class Neo4jClientError(Exception):
    """Base exception for Neo4j client errors."""
    pass


class ConnectionError(Neo4jClientError):
    """Exception raised when connection to Neo4j fails."""
    pass


class QueryError(Neo4jClientError):
    """Exception raised when a Cypher query fails."""
    pass


class NotFoundError(Neo4jClientError):
    """Exception raised when a requested entity is not found."""
    pass
