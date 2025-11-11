"""Repository pattern for Neo4j queries."""

from typing import List, Optional
from .connection import Neo4jConnection
from .models import (
    Aircraft, Airport, Flight, System, Component,
    Sensor, Reading, MaintenanceEvent, Delay
)
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """
        Initialize repository with Neo4j connection.
        
        Args:
            connection: Neo4jConnection instance
        """
        self.connection = connection
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """
        Create a new aircraft in the database.
        
        Args:
            aircraft: Aircraft model instance
            
        Returns:
            Created Aircraft instance
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
            with self.connection.get_session() as session:
                result = session.run(query, **aircraft.model_dump())
                record = result.single()
                if record:
                    return Aircraft(**dict(record["a"]))
                raise QueryError("Failed to create aircraft")
        except Exception as e:
            raise QueryError(f"Error creating aircraft: {str(e)}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """
        Find aircraft by ID.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            Aircraft instance or None if not found
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                record = result.single()
                if record:
                    return Aircraft(**dict(record["a"]))
                return None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """
        Find aircraft by tail number.
        
        Args:
            tail_number: Aircraft tail number
            
        Returns:
            Aircraft instance or None if not found
        """
        query = """
        MATCH (a:Aircraft {tail_number: $tail_number})
        RETURN a
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, tail_number=tail_number)
                record = result.single()
                if record:
                    return Aircraft(**dict(record["a"]))
                return None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """
        Find all aircraft with optional limit.
        
        Args:
            limit: Maximum number of results to return
            
        Returns:
            List of Aircraft instances
        """
        query = """
        MATCH (a:Aircraft)
        RETURN a
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, limit=limit)
                return [Aircraft(**dict(record["a"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def update(self, aircraft: Aircraft) -> Aircraft:
        """
        Update an existing aircraft.
        
        Args:
            aircraft: Aircraft model with updated values
            
        Returns:
            Updated Aircraft instance
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
            with self.connection.get_session() as session:
                result = session.run(query, **aircraft.model_dump())
                record = result.single()
                if record:
                    return Aircraft(**dict(record["a"]))
                raise NotFoundError(f"Aircraft not found: {aircraft.aircraft_id}")
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Error updating aircraft: {str(e)}")
    
    def delete(self, aircraft_id: str) -> bool:
        """
        Delete an aircraft by ID.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            True if deleted, False if not found
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        DETACH DELETE a
        RETURN count(a) as deleted_count
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                record = result.single()
                return record["deleted_count"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Error deleting aircraft: {str(e)}")
    
    def get_systems(self, aircraft_id: str) -> List[System]:
        """
        Get all systems for an aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            List of System instances
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)
        RETURN s
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                return [System(**dict(record["s"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding systems: {str(e)}")
    
    def get_flights(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """
        Get flights operated by an aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of results
            
        Returns:
            List of Flight instances
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:OPERATES_FLIGHT]->(f:Flight)
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, aircraft_id=aircraft_id, limit=limit)
                return [Flight(**dict(record["f"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding flights: {str(e)}")
    
    def get_maintenance_events(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Get maintenance events for an aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of results
            
        Returns:
            List of MaintenanceEvent instances
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})<-[:AFFECTS_AIRCRAFT]-(m:MaintenanceEvent)
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, aircraft_id=aircraft_id, limit=limit)
                return [MaintenanceEvent(**dict(record["m"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding maintenance events: {str(e)}")


class FlightRepository:
    """Repository for Flight entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """
        Initialize repository with Neo4j connection.
        
        Args:
            connection: Neo4jConnection instance
        """
        self.connection = connection
    
    def create(self, flight: Flight) -> Flight:
        """
        Create a new flight in the database.
        
        Args:
            flight: Flight model instance
            
        Returns:
            Created Flight instance
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
            with self.connection.get_session() as session:
                result = session.run(query, **flight.model_dump())
                record = result.single()
                if record:
                    return Flight(**dict(record["f"]))
                raise QueryError("Failed to create flight")
        except Exception as e:
            raise QueryError(f"Error creating flight: {str(e)}")
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """
        Find flight by ID.
        
        Args:
            flight_id: Flight identifier
            
        Returns:
            Flight instance or None if not found
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        RETURN f
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, flight_id=flight_id)
                record = result.single()
                if record:
                    return Flight(**dict(record["f"]))
                return None
        except Exception as e:
            raise QueryError(f"Error finding flight: {str(e)}")
    
    def find_by_flight_number(self, flight_number: str, limit: int = 100) -> List[Flight]:
        """
        Find flights by flight number.
        
        Args:
            flight_number: Flight number
            limit: Maximum number of results
            
        Returns:
            List of Flight instances
        """
        query = """
        MATCH (f:Flight {flight_number: $flight_number})
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, flight_number=flight_number, limit=limit)
                return [Flight(**dict(record["f"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding flights: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Flight]:
        """
        Find all flights with optional limit.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of Flight instances
        """
        query = """
        MATCH (f:Flight)
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, limit=limit)
                return [Flight(**dict(record["f"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding flights: {str(e)}")
    
    def get_delays(self, flight_id: str) -> List[Delay]:
        """
        Get delays for a flight.
        
        Args:
            flight_id: Flight identifier
            
        Returns:
            List of Delay instances
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})-[:HAS_DELAY]->(d:Delay)
        RETURN d
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, flight_id=flight_id)
                return [Delay(**dict(record["d"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding delays: {str(e)}")


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """
        Initialize repository with Neo4j connection.
        
        Args:
            connection: Neo4jConnection instance
        """
        self.connection = connection
    
    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """
        Create a new maintenance event.
        
        Args:
            event: MaintenanceEvent model instance
            
        Returns:
            Created MaintenanceEvent instance
        """
        query = """
        MERGE (m:MaintenanceEvent {event_id: $event_id})
        SET m.aircraft_id = $aircraft_id,
            m.system_id = $system_id,
            m.component_id = $component_id,
            m.fault = $fault,
            m.severity = $severity,
            m.reported_at = $reported_at,
            m.corrective_action = $corrective_action
        RETURN m
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, **event.model_dump())
                record = result.single()
                if record:
                    return MaintenanceEvent(**dict(record["m"]))
                raise QueryError("Failed to create maintenance event")
        except Exception as e:
            raise QueryError(f"Error creating maintenance event: {str(e)}")
    
    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """
        Find maintenance event by ID.
        
        Args:
            event_id: Event identifier
            
        Returns:
            MaintenanceEvent instance or None if not found
        """
        query = """
        MATCH (m:MaintenanceEvent {event_id: $event_id})
        RETURN m
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, event_id=event_id)
                record = result.single()
                if record:
                    return MaintenanceEvent(**dict(record["m"]))
                return None
        except Exception as e:
            raise QueryError(f"Error finding maintenance event: {str(e)}")
    
    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find maintenance events by severity level.
        
        Args:
            severity: Severity level (e.g., CRITICAL, WARNING)
            limit: Maximum number of results
            
        Returns:
            List of MaintenanceEvent instances
        """
        query = """
        MATCH (m:MaintenanceEvent {severity: $severity})
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, severity=severity, limit=limit)
                return [MaintenanceEvent(**dict(record["m"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding maintenance events: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find all maintenance events with optional limit.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of MaintenanceEvent instances
        """
        query = """
        MATCH (m:MaintenanceEvent)
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        try:
            with self.connection.get_session() as session:
                result = session.run(query, limit=limit)
                return [MaintenanceEvent(**dict(record["m"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding maintenance events: {str(e)}")
