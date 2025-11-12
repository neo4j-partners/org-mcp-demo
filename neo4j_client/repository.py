"""Repository pattern implementations for Neo4j queries."""

from typing import List, Optional
from neo4j_client.connection import Neo4jConnection
from neo4j_client.models import (
    Aircraft,
    Flight,
    Airport,
    System,
    MaintenanceEvent,
)
from neo4j_client.exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """Initialize repository with a Neo4j connection.
        
        Args:
            connection: Active Neo4j connection
        """
        self.connection = connection
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """Create a new aircraft in the database.
        
        Args:
            aircraft: Aircraft object to create
            
        Returns:
            The created aircraft
            
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
                    return aircraft
                raise QueryError("Failed to create aircraft")
        except Exception as e:
            raise QueryError(f"Error creating aircraft: {str(e)}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """Find an aircraft by its ID.
        
        Args:
            aircraft_id: Aircraft ID to search for
            
        Returns:
            Aircraft if found, None otherwise
            
        Raises:
            QueryError: If the query fails
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
                    node = record["a"]
                    return Aircraft(
                        aircraft_id=node["aircraft_id"],
                        tail_number=node["tail_number"],
                        icao24=node["icao24"],
                        model=node["model"],
                        operator=node["operator"],
                        manufacturer=node["manufacturer"]
                    )
                return None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """Find an aircraft by its tail number.
        
        Args:
            tail_number: Aircraft tail number to search for
            
        Returns:
            Aircraft if found, None otherwise
            
        Raises:
            QueryError: If the query fails
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
                    node = record["a"]
                    return Aircraft(
                        aircraft_id=node["aircraft_id"],
                        tail_number=node["tail_number"],
                        icao24=node["icao24"],
                        model=node["model"],
                        operator=node["operator"],
                        manufacturer=node["manufacturer"]
                    )
                return None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """Find all aircraft with optional limit.
        
        Args:
            limit: Maximum number of aircraft to return (default: 100)
            
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
            with self.connection.session() as session:
                result = session.run(query, limit=limit)
                aircraft_list = []
                for record in result:
                    node = record["a"]
                    aircraft_list.append(Aircraft(
                        aircraft_id=node["aircraft_id"],
                        tail_number=node["tail_number"],
                        icao24=node["icao24"],
                        model=node["model"],
                        operator=node["operator"],
                        manufacturer=node["manufacturer"]
                    ))
                return aircraft_list
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def find_by_operator(self, operator: str, limit: int = 100) -> List[Aircraft]:
        """Find all aircraft operated by a specific operator.
        
        Args:
            operator: Operator name to search for
            limit: Maximum number of aircraft to return (default: 100)
            
        Returns:
            List of Aircraft objects
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Aircraft {operator: $operator})
        RETURN a
        LIMIT $limit
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, operator=operator, limit=limit)
                aircraft_list = []
                for record in result:
                    node = record["a"]
                    aircraft_list.append(Aircraft(
                        aircraft_id=node["aircraft_id"],
                        tail_number=node["tail_number"],
                        icao24=node["icao24"],
                        model=node["model"],
                        operator=node["operator"],
                        manufacturer=node["manufacturer"]
                    ))
                return aircraft_list
        except Exception as e:
            raise QueryError(f"Error finding aircraft by operator: {str(e)}")
    
    def update(self, aircraft: Aircraft) -> Aircraft:
        """Update an existing aircraft.
        
        Args:
            aircraft: Aircraft object with updated values
            
        Returns:
            The updated aircraft
            
        Raises:
            NotFoundError: If aircraft doesn't exist
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
                if not record:
                    raise NotFoundError(f"Aircraft {aircraft.aircraft_id} not found")
                return aircraft
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Error updating aircraft: {str(e)}")
    
    def delete(self, aircraft_id: str) -> bool:
        """Delete an aircraft by ID.
        
        Args:
            aircraft_id: Aircraft ID to delete
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        DELETE a
        RETURN count(a) as deleted
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                record = result.single()
                return record["deleted"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Error deleting aircraft: {str(e)}")


class FlightRepository:
    """Repository for Flight entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """Initialize repository with a Neo4j connection.
        
        Args:
            connection: Active Neo4j connection
        """
        self.connection = connection
    
    def find_by_aircraft_id(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """Find all flights for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft ID to search for
            limit: Maximum number of flights to return (default: 100)
            
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
            with self.connection.session() as session:
                result = session.run(query, aircraft_id=aircraft_id, limit=limit)
                flights = []
                for record in result:
                    node = record["f"]
                    flights.append(Flight(
                        flight_id=node["flight_id"],
                        flight_number=node["flight_number"],
                        aircraft_id=node["aircraft_id"],
                        operator=node["operator"],
                        origin=node["origin"],
                        destination=node["destination"],
                        scheduled_departure=node["scheduled_departure"],
                        scheduled_arrival=node["scheduled_arrival"]
                    ))
                return flights
        except Exception as e:
            raise QueryError(f"Error finding flights: {str(e)}")
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """Find a flight by its ID.
        
        Args:
            flight_id: Flight ID to search for
            
        Returns:
            Flight if found, None otherwise
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        RETURN f
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, flight_id=flight_id)
                record = result.single()
                if record:
                    node = record["f"]
                    return Flight(
                        flight_id=node["flight_id"],
                        flight_number=node["flight_number"],
                        aircraft_id=node["aircraft_id"],
                        operator=node["operator"],
                        origin=node["origin"],
                        destination=node["destination"],
                        scheduled_departure=node["scheduled_departure"],
                        scheduled_arrival=node["scheduled_arrival"]
                    )
                return None
        except Exception as e:
            raise QueryError(f"Error finding flight: {str(e)}")


