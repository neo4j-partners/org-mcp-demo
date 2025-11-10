"""Repository pattern implementation for Aircraft entity."""

from typing import List, Optional
from neo4j.exceptions import Neo4jError

from neo4j_client.connection import Neo4jConnection
from neo4j_client.models import Aircraft
from neo4j_client.exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for managing Aircraft entities in Neo4j.
    
    This class provides CRUD operations for Aircraft nodes using
    parameterized Cypher queries to prevent injection attacks.
    """
    
    def __init__(self, connection: Neo4jConnection):
        """Initialize the repository.
        
        Args:
            connection: Neo4jConnection instance
        """
        self.connection = connection
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """Create a new aircraft in the database.
        
        Args:
            aircraft: Aircraft model to create
            
        Returns:
            The created Aircraft
            
        Raises:
            QueryError: If the query execution fails
        """
        query = """
        MERGE (a:Aircraft {aircraft_id: $aircraft_id})
        SET a.tail_number = $tail_number,
            a.icao24 = $icao24,
            a.model = $model,
            a.operator = $operator,
            a.manufacturer = $manufacturer
        RETURN a
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(
                    query,
                    aircraft_id=aircraft.aircraft_id,
                    tail_number=aircraft.tail_number,
                    icao24=aircraft.icao24,
                    model=aircraft.model,
                    operator=aircraft.operator,
                    manufacturer=aircraft.manufacturer
                )
                record = result.single()
                if record:
                    return Aircraft(**record["a"])
                raise QueryError("Failed to create aircraft")
        except Neo4jError as e:
            raise QueryError(f"Query execution failed: {e}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """Find an aircraft by its ID.
        
        Args:
            aircraft_id: The aircraft ID to search for
            
        Returns:
            Aircraft if found, None otherwise
            
        Raises:
            QueryError: If the query execution fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                record = result.single()
                if record:
                    return Aircraft(**record["a"])
                return None
        except Neo4jError as e:
            raise QueryError(f"Query execution failed: {e}")
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """Find an aircraft by its tail number.
        
        Args:
            tail_number: The tail number to search for
            
        Returns:
            Aircraft if found, None otherwise
            
        Raises:
            QueryError: If the query execution fails
        """
        query = """
        MATCH (a:Aircraft {tail_number: $tail_number})
        RETURN a
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, tail_number=tail_number)
                record = result.single()
                if record:
                    return Aircraft(**record["a"])
                return None
        except Neo4jError as e:
            raise QueryError(f"Query execution failed: {e}")
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """Find all aircraft in the database.
        
        Args:
            limit: Maximum number of aircraft to return (default: 100)
            
        Returns:
            List of Aircraft objects
            
        Raises:
            QueryError: If the query execution fails
        """
        query = """
        MATCH (a:Aircraft)
        RETURN a
        LIMIT $limit
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, limit=limit)
                return [Aircraft(**record["a"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Query execution failed: {e}")
    
    def find_by_operator(self, operator: str) -> List[Aircraft]:
        """Find all aircraft operated by a specific operator.
        
        Args:
            operator: The operator name to search for
            
        Returns:
            List of Aircraft objects
            
        Raises:
            QueryError: If the query execution fails
        """
        query = """
        MATCH (a:Aircraft {operator: $operator})
        RETURN a
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, operator=operator)
                return [Aircraft(**record["a"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Query execution failed: {e}")
    
    def find_by_manufacturer(self, manufacturer: str) -> List[Aircraft]:
        """Find all aircraft from a specific manufacturer.
        
        Args:
            manufacturer: The manufacturer name to search for
            
        Returns:
            List of Aircraft objects
            
        Raises:
            QueryError: If the query execution fails
        """
        query = """
        MATCH (a:Aircraft {manufacturer: $manufacturer})
        RETURN a
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, manufacturer=manufacturer)
                return [Aircraft(**record["a"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Query execution failed: {e}")
    
    def update(self, aircraft: Aircraft) -> Aircraft:
        """Update an existing aircraft.
        
        Args:
            aircraft: Aircraft model with updated data
            
        Returns:
            The updated Aircraft
            
        Raises:
            NotFoundError: If the aircraft doesn't exist
            QueryError: If the query execution fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        SET a.tail_number = $tail_number,
            a.icao24 = $icao24,
            a.model = $model,
            a.operator = $operator,
            a.manufacturer = $manufacturer
        RETURN a
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(
                    query,
                    aircraft_id=aircraft.aircraft_id,
                    tail_number=aircraft.tail_number,
                    icao24=aircraft.icao24,
                    model=aircraft.model,
                    operator=aircraft.operator,
                    manufacturer=aircraft.manufacturer
                )
                record = result.single()
                if record:
                    return Aircraft(**record["a"])
                raise NotFoundError(f"Aircraft with ID {aircraft.aircraft_id} not found")
        except Neo4jError as e:
            raise QueryError(f"Query execution failed: {e}")
    
    def delete(self, aircraft_id: str) -> bool:
        """Delete an aircraft by its ID.
        
        Args:
            aircraft_id: The aircraft ID to delete
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            QueryError: If the query execution fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        DELETE a
        RETURN count(a) as deleted_count
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                record = result.single()
                return record["deleted_count"] > 0 if record else False
        except Neo4jError as e:
            raise QueryError(f"Query execution failed: {e}")
