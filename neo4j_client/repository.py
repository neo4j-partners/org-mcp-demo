"""Repository pattern for querying Neo4j aircraft data."""

from typing import List, Optional
from neo4j import Session
from .models import (
    Aircraft, Airport, Flight, System, Component,
    Sensor, Reading, MaintenanceEvent, Delay
)
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entity operations."""
    
    def __init__(self, session: Session):
        """
        Initialize repository with a Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """
        Create a new aircraft node.
        
        Args:
            aircraft: Aircraft model instance
            
        Returns:
            Created aircraft
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
                return Aircraft(**record["a"])
            raise QueryError("Failed to create aircraft")
        except Exception as e:
            raise QueryError(f"Error creating aircraft: {e}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """
        Find aircraft by ID.
        
        Args:
            aircraft_id: Unique aircraft identifier
            
        Returns:
            Aircraft if found, None otherwise
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            if record:
                return Aircraft(**record["a"])
            return None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {e}")
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """
        Find aircraft by tail number.
        
        Args:
            tail_number: Aircraft registration/tail number
            
        Returns:
            Aircraft if found, None otherwise
        """
        query = """
        MATCH (a:Aircraft {tail_number: $tail_number})
        RETURN a
        """
        try:
            result = self.session.run(query, tail_number=tail_number)
            record = result.single()
            if record:
                return Aircraft(**record["a"])
            return None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {e}")
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """
        Find all aircraft.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of aircraft
        """
        query = """
        MATCH (a:Aircraft)
        RETURN a
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            return [Aircraft(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {e}")
    
    def get_flights(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """
        Get all flights for an aircraft.
        
        Args:
            aircraft_id: Unique aircraft identifier
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of flights
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:OPERATES_FLIGHT]->(f:Flight)
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
            return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error getting aircraft flights: {e}")
    
    def get_systems(self, aircraft_id: str) -> List[System]:
        """
        Get all systems for an aircraft.
        
        Args:
            aircraft_id: Unique aircraft identifier
            
        Returns:
            List of systems
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)
        RETURN s
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            return [System(**record["s"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error getting aircraft systems: {e}")
    
    def get_maintenance_events(
        self,
        aircraft_id: str,
        limit: int = 100
    ) -> List[MaintenanceEvent]:
        """
        Get maintenance events for an aircraft.
        
        Args:
            aircraft_id: Unique aircraft identifier
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of maintenance events
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})<-[:AFFECTS_AIRCRAFT]-(m:MaintenanceEvent)
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
            return [MaintenanceEvent(**record["m"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error getting maintenance events: {e}")


class FlightRepository:
    """Repository for Flight entity operations."""
    
    def __init__(self, session: Session):
        """
        Initialize repository with a Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """
        Find flight by ID.
        
        Args:
            flight_id: Unique flight identifier
            
        Returns:
            Flight if found, None otherwise
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        RETURN f
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
            record = result.single()
            if record:
                return Flight(**record["f"])
            return None
        except Exception as e:
            raise QueryError(f"Error finding flight: {e}")
    
    def find_by_flight_number(
        self,
        flight_number: str,
        limit: int = 100
    ) -> List[Flight]:
        """
        Find flights by flight number.
        
        Args:
            flight_number: Flight number (e.g., 'AA100')
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of flights
        """
        query = """
        MATCH (f:Flight {flight_number: $flight_number})
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, flight_number=flight_number, limit=limit)
            return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding flights: {e}")
    
    def get_delays(self, flight_id: str) -> List[Delay]:
        """
        Get delays for a flight.
        
        Args:
            flight_id: Unique flight identifier
            
        Returns:
            List of delays
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})-[:HAS_DELAY]->(d:Delay)
        RETURN d
        ORDER BY d.minutes DESC
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
            return [Delay(**record["d"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error getting flight delays: {e}")
    
    def find_with_delays(
        self,
        min_minutes: int = 30,
        limit: int = 100
    ) -> List[Flight]:
        """
        Find flights with significant delays.
        
        Args:
            min_minutes: Minimum delay minutes (default: 30)
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of delayed flights
        """
        query = """
        MATCH (f:Flight)-[:HAS_DELAY]->(d:Delay)
        WHERE d.minutes >= $min_minutes
        RETURN f
        ORDER BY d.minutes DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, min_minutes=min_minutes, limit=limit)
            return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding delayed flights: {e}")


class SystemRepository:
    """Repository for System entity operations."""
    
    def __init__(self, session: Session):
        """
        Initialize repository with a Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def find_by_id(self, system_id: str) -> Optional[System]:
        """
        Find system by ID.
        
        Args:
            system_id: Unique system identifier
            
        Returns:
            System if found, None otherwise
        """
        query = """
        MATCH (s:System {system_id: $system_id})
        RETURN s
        """
        try:
            result = self.session.run(query, system_id=system_id)
            record = result.single()
            if record:
                return System(**record["s"])
            return None
        except Exception as e:
            raise QueryError(f"Error finding system: {e}")
    
    def get_components(self, system_id: str) -> List[Component]:
        """
        Get all components for a system.
        
        Args:
            system_id: Unique system identifier
            
        Returns:
            List of components
        """
        query = """
        MATCH (s:System {system_id: $system_id})-[:HAS_COMPONENT]->(c:Component)
        RETURN c
        """
        try:
            result = self.session.run(query, system_id=system_id)
            return [Component(**record["c"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error getting system components: {e}")
    
    def get_sensors(self, system_id: str) -> List[Sensor]:
        """
        Get all sensors for a system.
        
        Args:
            system_id: Unique system identifier
            
        Returns:
            List of sensors
        """
        query = """
        MATCH (s:System {system_id: $system_id})-[:HAS_SENSOR]->(sensor:Sensor)
        RETURN sensor
        """
        try:
            result = self.session.run(query, system_id=system_id)
            return [Sensor(**record["sensor"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error getting system sensors: {e}")
    
    def get_maintenance_events(
        self,
        system_id: str,
        limit: int = 100
    ) -> List[MaintenanceEvent]:
        """
        Get maintenance events for a system.
        
        Args:
            system_id: Unique system identifier
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of maintenance events
        """
        query = """
        MATCH (s:System {system_id: $system_id})<-[:AFFECTS_SYSTEM]-(m:MaintenanceEvent)
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, system_id=system_id, limit=limit)
            return [MaintenanceEvent(**record["m"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error getting maintenance events: {e}")


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations."""
    
    def __init__(self, session: Session):
        """
        Initialize repository with a Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """
        Find maintenance event by ID.
        
        Args:
            event_id: Unique event identifier
            
        Returns:
            MaintenanceEvent if found, None otherwise
        """
        query = """
        MATCH (m:MaintenanceEvent {event_id: $event_id})
        RETURN m
        """
        try:
            result = self.session.run(query, event_id=event_id)
            record = result.single()
            if record:
                return MaintenanceEvent(**record["m"])
            return None
        except Exception as e:
            raise QueryError(f"Error finding maintenance event: {e}")
    
    def find_by_severity(
        self,
        severity: str,
        limit: int = 100
    ) -> List[MaintenanceEvent]:
        """
        Find maintenance events by severity level.
        
        Args:
            severity: Severity level (e.g., 'CRITICAL', 'WARNING')
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of maintenance events
        """
        query = """
        MATCH (m:MaintenanceEvent {severity: $severity})
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, severity=severity, limit=limit)
            return [MaintenanceEvent(**record["m"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding maintenance events: {e}")


class SensorRepository:
    """Repository for Sensor entity operations."""
    
    def __init__(self, session: Session):
        """
        Initialize repository with a Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def find_by_id(self, sensor_id: str) -> Optional[Sensor]:
        """
        Find sensor by ID.
        
        Args:
            sensor_id: Unique sensor identifier
            
        Returns:
            Sensor if found, None otherwise
        """
        query = """
        MATCH (s:Sensor {sensor_id: $sensor_id})
        RETURN s
        """
        try:
            result = self.session.run(query, sensor_id=sensor_id)
            record = result.single()
            if record:
                return Sensor(**record["s"])
            return None
        except Exception as e:
            raise QueryError(f"Error finding sensor: {e}")
    
    def get_readings(
        self,
        sensor_id: str,
        limit: int = 100
    ) -> List[Reading]:
        """
        Get recent readings for a sensor.
        
        Args:
            sensor_id: Unique sensor identifier
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of readings
        """
        query = """
        MATCH (r:Reading {sensor_id: $sensor_id})
        RETURN r
        ORDER BY r.timestamp DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, sensor_id=sensor_id, limit=limit)
            return [Reading(**record["r"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error getting sensor readings: {e}")


class AirportRepository:
    """Repository for Airport entity operations."""
    
    def __init__(self, session: Session):
        """
        Initialize repository with a Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """
        Find airport by IATA code.
        
        Args:
            iata: IATA airport code (e.g., 'LAX')
            
        Returns:
            Airport if found, None otherwise
        """
        query = """
        MATCH (a:Airport {iata: $iata})
        RETURN a
        """
        try:
            result = self.session.run(query, iata=iata)
            record = result.single()
            if record:
                return Airport(**record["a"])
            return None
        except Exception as e:
            raise QueryError(f"Error finding airport: {e}")
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """
        Find all airports.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of airports
        """
        query = """
        MATCH (a:Airport)
        RETURN a
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            return [Airport(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding airports: {e}")