class AirportRepository:
    """Repository for Airport entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """Initialize repository with a Neo4j connection.
        
        Args:
            connection: Active Neo4j connection
        """
        self.connection = connection
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """Find an airport by its IATA code.
        
        Args:
            iata: IATA airport code (e.g., "LAX")
            
        Returns:
            Airport if found, None otherwise
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Airport {iata: $iata})
        RETURN a
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, iata=iata)
                record = result.single()
                if record:
                    node = record["a"]
                    return Airport(
                        airport_id=node["airport_id"],
                        iata=node["iata"],
                        icao=node["icao"],
                        name=node["name"],
                        city=node["city"],
                        country=node["country"],
                        lat=node["lat"],
                        lon=node["lon"]
                    )
                return None
        except Exception as e:
            raise QueryError(f"Error finding airport: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """Find all airports with optional limit.
        
        Args:
            limit: Maximum number of airports to return (default: 100)
            
        Returns:
            List of Airport objects
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Airport)
        RETURN a
        LIMIT $limit
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, limit=limit)
                airports = []
                for record in result:
                    node = record["a"]
                    airports.append(Airport(
                        airport_id=node["airport_id"],
                        iata=node["iata"],
                        icao=node["icao"],
                        name=node["name"],
                        city=node["city"],
                        country=node["country"],
                        lat=node["lat"],
                        lon=node["lon"]
                    ))
                return airports
        except Exception as e:
            raise QueryError(f"Error finding airports: {str(e)}")


class SystemRepository:
    """Repository for System entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """Initialize repository with a Neo4j connection.
        
        Args:
            connection: Active Neo4j connection
        """
        self.connection = connection
    
    def find_by_aircraft_id(self, aircraft_id: str) -> List[System]:
        """Find all systems for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft ID to search for
            
        Returns:
            List of System objects
            
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)
        RETURN s
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                systems = []
                for record in result:
                    node = record["s"]
                    systems.append(System(
                        system_id=node["system_id"],
                        aircraft_id=node["aircraft_id"],
                        name=node["name"],
                        type=node["type"]
                    ))
                return systems
        except Exception as e:
            raise QueryError(f"Error finding systems: {str(e)}")


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """Initialize repository with a Neo4j connection.
        
        Args:
            connection: Active Neo4j connection
        """
        self.connection = connection
    
    def find_by_aircraft_id(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find all maintenance events for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft ID to search for
            limit: Maximum number of events to return (default: 100)
            
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
            with self.connection.session() as session:
                result = session.run(query, aircraft_id=aircraft_id, limit=limit)
                events = []
                for record in result:
                    node = record["m"]
                    events.append(MaintenanceEvent(
                        event_id=node["event_id"],
                        aircraft_id=node["aircraft_id"],
                        system_id=node["system_id"],
                        component_id=node["component_id"],
                        fault=node["fault"],
                        severity=node["severity"],
                        reported_at=node["reported_at"],
                        corrective_action=node["corrective_action"]
                    ))
                return events
        except Exception as e:
            raise QueryError(f"Error finding maintenance events: {str(e)}")
    
    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find all maintenance events by severity level.
        
        Args:
            severity: Severity level (e.g., "CRITICAL", "WARNING")
            limit: Maximum number of events to return (default: 100)
            
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
            with self.connection.session() as session:
                result = session.run(query, severity=severity, limit=limit)
                events = []
                for record in result:
                    node = record["m"]
                    events.append(MaintenanceEvent(
                        event_id=node["event_id"],
                        aircraft_id=node["aircraft_id"],
                        system_id=node["system_id"],
                        component_id=node["component_id"],
                        fault=node["fault"],
                        severity=node["severity"],
                        reported_at=node["reported_at"],
                        corrective_action=node["corrective_action"]
                    ))
                return events
        except Exception as e:
            raise QueryError(f"Error finding maintenance events: {str(e)}")
