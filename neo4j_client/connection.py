"""Connection management for Neo4j database."""

from typing import Optional
from neo4j import GraphDatabase, Driver, Session
from neo4j_client.exceptions import ConnectionError


class Neo4jConnection:
    """Manages connections to a Neo4j database.
    
    This class provides connection management with context manager support
    for automatic resource cleanup.
    
    Example:
        >>> with Neo4jConnection(uri, username, password) as conn:
        ...     session = conn.session()
        ...     # use session
    """
    
    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
        database: str = "neo4j"
    ):
        """Initialize the Neo4j connection.
        
        Args:
            uri: Neo4j connection URI (e.g., "bolt://localhost:7687")
            username: Database username
            password: Database password
            database: Target database name (default: "neo4j")
            
        Raises:
            ConnectionError: If connection to database fails
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
            # Verify connectivity
            self._driver.verify_connectivity()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Neo4j: {str(e)}")
    
    def session(self) -> Session:
        """Create a new database session.
        
        Returns:
            A Neo4j session object
            
        Raises:
            ConnectionError: If driver is not initialized
        """
        if not self._driver:
            raise ConnectionError("Driver is not initialized")
        return self._driver.session(database=self.database)
    
    def close(self) -> None:
        """Close the database connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
    
    def __enter__(self) -> "Neo4jConnection":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with automatic cleanup."""
        self.close()
