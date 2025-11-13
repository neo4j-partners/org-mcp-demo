"""Connection management for Neo4j database."""

from typing import Optional
from neo4j import GraphDatabase, Driver, Session
from .exceptions import ConnectionError as ClientConnectionError


class Neo4jConnection:
    """Manages connections to Neo4j database with context manager support."""
    
    def __init__(self, uri: str, username: str, password: str, database: str = "neo4j"):
        """
        Initialize Neo4j connection manager.
        
        Args:
            uri: Neo4j connection URI (e.g., 'bolt://localhost:7687')
            username: Database username
            password: Database password
            database: Target database name (default: 'neo4j')
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self._driver: Optional[Driver] = None
        
    def connect(self) -> Driver:
        """
        Establish connection to Neo4j.
        
        Returns:
            Neo4j driver instance
            
        Raises:
            ClientConnectionError: If connection fails
        """
        try:
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )
            # Verify connectivity
            self._driver.verify_connectivity()
            return self._driver
        except Exception as e:
            raise ClientConnectionError(f"Failed to connect to Neo4j: {e}")
    
    def close(self) -> None:
        """Close the Neo4j connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
    
    def get_session(self) -> Session:
        """
        Get a new session for query execution.
        
        Returns:
            Neo4j session
            
        Raises:
            ClientConnectionError: If not connected
        """
        if not self._driver:
            raise ClientConnectionError("Not connected. Call connect() first.")
        return self._driver.session(database=self.database)
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
