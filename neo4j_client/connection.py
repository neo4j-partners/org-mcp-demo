"""Connection management for Neo4j database."""

from typing import Optional
from neo4j import GraphDatabase, Driver, Session
from .exceptions import ConnectionError as Neo4jConnectionError


class Neo4jConnection:
    """Manages connections to Neo4j database."""
    
    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
        database: str = "neo4j"
    ):
        """
        Initialize Neo4j connection.
        
        Args:
            uri: Neo4j database URI (e.g., 'bolt://localhost:7687')
            username: Database username
            password: Database password
            database: Database name (default: 'neo4j')
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self._driver: Optional[Driver] = None
        
    def connect(self) -> Driver:
        """
        Establish connection to Neo4j database.
        
        Returns:
            Neo4j driver instance
            
        Raises:
            Neo4jConnectionError: If connection fails
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
            raise Neo4jConnectionError(f"Failed to connect to Neo4j: {str(e)}")
    
    def close(self):
        """Close the database connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
    
    def get_session(self) -> Session:
        """
        Get a new database session.
        
        Returns:
            Neo4j session instance
            
        Raises:
            Neo4jConnectionError: If not connected
        """
        if not self._driver:
            raise Neo4jConnectionError("Not connected to database. Call connect() first.")
        return self._driver.session(database=self.database)
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
