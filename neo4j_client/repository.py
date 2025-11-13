"""Repository pattern for aircraft data queries."""

from typing import List, Optional
from neo4j import Session
from .models import Aircraft, Airport, Flight, System, Component, Sensor, MaintenanceEvent, Delay
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entity operations."""
    
    def __init__(self, session: Session):
        """
        Initialize repository with Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """
        Create a new aircraft in the database.
        
        Args:
            aircraft: Aircraft model instance
            
        Returns:
            Created aircraft
            
        Raises:
            QueryError: If query execution fails
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
                return Aircraft(**dict(record["a"]))
            raise QueryError("Failed to create aircraft")
        except Exception as e:
            raise QueryError(f"Failed to create aircraft: {e}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """
        Find aircraft by ID.
        
        Args:
            aircraft_id: Unique aircraft identifier
            
        Returns:
            Aircraft if found, None otherwise
        """
        query = "MATCH (a:Aircraft {aircraft_id: $aircraft_id}) RETURN a"
        result = self.session.run(query, aircraft_id=aircraft_id)
        record = result.single()
        if record:
            return Aircraft(**dict(record["a"]))
        return None
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """
        Find aircraft by tail number.
        
        Args:
            tail_number: Aircraft registration/tail number
            
        Returns:
            Aircraft if found, None otherwise
        """
        query = "MATCH (a:Aircraft {tail_number: $tail_number}) RETURN a"
        result = self.session.run(query, tail_number=tail_number)
        record = result.single()
        if record:
            return Aircraft(**dict(record["a"]))
        return None
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """
        Get all aircraft with optional limit.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of aircraft
        """
        query = "MATCH (a:Aircraft) RETURN a LIMIT $limit"
        result = self.session.run(query, limit=limit)
        return [Aircraft(**dict(record["a"])) for record in result]
    
    def find_by_operator(self, operator: str, limit: int = 100) -> List[Aircraft]:
        """
        Find all aircraft by operator.
        
        Args:
            operator: Operating airline name
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of aircraft
        """
        query = "MATCH (a:Aircraft {operator: $operator}) RETURN a LIMIT $limit"
        result = self.session.run(query, operator=operator, limit=limit)
        return [Aircraft(**dict(record["a"])) for record in result]
    
    def delete(self, aircraft_id: str) -> bool:
        """
        Delete aircraft by ID.
        
        Args:
            aircraft_id: Unique aircraft identifier
            
        Returns:
            True if deleted, False if not found
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        DELETE a
        RETURN count(a) as deleted
        """
        result = self.session.run(query, aircraft_id=aircraft_id)
        record = result.single()
        return record["deleted"] > 0 if record else False


class FlightRepository:
    """Repository for Flight entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session."""
        self.session = session
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """Find flight by ID."""
        query = "MATCH (f:Flight {flight_id: $flight_id}) RETURN f"
        result = self.session.run(query, flight_id=flight_id)
        record = result.single()
        if record:
            return Flight(**dict(record["f"]))
        return None
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """
        Find all flights for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of flights ordered by scheduled departure (most recent first)
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:OPERATES_FLIGHT]->(f:Flight)
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
        return [Flight(**dict(record["f"])) for record in result]
    
    def find_by_route(self, origin: str, destination: str, limit: int = 100) -> List[Flight]:
        """
        Find flights by origin and destination.
        
        Args:
            origin: Origin airport code
            destination: Destination airport code
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of flights
        """
        query = """
        MATCH (f:Flight {origin: $origin, destination: $destination})
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        result = self.session.run(query, origin=origin, destination=destination, limit=limit)
        return [Flight(**dict(record["f"])) for record in result]
    
    def find_with_delays(self, min_delay_minutes: int = 30, limit: int = 100) -> List[Flight]:
        """
        Find flights with delays exceeding a threshold.
        
        Args:
            min_delay_minutes: Minimum delay duration in minutes
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of flights with delays
        """
        query = """
        MATCH (f:Flight)-[:HAS_DELAY]->(d:Delay)
        WHERE d.minutes >= $min_delay_minutes
        RETURN DISTINCT f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        result = self.session.run(query, min_delay_minutes=min_delay_minutes, limit=limit)
        return [Flight(**dict(record["f"])) for record in result]


class SystemRepository:
    """Repository for System entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session."""
        self.session = session
    
    def find_by_aircraft(self, aircraft_id: str) -> List[System]:
        """
        Find all systems for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            List of systems
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)
        RETURN s
        """
        result = self.session.run(query, aircraft_id=aircraft_id)
        return [System(**dict(record["s"])) for record in result]
    
    def find_by_id(self, system_id: str) -> Optional[System]:
        """Find system by ID."""
        query = "MATCH (s:System {system_id: $system_id}) RETURN s"
        result = self.session.run(query, system_id=system_id)
        record = result.single()
        if record:
            return System(**dict(record["s"]))
        return None


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session."""
        self.session = session
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find all maintenance events for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of maintenance events ordered by reported date (most recent first)
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})<-[:AFFECTS_AIRCRAFT]-(m:MaintenanceEvent)
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
        return [MaintenanceEvent(**dict(record["m"])) for record in result]
    
    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find maintenance events by severity level.
        
        Args:
            severity: Severity level (e.g., 'CRITICAL', 'WARNING')
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of maintenance events ordered by reported date (most recent first)
        """
        query = """
        MATCH (m:MaintenanceEvent {severity: $severity})
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        result = self.session.run(query, severity=severity, limit=limit)
        return [MaintenanceEvent(**dict(record["m"])) for record in result]
    
    def find_critical_events(self, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find all critical maintenance events.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of critical maintenance events
        """
        return self.find_by_severity("CRITICAL", limit=limit)


class AirportRepository:
    """Repository for Airport entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session."""
        self.session = session
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """
        Find airport by IATA code.
        
        Args:
            iata: IATA airport code (e.g., 'LAX')
            
        Returns:
            Airport if found, None otherwise
        """
        query = "MATCH (a:Airport {iata: $iata}) RETURN a"
        result = self.session.run(query, iata=iata)
        record = result.single()
        if record:
            return Airport(**dict(record["a"]))
        return None
    
    def find_by_icao(self, icao: str) -> Optional[Airport]:
        """
        Find airport by ICAO code.
        
        Args:
            icao: ICAO airport code (e.g., 'KLAX')
            
        Returns:
            Airport if found, None otherwise
        """
        query = "MATCH (a:Airport {icao: $icao}) RETURN a"
        result = self.session.run(query, icao=icao)
        record = result.single()
        if record:
            return Airport(**dict(record["a"]))
        return None
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """
        Get all airports with optional limit.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of airports
        """
        query = "MATCH (a:Airport) RETURN a ORDER BY a.name LIMIT $limit"
        result = self.session.run(query, limit=limit)
        return [Airport(**dict(record["a"])) for record in result]
