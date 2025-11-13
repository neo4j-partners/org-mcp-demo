"""Neo4j connection management."""

from typing import Optional
from neo4j import GraphDatabase, Driver, Session
from .exceptions import ConnectionError


class Neo4jConnection:
    """Manages Neo4j database connections.
    
    This class provides connection management with context manager support
    for safe resource cleanup.
    
    Attributes:
        uri: Neo4j connection URI (e.g., "bolt://localhost:7687")
        username: Authentication username
        password: Authentication password
        database: Target database name (default: "neo4j")
    """
    
    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
        database: str = "neo4j"
    ):
        """Initialize Neo4j connection.
        
        Args:
            uri: Neo4j connection URI
            username: Authentication username
            password: Authentication password
            database: Target database name (default: "neo4j")
            
        Raises:
            ConnectionError: If connection to Neo4j fails
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self._driver: Optional[Driver] = None
        
        try:
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )
            # Test connection
            self._driver.verify_connectivity()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Neo4j: {e}")
    
    def get_session(self) -> Session:
        """Get a new Neo4j session.
        
        Returns:
            A new Neo4j session instance
            
        Raises:
            ConnectionError: If driver is not initialized
        """
        if not self._driver:
            raise ConnectionError("Driver not initialized")
        return self._driver.session(database=self.database)
    
    def close(self) -> None:
        """Close the Neo4j driver connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
    
    def __enter__(self) -> "Neo4jConnection":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with cleanup."""
        self.close()
