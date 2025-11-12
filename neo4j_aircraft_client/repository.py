"""
Repository pattern implementation for Neo4j aircraft data.

This module provides repository classes for each entity type, offering
clean CRUD operations with parameterized Cypher queries.
"""

from typing import List, Optional
from neo4j import Session
from .models import Aircraft, Airport, Flight, System, Component, Sensor, MaintenanceEvent, Delay
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """
    Repository for Aircraft entity operations.
    
    Provides CRUD operations for aircraft with parameterized queries
    to prevent SQL injection attacks.
    """
    
    def __init__(self, session: Session):
        """
        Initialize the repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """
        Create a new aircraft in the database.
        
        Args:
            aircraft: Aircraft object to create
            
        Returns:
            The created Aircraft object
            
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
                return Aircraft(**dict(record["a"]))
            raise QueryError("Failed to create aircraft")
        except Exception as e:
            raise QueryError(f"Error creating aircraft: {str(e)}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """
        Find an aircraft by its ID.
        
        Args:
            aircraft_id: Unique aircraft identifier
            
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
                return Aircraft(**dict(record["a"]))
            return None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """
        Find an aircraft by its tail number.
        
        Args:
            tail_number: Aircraft tail number
            
        Returns:
            Aircraft object if found, None otherwise
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Aircraft {tail_number: $tail_number})
        RETURN a
        """
        try:
            result = self.session.run(query, tail_number=tail_number)
            record = result.single()
            if record:
                return Aircraft(**dict(record["a"]))
            return None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """
        Find all aircraft in the database.
        
        Args:
            limit: Maximum number of results to return (default: 100)
            
        Returns:
            List of Aircraft objects
            
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
            return [Aircraft(**dict(record["a"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def update(self, aircraft: Aircraft) -> Aircraft:
        """
        Update an existing aircraft.
        
        Args:
            aircraft: Aircraft object with updated data
            
        Returns:
            The updated Aircraft object
            
        Raises:
            NotFoundError: If the aircraft doesn't exist
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
            if record:
                return Aircraft(**dict(record["a"]))
            raise NotFoundError(f"Aircraft with ID {aircraft.aircraft_id} not found")
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Error updating aircraft: {str(e)}")
    
    def delete(self, aircraft_id: str) -> bool:
        """
        Delete an aircraft by ID.
        
        Args:
            aircraft_id: Unique aircraft identifier
            
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
        except Exception as e:
            raise QueryError(f"Error deleting aircraft: {str(e)}")


class FlightRepository:
    """
    Repository for Flight entity operations.
    
    Provides CRUD operations for flights with parameterized queries.
    """
    
    def __init__(self, session: Session):
        """
        Initialize the repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def create(self, flight: Flight) -> Flight:
        """
        Create a new flight in the database.
        
        Args:
            flight: Flight object to create
            
        Returns:
            The created Flight object
            
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
                return Flight(**dict(record["f"]))
            raise QueryError("Failed to create flight")
        except Exception as e:
            raise QueryError(f"Error creating flight: {str(e)}")
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """
        Find a flight by its ID.
        
        Args:
            flight_id: Unique flight identifier
            
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
                return Flight(**dict(record["f"]))
            return None
        except Exception as e:
            raise QueryError(f"Error finding flight: {str(e)}")
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """
        Find all flights for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of results to return (default: 100)
            
        Returns:
            List of Flight objects
            
        Raises:
            QueryError: If the query fails
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
            raise QueryError(f"Error finding flights: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Flight]:
        """
        Find all flights in the database.
        
        Args:
            limit: Maximum number of results to return (default: 100)
            
        Returns:
            List of Flight objects
            
        Raises:
            QueryError: If the query fails
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
            raise QueryError(f"Error finding flights: {str(e)}")
    
    def delete(self, flight_id: str) -> bool:
        """
        Delete a flight by ID.
        
        Args:
            flight_id: Unique flight identifier
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        DETACH DELETE f
        RETURN count(f) as deleted
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Error deleting flight: {str(e)}")


class AirportRepository:
    """
    Repository for Airport entity operations.
    
    Provides CRUD operations for airports with parameterized queries.
    """
    
    def __init__(self, session: Session):
        """
        Initialize the repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def create(self, airport: Airport) -> Airport:
        """
        Create a new airport in the database.
        
        Args:
            airport: Airport object to create
            
        Returns:
            The created Airport object
            
        Raises:
            QueryError: If the query fails
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
            if record:
                return Airport(**dict(record["a"]))
            raise QueryError("Failed to create airport")
        except Exception as e:
            raise QueryError(f"Error creating airport: {str(e)}")
    
    def find_by_id(self, airport_id: str) -> Optional[Airport]:
        """
        Find an airport by its ID.
        
        Args:
            airport_id: Unique airport identifier
            
        Returns:
            Airport object if found, None otherwise
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Airport {airport_id: $airport_id})
        RETURN a
        """
        try:
            result = self.session.run(query, airport_id=airport_id)
            record = result.single()
            if record:
                return Airport(**dict(record["a"]))
            return None
        except Exception as e:
            raise QueryError(f"Error finding airport: {str(e)}")
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """
        Find an airport by its IATA code.
        
        Args:
            iata: IATA airport code (e.g., "LAX")
            
        Returns:
            Airport object if found, None otherwise
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Airport {iata: $iata})
        RETURN a
        """
        try:
            result = self.session.run(query, iata=iata)
            record = result.single()
            if record:
                return Airport(**dict(record["a"]))
            return None
        except Exception as e:
            raise QueryError(f"Error finding airport: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """
        Find all airports in the database.
        
        Args:
            limit: Maximum number of results to return (default: 100)
            
        Returns:
            List of Airport objects
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Airport)
        RETURN a
        ORDER BY a.name
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            return [Airport(**dict(record["a"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding airports: {str(e)}")


class SystemRepository:
    """
    Repository for System entity operations.
    
    Provides CRUD operations for aircraft systems with parameterized queries.
    """
    
    def __init__(self, session: Session):
        """
        Initialize the repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def create(self, system: System) -> System:
        """
        Create a new system in the database.
        
        Args:
            system: System object to create
            
        Returns:
            The created System object
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MERGE (s:System {system_id: $system_id})
        SET s.aircraft_id = $aircraft_id,
            s.name = $name,
            s.type = $type
        RETURN s
        """
        try:
            result = self.session.run(query, **system.model_dump())
            record = result.single()
            if record:
                return System(**dict(record["s"]))
            raise QueryError("Failed to create system")
        except Exception as e:
            raise QueryError(f"Error creating system: {str(e)}")
    
    def find_by_id(self, system_id: str) -> Optional[System]:
        """
        Find a system by its ID.
        
        Args:
            system_id: Unique system identifier
            
        Returns:
            System object if found, None otherwise
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (s:System {system_id: $system_id})
        RETURN s
        """
        try:
            result = self.session.run(query, system_id=system_id)
            record = result.single()
            if record:
                return System(**dict(record["s"]))
            return None
        except Exception as e:
            raise QueryError(f"Error finding system: {str(e)}")
    
    def find_by_aircraft(self, aircraft_id: str) -> List[System]:
        """
        Find all systems for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            List of System objects
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)
        RETURN s
        ORDER BY s.name
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            return [System(**dict(record["s"])) for record in result]
        except Exception as e:
            raise QueryError(f"Error finding systems: {str(e)}")


class MaintenanceEventRepository:
    """
    Repository for MaintenanceEvent entity operations.
    
    Provides CRUD operations for maintenance events with parameterized queries.
    """
    
    def __init__(self, session: Session):
        """
        Initialize the repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """
        Create a new maintenance event in the database.
        
        Args:
            event: MaintenanceEvent object to create
            
        Returns:
            The created MaintenanceEvent object
            
        Raises:
            QueryError: If the query fails
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
            if record:
                return MaintenanceEvent(**dict(record["m"]))
            raise QueryError("Failed to create maintenance event")
        except Exception as e:
            raise QueryError(f"Error creating maintenance event: {str(e)}")
    
    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """
        Find a maintenance event by its ID.
        
        Args:
            event_id: Unique event identifier
            
        Returns:
            MaintenanceEvent object if found, None otherwise
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (m:MaintenanceEvent {event_id: $event_id})
        RETURN m
        """
        try:
            result = self.session.run(query, event_id=event_id)
            record = result.single()
            if record:
                return MaintenanceEvent(**dict(record["m"]))
            return None
        except Exception as e:
            raise QueryError(f"Error finding maintenance event: {str(e)}")
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find all maintenance events for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of results to return (default: 100)
            
        Returns:
            List of MaintenanceEvent objects
            
        Raises:
            QueryError: If the query fails
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
            raise QueryError(f"Error finding maintenance events: {str(e)}")
    
    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find maintenance events by severity level.
        
        Args:
            severity: Severity level (e.g., "CRITICAL", "WARNING")
            limit: Maximum number of results to return (default: 100)
            
        Returns:
            List of MaintenanceEvent objects
            
        Raises:
            QueryError: If the query fails
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
            raise QueryError(f"Error finding maintenance events: {str(e)}")
