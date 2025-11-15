"""Repository pattern for Neo4j queries."""

from typing import List, Optional
from neo4j import Session
from .models import Aircraft, Airport, Flight, System, Component, Sensor, MaintenanceEvent, Delay
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """Create a new aircraft node.
        
        Args:
            aircraft: Aircraft model instance
            
        Returns:
            Created aircraft
            
        Raises:
            QueryError: If creation fails
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
            if not record:
                raise QueryError("Failed to create aircraft")
            return aircraft
        except Exception as e:
            raise QueryError(f"Error creating aircraft: {e}") from e
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """Find aircraft by ID.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            Aircraft if found, None otherwise
            
        Raises:
            QueryError: If query fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            if not record:
                return None
            node = record["a"]
            return Aircraft(**dict(node))
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {e}") from e
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """Find aircraft by tail number.
        
        Args:
            tail_number: Aircraft tail number
            
        Returns:
            Aircraft if found, None otherwise
            
        Raises:
            QueryError: If query fails
        """
        query = """
        MATCH (a:Aircraft {tail_number: $tail_number})
        RETURN a
        """
        try:
            result = self.session.run(query, tail_number=tail_number)
            record = result.single()
            if not record:
                return None
            node = record["a"]
            return Aircraft(**dict(node))
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {e}") from e
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """Find all aircraft with optional limit.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of aircraft
            
        Raises:
            QueryError: If query fails
        """
        query = """
        MATCH (a:Aircraft)
        RETURN a
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            return [Aircraft(**dict(record["a"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {e}") from e
    
    def update(self, aircraft: Aircraft) -> Aircraft:
        """Update an existing aircraft.
        
        Args:
            aircraft: Aircraft model with updated data
            
        Returns:
            Updated aircraft
            
        Raises:
            NotFoundError: If aircraft doesn't exist
            QueryError: If update fails
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
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Error updating aircraft: {e}") from e
    
    def delete(self, aircraft_id: str) -> bool:
        """Delete an aircraft by ID.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            QueryError: If deletion fails
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
            raise QueryError(f"Error deleting aircraft: {e}") from e


class FlightRepository:
    """Repository for Flight entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, flight: Flight) -> Flight:
        """Create a new flight node.
        
        Args:
            flight: Flight model instance
            
        Returns:
            Created flight
            
        Raises:
            QueryError: If creation fails
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
            if not record:
                raise QueryError("Failed to create flight")
            return flight
        except Exception as e:
            raise QueryError(f"Error creating flight: {e}") from e
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """Find flight by ID.
        
        Args:
            flight_id: Flight identifier
            
        Returns:
            Flight if found, None otherwise
            
        Raises:
            QueryError: If query fails
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        RETURN f
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
            record = result.single()
            if not record:
                return None
            node = record["f"]
            return Flight(**dict(node))
        except Exception as e:
            raise QueryError(f"Error finding flight: {e}") from e
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """Find all flights for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of flights
            
        Raises:
            QueryError: If query fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:OPERATES_FLIGHT]->(f:Flight)
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
            return [Flight(**dict(record["f"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding flights: {e}") from e
    
    def find_all(self, limit: int = 100) -> List[Flight]:
        """Find all flights with optional limit.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of flights
            
        Raises:
            QueryError: If query fails
        """
        query = """
        MATCH (f:Flight)
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            return [Flight(**dict(record["f"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding flights: {e}") from e
    
    def delete(self, flight_id: str) -> bool:
        """Delete a flight by ID.
        
        Args:
            flight_id: Flight identifier
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            QueryError: If deletion fails
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        DETACH DELETE f
        RETURN count(f) as deleted
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
            record = result.single()
            return record["deleted"] > 0
        except Exception as e:
            raise QueryError(f"Error deleting flight: {e}") from e


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """Create a new maintenance event node.
        
        Args:
            event: MaintenanceEvent model instance
            
        Returns:
            Created maintenance event
            
        Raises:
            QueryError: If creation fails
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
            if not record:
                raise QueryError("Failed to create maintenance event")
            return event
        except Exception as e:
            raise QueryError(f"Error creating maintenance event: {e}") from e
    
    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """Find maintenance event by ID.
        
        Args:
            event_id: Event identifier
            
        Returns:
            MaintenanceEvent if found, None otherwise
            
        Raises:
            QueryError: If query fails
        """
        query = """
        MATCH (m:MaintenanceEvent {event_id: $event_id})
        RETURN m
        """
        try:
            result = self.session.run(query, event_id=event_id)
            record = result.single()
            if not record:
                return None
            node = record["m"]
            return MaintenanceEvent(**dict(node))
        except Exception as e:
            raise QueryError(f"Error finding maintenance event: {e}") from e
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find all maintenance events for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of maintenance events
            
        Raises:
            QueryError: If query fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})<-[:AFFECTS_AIRCRAFT]-(m:MaintenanceEvent)
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
            return [MaintenanceEvent(**dict(record["m"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding maintenance events: {e}") from e
    
    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find maintenance events by severity level.
        
        Args:
            severity: Severity level (e.g., "CRITICAL", "WARNING")
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of maintenance events
            
        Raises:
            QueryError: If query fails
        """
        query = """
        MATCH (m:MaintenanceEvent {severity: $severity})
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, severity=severity, limit=limit)
            return [MaintenanceEvent(**dict(record["m"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding maintenance events: {e}") from e


class AirportRepository:
    """Repository for Airport entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, airport: Airport) -> Airport:
        """Create a new airport node.
        
        Args:
            airport: Airport model instance
            
        Returns:
            Created airport
            
        Raises:
            QueryError: If creation fails
        """
        query = """
        MERGE (a:Airport {airport_id: $airport_id})
        SET a.iata = $iata,
            a.icao = $icao,
            a.name = $name,
            a.city = $city,
            a.country = $country,
            a.lat = $lat,
            a.lon = $lon
        RETURN a
        """
        try:
            result = self.session.run(query, **airport.model_dump())
            record = result.single()
            if not record:
                raise QueryError("Failed to create airport")
            return airport
        except Exception as e:
            raise QueryError(f"Error creating airport: {e}") from e
    
    def find_by_id(self, airport_id: str) -> Optional[Airport]:
        """Find airport by ID.
        
        Args:
            airport_id: Airport identifier
            
        Returns:
            Airport if found, None otherwise
            
        Raises:
            QueryError: If query fails
        """
        query = """
        MATCH (a:Airport {airport_id: $airport_id})
        RETURN a
        """
        try:
            result = self.session.run(query, airport_id=airport_id)
            record = result.single()
            if not record:
                return None
            node = record["a"]
            return Airport(**dict(node))
        except Exception as e:
            raise QueryError(f"Error finding airport: {e}") from e
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """Find airport by IATA code.
        
        Args:
            iata: IATA airport code
            
        Returns:
            Airport if found, None otherwise
            
        Raises:
            QueryError: If query fails
        """
        query = """
        MATCH (a:Airport {iata: $iata})
        RETURN a
        """
        try:
            result = self.session.run(query, iata=iata)
            record = result.single()
            if not record:
                return None
            node = record["a"]
            return Airport(**dict(node))
        except Exception as e:
            raise QueryError(f"Error finding airport: {e}") from e
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """Find all airports with optional limit.
        
        Args:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of airports
            
        Raises:
            QueryError: If query fails
        """
        query = """
        MATCH (a:Airport)
        RETURN a
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            return [Airport(**dict(record["a"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding airports: {e}") from e
