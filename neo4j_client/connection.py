"""Connection management for Neo4j database."""

from typing import Optional
from neo4j import GraphDatabase, Driver, Session
from .exceptions import ConnectionError as ClientConnectionError


class Neo4jConnection:
    """Manages connections to Neo4j database."""
    
    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
        database: str = "neo4j"
    ):
        """Initialize Neo4j connection.
        
        Args:
            uri: Neo4j database URI (e.g., bolt://localhost:7687)
            username: Authentication username
            password: Authentication password
            database: Database name (default: neo4j)
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self._driver: Optional[Driver] = None
        
    def connect(self) -> None:
        """Establish connection to Neo4j database."""
        try:
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )
            # Verify connectivity
            self._driver.verify_connectivity()
        except Exception as e:
            raise ClientConnectionError(f"Failed to connect to Neo4j: {str(e)}")
    
    def close(self) -> None:
        """Close the database connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
    
    def get_session(self) -> Session:
        """Get a database session.
        
        Returns:
            Neo4j session object
            
        Raises:
            ClientConnectionError: If not connected
        """
        if not self._driver:
            raise ClientConnectionError("Not connected to database. Call connect() first.")
        return self._driver.session(database=self.database)
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
