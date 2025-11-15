"""Connection management for Neo4j database."""

from typing import Optional
from neo4j import GraphDatabase, Driver, Session
from neo4j.exceptions import Neo4jError

from neo4j_client.exceptions import ConnectionError as ClientConnectionError


class Neo4jConnection:
    """Manages connections to the Neo4j database.
    
    This class provides connection management with context manager support
    for safe resource handling.
    
    Args:
        uri: Neo4j connection URI (e.g., "bolt://localhost:7687")
        username: Authentication username
        password: Authentication password
        database: Target database name (default: "neo4j")
    
    Example:
        >>> with Neo4jConnection(uri, username, password) as conn:
        ...     session = conn.session()
        ...     result = session.run("MATCH (n) RETURN count(n)")
    """

    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
        database: str = "neo4j",
    ):
        """Initialize the connection manager.
        
        Args:
            uri: Neo4j connection URI
            username: Authentication username
            password: Authentication password
            database: Target database name
        
        Raises:
            ClientConnectionError: If connection cannot be established
        """
        self.uri = uri
        self.username = username
        self.database = database
        self._driver: Optional[Driver] = None

        try:
            self._driver = GraphDatabase.driver(uri, auth=(username, password))
            # Verify connectivity
            self._driver.verify_connectivity()
        except Neo4jError as e:
            raise ClientConnectionError(f"Failed to connect to Neo4j: {e}") from e

    def close(self) -> None:
        """Close the connection to Neo4j."""
        if self._driver:
            self._driver.close()
            self._driver = None

    def session(self, **kwargs) -> Session:
        """Create a new database session.
        
        Args:
            **kwargs: Additional session parameters
        
        Returns:
            A Neo4j session object
        
        Raises:
            ClientConnectionError: If driver is not initialized
        """
        if not self._driver:
            raise ClientConnectionError("Driver is not initialized")
        
        return self._driver.session(database=self.database, **kwargs)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
