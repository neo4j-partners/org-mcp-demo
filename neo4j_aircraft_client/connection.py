"""
Connection management for Neo4j database.

This module provides a connection manager class for handling Neo4j database connections
with support for context managers and session management.
"""

from typing import Optional
from neo4j import GraphDatabase, Driver, Session
from .exceptions import ConnectionError as ClientConnectionError


class Neo4jConnection:
    """
    Manages connections to a Neo4j database.
    
    This class provides a simple interface for connecting to Neo4j and managing
    database sessions. It supports both direct usage and context manager protocol.
    
    Attributes:
        uri: Neo4j connection URI (e.g., "bolt://localhost:7687")
        username: Database username
        password: Database password
        database: Target database name (default: "neo4j")
    
    Example:
        >>> conn = Neo4jConnection("bolt://localhost:7687", "neo4j", "password")
        >>> with conn.session() as session:
        ...     result = session.run("MATCH (n) RETURN count(n)")
        >>> conn.close()
        
        Or using context manager:
        >>> with Neo4jConnection("bolt://localhost:7687", "neo4j", "password") as conn:
        ...     with conn.session() as session:
        ...         result = session.run("MATCH (n) RETURN count(n)")
    """
    
    def __init__(self, uri: str, username: str, password: str, database: str = "neo4j"):
        """
        Initialize a new Neo4j connection.
        
        Args:
            uri: Neo4j connection URI (e.g., "bolt://localhost:7687")
            username: Database username
            password: Database password
            database: Target database name (default: "neo4j")
            
        Raises:
            ClientConnectionError: If connection to the database fails
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self._driver: Optional[Driver] = None
        
        try:
            self._driver = GraphDatabase.driver(uri, auth=(username, password))
            # Verify connectivity
            self._driver.verify_connectivity()
        except Exception as e:
            raise ClientConnectionError(f"Failed to connect to Neo4j at {uri}: {str(e)}")
    
    def session(self) -> Session:
        """
        Create a new database session.
        
        Returns:
            A Neo4j session object
            
        Raises:
            ClientConnectionError: If the driver is not initialized
        """
        if self._driver is None:
            raise ClientConnectionError("Driver is not initialized")
        return self._driver.session(database=self.database)
    
    def close(self) -> None:
        """Close the database connection."""
        if self._driver is not None:
            self._driver.close()
            self._driver = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
