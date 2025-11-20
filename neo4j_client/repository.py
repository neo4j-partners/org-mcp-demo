"""
Repository pattern implementation for Neo4j aviation database queries.

This module provides repository classes for each entity type with CRUD operations
and domain-specific query methods. All Cypher queries use parameterization for security.
"""

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
        """Initialize repository with database connection."""
        self.connection = connection
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """
        Retrieve all aircraft with optional limit.
        
        Args:
            limit: Maximum number of aircraft to return (default: 100)
        
        Returns:
            List of Aircraft objects
        """
        query = """
        MATCH (a:Aircraft)
        RETURN a
        ORDER BY a.tail_number
        LIMIT $limit
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, limit=limit)
                return [Aircraft(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find aircraft: {str(e)}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """
        Find aircraft by ID.
        
        Args:
            aircraft_id: Unique aircraft identifier
        
        Returns:
            Aircraft object if found, None otherwise
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                record = result.single()
                return Aircraft(**record["a"]) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find aircraft by ID: {str(e)}")
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """
        Find aircraft by tail number.
        
        Args:
            tail_number: Aircraft tail number
        
        Returns:
            Aircraft object if found, None otherwise
        """
        query = """
        MATCH (a:Aircraft {tail_number: $tail_number})
        RETURN a
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, tail_number=tail_number)
                record = result.single()
                return Aircraft(**record["a"]) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find aircraft by tail number: {str(e)}")
    
    def get_systems(self, aircraft_id: str) -> List[System]:
        """
        Get all systems for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
        
        Returns:
            List of System objects
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)
        RETURN s
        ORDER BY s.name
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                return [System(**record["s"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to get aircraft systems: {str(e)}")
    
    def get_components(self, aircraft_id: str) -> List[Component]:
        """
        Get all components for a specific aircraft (across all systems).
        
        Args:
            aircraft_id: Aircraft identifier
        
        Returns:
            List of Component objects
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)
              -[:HAS_COMPONENT]->(c:Component)
        RETURN c
        ORDER BY c.name
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, aircraft_id=aircraft_id)
                return [Component(**record["c"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to get aircraft components: {str(e)}")


class AirportRepository:
    """Repository for Airport entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """Initialize repository with database connection."""
        self.connection = connection
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """
        Retrieve all airports with optional limit.
        
        Args:
            limit: Maximum number of airports to return (default: 100)
        
        Returns:
            List of Airport objects
        """
        query = """
        MATCH (a:Airport)
        RETURN a
        ORDER BY a.iata
        LIMIT $limit
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, limit=limit)
                return [Airport(**record["a"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find airports: {str(e)}")
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """
        Find airport by IATA code.
        
        Args:
            iata: IATA airport code (e.g., LAX)
        
        Returns:
            Airport object if found, None otherwise
        """
        query = """
        MATCH (a:Airport {iata: $iata})
        RETURN a
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, iata=iata)
                record = result.single()
                return Airport(**record["a"]) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find airport by IATA: {str(e)}")
    
    def find_by_icao(self, icao: str) -> Optional[Airport]:
        """
        Find airport by ICAO code.
        
        Args:
            icao: ICAO airport code (e.g., KLAX)
        
        Returns:
            Airport object if found, None otherwise
        """
        query = """
        MATCH (a:Airport {icao: $icao})
        RETURN a
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, icao=icao)
                record = result.single()
                return Airport(**record["a"]) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find airport by ICAO: {str(e)}")


class FlightRepository:
    """Repository for Flight entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """Initialize repository with database connection."""
        self.connection = connection
    
    def find_all(self, limit: int = 100) -> List[Flight]:
        """
        Retrieve all flights with optional limit.
        
        Args:
            limit: Maximum number of flights to return (default: 100)
        
        Returns:
            List of Flight objects
        """
        query = """
        MATCH (f:Flight)
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, limit=limit)
                return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find flights: {str(e)}")
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """
        Find flight by ID.
        
        Args:
            flight_id: Unique flight identifier
        
        Returns:
            Flight object if found, None otherwise
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        RETURN f
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, flight_id=flight_id)
                record = result.single()
                return Flight(**record["f"]) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find flight by ID: {str(e)}")
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """
        Find all flights operated by a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of flights to return (default: 100)
        
        Returns:
            List of Flight objects ordered by departure time (most recent first)
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
                return [Flight(**record["f"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find flights by aircraft: {str(e)}")
    
    def find_latest_destinations(self, limit: int = 20) -> List[dict]:
        """
        Find the latest flight destinations with airport details.
        
        Args:
            limit: Maximum number of destinations to return (default: 20)
        
        Returns:
            List of dictionaries containing flight and destination airport information
        """
        query = """
        MATCH (f:Flight)-[:ARRIVES_AT]->(a:Airport)
        RETURN f, a
        ORDER BY f.scheduled_arrival DESC
        LIMIT $limit
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, limit=limit)
                return [
                    {
                        "flight": Flight(**record["f"]),
                        "destination": Airport(**record["a"])
                    }
                    for record in result
                ]
        except Exception as e:
            raise QueryError(f"Failed to find latest destinations: {str(e)}")


