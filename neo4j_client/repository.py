"""Repository pattern for Neo4j aircraft data queries."""

from typing import List, Optional
from neo4j import Session
from .models import Aircraft, Flight, MaintenanceEvent, System, Airport, Delay
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entity operations.
    
    Provides CRUD operations for Aircraft nodes using parameterized queries.
    """
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """Create a new aircraft node.
        
        Args:
            aircraft: Aircraft model to create
            
        Returns:
            Created Aircraft model
            
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
            return Aircraft(**record["a"])
        except Exception as e:
            raise QueryError(f"Failed to create aircraft: {e}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """Find aircraft by ID.
        
        Args:
            aircraft_id: Unique aircraft identifier
            
        Returns:
            Aircraft model if found, None otherwise
            
        Raises:
            QueryError: If query execution fails
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
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """Find aircraft by tail number.
        
        Args:
            tail_number: Aircraft tail number
            
        Returns:
            Aircraft model if found, None otherwise
            
        Raises:
            QueryError: If query execution fails
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
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """Find all aircraft with optional limit.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of Aircraft models
            
        Raises:
            QueryError: If query execution fails
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
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def find_by_operator(self, operator: str, limit: int = 100) -> List[Aircraft]:
        """Find aircraft by operator.
        
        Args:
            operator: Operating airline name
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of Aircraft models
            
        Raises:
            QueryError: If query execution fails
        """
        query = """
        MATCH (a:Aircraft {operator: $operator})
        RETURN a
        LIMIT $limit
        """
        try:
            result = self.session.run(query, operator=operator, limit=limit)
            return [Aircraft(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find aircraft by operator: {e}")
    
    def update(self, aircraft: Aircraft) -> Aircraft:
        """Update an existing aircraft.
        
        Args:
            aircraft: Aircraft model with updated data
            
        Returns:
            Updated Aircraft model
            
        Raises:
            NotFoundError: If aircraft not found
            QueryError: If query execution fails
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
            return Aircraft(**record["a"])
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Failed to update aircraft: {e}")
    
    def delete(self, aircraft_id: str) -> bool:
        """Delete an aircraft by ID.
        
        Args:
            aircraft_id: Unique aircraft identifier
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            QueryError: If query execution fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        DETACH DELETE a
        RETURN count(a) as deleted
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            return record["deleted"] > 0
        except Exception as e:
            raise QueryError(f"Failed to delete aircraft: {e}")


class FlightRepository:
    """Repository for Flight entity operations.
    
    Provides query operations for Flight nodes and relationships.
    """
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """Find flight by ID.
        
        Args:
            flight_id: Unique flight identifier
            
        Returns:
            Flight model if found, None otherwise
            
        Raises:
            QueryError: If query execution fails
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
            raise QueryError(f"Failed to find flight: {e}")
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """Find all flights for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of Flight models ordered by scheduled departure (most recent first)
            
        Raises:
            QueryError: If query execution fails
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
            raise QueryError(f"Failed to find flights for aircraft: {e}")
    
    def find_by_flight_number(self, flight_number: str, limit: int = 100) -> List[Flight]:
        """Find flights by flight number.
        
        Args:
            flight_number: Flight number (e.g., "AA100")
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of Flight models
            
        Raises:
            QueryError: If query execution fails
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
            raise QueryError(f"Failed to find flights by number: {e}")
    
    def find_by_route(
        self,
        origin: str,
        destination: str,
        limit: int = 100
    ) -> List[Flight]:
        """Find flights by origin and destination.
        
        Args:
            origin: Origin airport code
            destination: Destination airport code
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of Flight models
            
        Raises:
            QueryError: If query execution fails
        """
        query = """
        MATCH (f:Flight {origin: $origin, destination: $destination})
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(
                query,
                origin=origin,
                destination=destination,
                limit=limit
            )
            return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find flights by route: {e}")
    
    def find_with_delays(self, min_delay_minutes: int = 30, limit: int = 100) -> List[dict]:
        """Find flights with delays.
        
        Args:
            min_delay_minutes: Minimum delay in minutes (default: 30)
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of dictionaries with flight and delay information
            
        Raises:
            QueryError: If query execution fails
        """
        query = """
        MATCH (f:Flight)-[:HAS_DELAY]->(d:Delay)
        WHERE d.minutes >= $min_delay_minutes
        RETURN f, d
        ORDER BY d.minutes DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, min_delay_minutes=min_delay_minutes, limit=limit)
            flights_with_delays = []
            for record in result:
                flight = Flight(**record["f"])
                delay = Delay(**record["d"])
                flights_with_delays.append({
                    "flight": flight,
                    "delay": delay
                })
            return flights_with_delays
        except Exception as e:
            raise QueryError(f"Failed to find flights with delays: {e}")


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations.
    
    Provides query operations for MaintenanceEvent nodes and relationships.
    """
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """Find maintenance event by ID.
        
        Args:
            event_id: Unique event identifier
            
        Returns:
            MaintenanceEvent model if found, None otherwise
            
        Raises:
            QueryError: If query execution fails
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
            raise QueryError(f"Failed to find maintenance event: {e}")
    
    def find_by_aircraft(
        self,
        aircraft_id: str,
        severity: Optional[str] = None,
        limit: int = 100
    ) -> List[MaintenanceEvent]:
        """Find maintenance events for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            severity: Optional severity filter (e.g., "CRITICAL")
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of MaintenanceEvent models ordered by reported_at (most recent first)
            
        Raises:
            QueryError: If query execution fails
        """
        if severity:
            query = """
            MATCH (a:Aircraft {aircraft_id: $aircraft_id})<-[:AFFECTS_AIRCRAFT]-(m:MaintenanceEvent)
            WHERE m.severity = $severity
            RETURN m
            ORDER BY m.reported_at DESC
            LIMIT $limit
            """
            params = {"aircraft_id": aircraft_id, "severity": severity, "limit": limit}
        else:
            query = """
            MATCH (a:Aircraft {aircraft_id: $aircraft_id})<-[:AFFECTS_AIRCRAFT]-(m:MaintenanceEvent)
            RETURN m
            ORDER BY m.reported_at DESC
            LIMIT $limit
            """
            params = {"aircraft_id": aircraft_id, "limit": limit}
        
        try:
            result = self.session.run(query, **params)
            return [MaintenanceEvent(**record["m"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find maintenance events for aircraft: {e}")
    
    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find maintenance events by severity level.
        
        Args:
            severity: Severity level (e.g., "CRITICAL", "WARNING")
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of MaintenanceEvent models ordered by reported_at (most recent first)
            
        Raises:
            QueryError: If query execution fails
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
            raise QueryError(f"Failed to find maintenance events by severity: {e}")
    
    def find_by_system(self, system_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find maintenance events for a specific system.
        
        Args:
            system_id: System identifier
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of MaintenanceEvent models ordered by reported_at (most recent first)
            
        Raises:
            QueryError: If query execution fails
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
            raise QueryError(f"Failed to find maintenance events for system: {e}")
    
    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """Create a new maintenance event.
        
        Args:
            event: MaintenanceEvent model to create
            
        Returns:
            Created MaintenanceEvent model
            
        Raises:
            QueryError: If query execution fails
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
            result = self.session.run(query, **event.model_dump())
            record = result.single()
            return MaintenanceEvent(**record["m"])
        except Exception as e:
            raise QueryError(f"Failed to create maintenance event: {e}")


class SystemRepository:
    """Repository for System entity operations.
    
    Provides query operations for System nodes and relationships.
    """
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def find_by_aircraft(self, aircraft_id: str) -> List[System]:
        """Find all systems for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            List of System models
            
        Raises:
            QueryError: If query execution fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)
        RETURN s
        ORDER BY s.name
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            return [System(**record["s"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find systems for aircraft: {e}")
    
    def find_by_id(self, system_id: str) -> Optional[System]:
        """Find system by ID.
        
        Args:
            system_id: Unique system identifier
            
        Returns:
            System model if found, None otherwise
            
        Raises:
            QueryError: If query execution fails
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
            raise QueryError(f"Failed to find system: {e}")


class AirportRepository:
    """Repository for Airport entity operations.
    
    Provides query operations for Airport nodes.
    """
    
    def __init__(self, session: Session):
        """Initialize repository with Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """Find airport by IATA code.
        
        Args:
            iata: IATA airport code (e.g., "LAX")
            
        Returns:
            Airport model if found, None otherwise
            
        Raises:
            QueryError: If query execution fails
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
            raise QueryError(f"Failed to find airport: {e}")
    
    def find_by_country(self, country: str, limit: int = 100) -> List[Airport]:
        """Find airports by country.
        
        Args:
            country: Country name
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of Airport models
            
        Raises:
            QueryError: If query execution fails
        """
        query = """
        MATCH (a:Airport {country: $country})
        RETURN a
        ORDER BY a.name
        LIMIT $limit
        """
        try:
            result = self.session.run(query, country=country, limit=limit)
            return [Airport(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find airports by country: {e}")
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """Find all airports.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of Airport models
            
        Raises:
            QueryError: If query execution fails
        """
        query = """
        MATCH (a:Airport)
        RETURN a
        ORDER BY a.name
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            return [Airport(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find airports: {e}")
