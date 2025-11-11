"""Repository pattern for Neo4j entities."""

from typing import List, Optional
from neo4j import Session
from neo4j.exceptions import Neo4jError

from .models import (
    Aircraft, Airport, Flight, Delay, MaintenanceEvent,
    System, Component, Sensor, Reading
)
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """
        Create a new aircraft in the database.
        
        Args:
            aircraft: Aircraft object to create
            
        Returns:
            Created aircraft object
            
        Raises:
            QueryError: If the query fails
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
            result = self.session.run(query, **aircraft.model_dump())
            record = result.single()
            if record:
                return aircraft
            raise QueryError("Failed to create aircraft")
        except Neo4jError as e:
            raise QueryError(f"Failed to create aircraft: {e}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """
        Find an aircraft by ID.
        
        Args:
            aircraft_id: Aircraft ID to search for
            
        Returns:
            Aircraft object if found, None otherwise
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            if record:
                node = record["a"]
                return Aircraft(**node)
            return None
        except Neo4jError as e:
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """
        Find all aircraft.
        
        Args:
            limit: Maximum number of results to return
            
        Returns:
            List of aircraft objects
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Aircraft)
        RETURN a
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            return [Aircraft(**record["a"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def update(self, aircraft: Aircraft) -> Aircraft:
        """
        Update an existing aircraft.
        
        Args:
            aircraft: Aircraft object with updated data
            
        Returns:
            Updated aircraft object
            
        Raises:
            NotFoundError: If aircraft not found
            QueryError: If the query fails
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
            result = self.session.run(query, **aircraft.model_dump())
            record = result.single()
            if not record:
                raise NotFoundError(f"Aircraft {aircraft.aircraft_id} not found")
            return aircraft
        except Neo4jError as e:
            raise QueryError(f"Failed to update aircraft: {e}")
    
    def delete(self, aircraft_id: str) -> bool:
        """
        Delete an aircraft by ID.
        
        Args:
            aircraft_id: Aircraft ID to delete
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        DETACH DELETE a
        RETURN count(a) as deleted
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Neo4jError as e:
            raise QueryError(f"Failed to delete aircraft: {e}")


class FlightRepository:
    """Repository for Flight entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, flight: Flight) -> Flight:
        """
        Create a new flight in the database.
        
        Args:
            flight: Flight object to create
            
        Returns:
            Created flight object
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MERGE (f:Flight {flight_id: $flight_id})
        SET f.flight_number = $flight_number,
            f.aircraft_id = $aircraft_id,
            f.operator = $operator,
            f.origin = $origin,
            f.destination = $destination,
            f.scheduled_departure = $scheduled_departure,
            f.scheduled_arrival = $scheduled_arrival
        RETURN f
        """
        try:
            result = self.session.run(query, **flight.model_dump())
            record = result.single()
            if record:
                return flight
            raise QueryError("Failed to create flight")
        except Neo4jError as e:
            raise QueryError(f"Failed to create flight: {e}")
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """
        Find a flight by ID.
        
        Args:
            flight_id: Flight ID to search for
            
        Returns:
            Flight object if found, None otherwise
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        RETURN f
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
            record = result.single()
            if record:
                node = record["f"]
                return Flight(**node)
            return None
        except Neo4jError as e:
            raise QueryError(f"Failed to find flight: {e}")
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """
        Find flights by aircraft ID.
        
        Args:
            aircraft_id: Aircraft ID to search for
            limit: Maximum number of results to return
            
        Returns:
            List of flight objects
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (f:Flight {aircraft_id: $aircraft_id})
        RETURN f
        LIMIT $limit
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
            return [Flight(**record["f"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Failed to find flights: {e}")
    
    def find_all(self, limit: int = 100) -> List[Flight]:
        """
        Find all flights.
        
        Args:
            limit: Maximum number of results to return
            
        Returns:
            List of flight objects
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (f:Flight)
        RETURN f
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            return [Flight(**record["f"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Failed to find flights: {e}")


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """
        Create a new maintenance event in the database.
        
        Args:
            event: MaintenanceEvent object to create
            
        Returns:
            Created maintenance event object
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MERGE (e:MaintenanceEvent {event_id: $event_id})
        SET e.aircraft_id = $aircraft_id,
            e.system_id = $system_id,
            e.component_id = $component_id,
            e.fault = $fault,
            e.severity = $severity,
            e.corrective_action = $corrective_action,
            e.reported_at = $reported_at
        RETURN e
        """
        try:
            result = self.session.run(query, **event.model_dump())
            record = result.single()
            if record:
                return event
            raise QueryError("Failed to create maintenance event")
        except Neo4jError as e:
            raise QueryError(f"Failed to create maintenance event: {e}")
    
    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """
        Find a maintenance event by ID.
        
        Args:
            event_id: Event ID to search for
            
        Returns:
            MaintenanceEvent object if found, None otherwise
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (e:MaintenanceEvent {event_id: $event_id})
        RETURN e
        """
        try:
            result = self.session.run(query, event_id=event_id)
            record = result.single()
            if record:
                node = record["e"]
                return MaintenanceEvent(**node)
            return None
        except Neo4jError as e:
            raise QueryError(f"Failed to find maintenance event: {e}")
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find maintenance events by aircraft ID.
        
        Args:
            aircraft_id: Aircraft ID to search for
            limit: Maximum number of results to return
            
        Returns:
            List of maintenance event objects
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (e:MaintenanceEvent {aircraft_id: $aircraft_id})
        RETURN e
        ORDER BY e.reported_at DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
            return [MaintenanceEvent(**record["e"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Failed to find maintenance events: {e}")
    
    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find maintenance events by severity.
        
        Args:
            severity: Severity level to search for
            limit: Maximum number of results to return
            
        Returns:
            List of maintenance event objects
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (e:MaintenanceEvent {severity: $severity})
        RETURN e
        ORDER BY e.reported_at DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, severity=severity, limit=limit)
            return [MaintenanceEvent(**record["e"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Failed to find maintenance events: {e}")