class ComponentRepository:
    """Repository for Component entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """Initialize repository with database connection."""
        self.connection = connection
    
    def find_all(self, limit: int = 100) -> List[Component]:
        """
        Retrieve all components with optional limit.
        
        Args:
            limit: Maximum number of components to return (default: 100)
        
        Returns:
            List of Component objects
        """
        query = """
        MATCH (c:Component)
        RETURN c
        ORDER BY c.name
        LIMIT $limit
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, limit=limit)
                return [Component(**record["c"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find components: {str(e)}")
    
    def find_by_id(self, component_id: str) -> Optional[Component]:
        """
        Find component by ID.
        
        Args:
            component_id: Unique component identifier
        
        Returns:
            Component object if found, None otherwise
        """
        query = """
        MATCH (c:Component {component_id: $component_id})
        RETURN c
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, component_id=component_id)
                record = result.single()
                return Component(**record["c"]) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find component by ID: {str(e)}")
    
    def find_by_system(self, system_id: str) -> List[Component]:
        """
        Find all components for a specific system.
        
        Args:
            system_id: System identifier
        
        Returns:
            List of Component objects
        """
        query = """
        MATCH (s:System {system_id: $system_id})-[:HAS_COMPONENT]->(c:Component)
        RETURN c
        ORDER BY c.name
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, system_id=system_id)
                return [Component(**record["c"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find components by system: {str(e)}")


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """Initialize repository with database connection."""
        self.connection = connection
    
    def find_all(self, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Retrieve all maintenance events with optional limit.
        
        Args:
            limit: Maximum number of events to return (default: 100)
        
        Returns:
            List of MaintenanceEvent objects ordered by reported time (most recent first)
        """
        query = """
        MATCH (m:MaintenanceEvent)
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, limit=limit)
                return [MaintenanceEvent(**record["m"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find maintenance events: {str(e)}")
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find all maintenance events for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of events to return (default: 100)
        
        Returns:
            List of MaintenanceEvent objects ordered by reported time (most recent first)
        """
        query = """
        MATCH (m:MaintenanceEvent)-[:AFFECTS_AIRCRAFT]->(a:Aircraft {aircraft_id: $aircraft_id})
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, aircraft_id=aircraft_id, limit=limit)
                return [MaintenanceEvent(**record["m"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find maintenance events by aircraft: {str(e)}")
    
    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find maintenance events by severity level.
        
        Args:
            severity: Severity level (e.g., CRITICAL, WARNING)
            limit: Maximum number of events to return (default: 100)
        
        Returns:
            List of MaintenanceEvent objects ordered by reported time (most recent first)
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
                return [MaintenanceEvent(**record["m"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find maintenance events by severity: {str(e)}")
    
    def find_missing_components(self, limit: int = 100) -> List[dict]:
        """
        Find components with critical maintenance events (indicating missing/faulty components).
        
        Args:
            limit: Maximum number of results to return (default: 100)
        
        Returns:
            List of dictionaries containing component and maintenance event information
        """
        query = """
        MATCH (c:Component)-[:HAS_EVENT]->(m:MaintenanceEvent)
        WHERE m.severity = 'CRITICAL'
        RETURN c, m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, limit=limit)
                return [
                    {
                        "component": Component(**record["c"]),
                        "maintenance_event": MaintenanceEvent(**record["m"])
                    }
                    for record in result
                ]
        except Exception as e:
            raise QueryError(f"Failed to find missing components: {str(e)}")


class SystemRepository:
    """Repository for System entity operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """Initialize repository with database connection."""
        self.connection = connection
    
    def find_all(self, limit: int = 100) -> List[System]:
        """
        Retrieve all systems with optional limit.
        
        Args:
            limit: Maximum number of systems to return (default: 100)
        
        Returns:
            List of System objects
        """
        query = """
        MATCH (s:System)
        RETURN s
        ORDER BY s.name
        LIMIT $limit
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, limit=limit)
                return [System(**record["s"]) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find systems: {str(e)}")
    
    def find_by_id(self, system_id: str) -> Optional[System]:
        """
        Find system by ID.
        
        Args:
            system_id: Unique system identifier
        
        Returns:
            System object if found, None otherwise
        """
        query = """
        MATCH (s:System {system_id: $system_id})
        RETURN s
        """
        
        try:
            with self.connection.session() as session:
                result = session.run(query, system_id=system_id)
                record = result.single()
                return System(**record["s"]) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find system by ID: {str(e)}")
