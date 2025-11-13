"""Repository pattern implementations for Neo4j entities."""

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
        Initialize repository with database session.
        
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
            QueryError: If creation fails
        """
        try:
            query = """
            MERGE (a:Aircraft {aircraft_id: $aircraft_id})
            SET a.tail_number = $tail_number,
                a.icao24 = $icao24,
                a.model = $model,
                a.operator = $operator,
                a.manufacturer = $manufacturer
            RETURN a
            """
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
            aircraft_id: Aircraft identifier
            
        Returns:
            Aircraft if found, None otherwise
        """
        try:
            query = "MATCH (a:Aircraft {aircraft_id: $aircraft_id}) RETURN a"
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            return Aircraft(**dict(record["a"])) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """
        Find aircraft by tail number.
        
        Args:
            tail_number: Aircraft tail number
            
        Returns:
            Aircraft if found, None otherwise
        """
        try:
            query = "MATCH (a:Aircraft {tail_number: $tail_number}) RETURN a"
            result = self.session.run(query, tail_number=tail_number)
            record = result.single()
            return Aircraft(**dict(record["a"])) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """
        Find all aircraft.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of aircraft
        """
        try:
            query = "MATCH (a:Aircraft) RETURN a LIMIT $limit"
            result = self.session.run(query, limit=limit)
            return [Aircraft(**dict(record["a"])) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find aircraft: {e}")
    
    def update(self, aircraft: Aircraft) -> Aircraft:
        """
        Update an existing aircraft.
        
        Args:
            aircraft: Aircraft with updated data
            
        Returns:
            Updated aircraft
            
        Raises:
            NotFoundError: If aircraft not found
        """
        try:
            query = """
            MATCH (a:Aircraft {aircraft_id: $aircraft_id})
            SET a.tail_number = $tail_number,
                a.icao24 = $icao24,
                a.model = $model,
                a.operator = $operator,
                a.manufacturer = $manufacturer
            RETURN a
            """
            result = self.session.run(query, **aircraft.model_dump())
            record = result.single()
            if not record:
                raise NotFoundError(f"Aircraft not found: {aircraft.aircraft_id}")
            return Aircraft(**dict(record["a"]))
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Failed to update aircraft: {e}")
    
    def delete(self, aircraft_id: str) -> bool:
        """
        Delete an aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            
        Returns:
            True if deleted, False if not found
        """
        try:
            query = """
            MATCH (a:Aircraft {aircraft_id: $aircraft_id})
            DETACH DELETE a
            RETURN count(a) as deleted
            """
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Failed to delete aircraft: {e}")


class AirportRepository:
    """Repository for Airport entity operations."""
    
    def __init__(self, session: Session):
        """
        Initialize repository with database session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, airport: Airport) -> Airport:
        """
        Create a new airport in the database.
        
        Args:
            airport: Airport model instance
            
        Returns:
            Created airport
        """
        try:
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
            result = self.session.run(query, **airport.model_dump())
            record = result.single()
            if record:
                return Airport(**dict(record["a"]))
            raise QueryError("Failed to create airport")
        except Exception as e:
            raise QueryError(f"Failed to create airport: {e}")
    
    def find_by_id(self, airport_id: str) -> Optional[Airport]:
        """
        Find airport by ID.
        
        Args:
            airport_id: Airport identifier
            
        Returns:
            Airport if found, None otherwise
        """
        try:
            query = "MATCH (a:Airport {airport_id: $airport_id}) RETURN a"
            result = self.session.run(query, airport_id=airport_id)
            record = result.single()
            return Airport(**dict(record["a"])) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find airport: {e}")
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """
        Find airport by IATA code.
        
        Args:
            iata: IATA airport code
            
        Returns:
            Airport if found, None otherwise
        """
        try:
            query = "MATCH (a:Airport {iata: $iata}) RETURN a"
            result = self.session.run(query, iata=iata)
            record = result.single()
            return Airport(**dict(record["a"])) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find airport: {e}")
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """
        Find all airports.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of airports
        """
        try:
            query = "MATCH (a:Airport) RETURN a LIMIT $limit"
            result = self.session.run(query, limit=limit)
            return [Airport(**dict(record["a"])) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find airports: {e}")
    
    def update(self, airport: Airport) -> Airport:
        """
        Update an existing airport.
        
        Args:
            airport: Airport with updated data
            
        Returns:
            Updated airport
        """
        try:
            query = """
            MATCH (a:Airport {airport_id: $airport_id})
            SET a.iata = $iata,
                a.icao = $icao,
                a.name = $name,
                a.city = $city,
                a.country = $country,
                a.lat = $lat,
                a.lon = $lon
            RETURN a
            """
            result = self.session.run(query, **airport.model_dump())
            record = result.single()
            if not record:
                raise NotFoundError(f"Airport not found: {airport.airport_id}")
            return Airport(**dict(record["a"]))
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Failed to update airport: {e}")
    
    def delete(self, airport_id: str) -> bool:
        """
        Delete an airport.
        
        Args:
            airport_id: Airport identifier
            
        Returns:
            True if deleted, False if not found
        """
        try:
            query = """
            MATCH (a:Airport {airport_id: $airport_id})
            DETACH DELETE a
            RETURN count(a) as deleted
            """
            result = self.session.run(query, airport_id=airport_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Failed to delete airport: {e}")


class FlightRepository:
    """Repository for Flight entity operations."""
    
    def __init__(self, session: Session):
        """
        Initialize repository with database session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, flight: Flight) -> Flight:
        """
        Create a new flight in the database.
        
        Args:
            flight: Flight model instance
            
        Returns:
            Created flight
        """
        try:
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
            result = self.session.run(query, **flight.model_dump())
            record = result.single()
            if record:
                return Flight(**dict(record["f"]))
            raise QueryError("Failed to create flight")
        except Exception as e:
            raise QueryError(f"Failed to create flight: {e}")
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """
        Find flight by ID.
        
        Args:
            flight_id: Flight identifier
            
        Returns:
            Flight if found, None otherwise
        """
        try:
            query = "MATCH (f:Flight {flight_id: $flight_id}) RETURN f"
            result = self.session.run(query, flight_id=flight_id)
            record = result.single()
            return Flight(**dict(record["f"])) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find flight: {e}")
    
    def find_by_flight_number(self, flight_number: str, limit: int = 100) -> List[Flight]:
        """
        Find flights by flight number.
        
        Args:
            flight_number: Flight number
            limit: Maximum number of results
            
        Returns:
            List of flights
        """
        try:
            query = """
            MATCH (f:Flight {flight_number: $flight_number}) 
            RETURN f 
            ORDER BY f.scheduled_departure DESC
            LIMIT $limit
            """
            result = self.session.run(query, flight_number=flight_number, limit=limit)
            return [Flight(**dict(record["f"])) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find flights: {e}")
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """
        Find flights by aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of results
            
        Returns:
            List of flights
        """
        try:
            query = """
            MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:OPERATES_FLIGHT]->(f:Flight)
            RETURN f
            ORDER BY f.scheduled_departure DESC
            LIMIT $limit
            """
            result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
            return [Flight(**dict(record["f"])) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find flights: {e}")
    
    def find_all(self, limit: int = 100) -> List[Flight]:
        """
        Find all flights.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of flights
        """
        try:
            query = "MATCH (f:Flight) RETURN f LIMIT $limit"
            result = self.session.run(query, limit=limit)
            return [Flight(**dict(record["f"])) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find flights: {e}")
    
    def update(self, flight: Flight) -> Flight:
        """
        Update an existing flight.
        
        Args:
            flight: Flight with updated data
            
        Returns:
            Updated flight
        """
        try:
            query = """
            MATCH (f:Flight {flight_id: $flight_id})
            SET f.flight_number = $flight_number,
                f.aircraft_id = $aircraft_id,
                f.operator = $operator,
                f.origin = $origin,
                f.destination = $destination,
                f.scheduled_departure = $scheduled_departure,
                f.scheduled_arrival = $scheduled_arrival
            RETURN f
            """
            result = self.session.run(query, **flight.model_dump())
            record = result.single()
            if not record:
                raise NotFoundError(f"Flight not found: {flight.flight_id}")
            return Flight(**dict(record["f"]))
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Failed to update flight: {e}")
    
    def delete(self, flight_id: str) -> bool:
        """
        Delete a flight.
        
        Args:
            flight_id: Flight identifier
            
        Returns:
            True if deleted, False if not found
        """
        try:
            query = """
            MATCH (f:Flight {flight_id: $flight_id})
            DETACH DELETE f
            RETURN count(f) as deleted
            """
            result = self.session.run(query, flight_id=flight_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Failed to delete flight: {e}")


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations."""
    
    def __init__(self, session: Session):
        """
        Initialize repository with database session.
        
        Args:
            session: Neo4j database session
        """
        self.session = session
    
    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """
        Create a new maintenance event in the database.
        
        Args:
            event: MaintenanceEvent model instance
            
        Returns:
            Created maintenance event
        """
        try:
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
            result = self.session.run(query, **event.model_dump())
            record = result.single()
            if record:
                return MaintenanceEvent(**dict(record["m"]))
            raise QueryError("Failed to create maintenance event")
        except Exception as e:
            raise QueryError(f"Failed to create maintenance event: {e}")
    
    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """
        Find maintenance event by ID.
        
        Args:
            event_id: Event identifier
            
        Returns:
            MaintenanceEvent if found, None otherwise
        """
        try:
            query = "MATCH (m:MaintenanceEvent {event_id: $event_id}) RETURN m"
            result = self.session.run(query, event_id=event_id)
            record = result.single()
            return MaintenanceEvent(**dict(record["m"])) if record else None
        except Exception as e:
            raise QueryError(f"Failed to find maintenance event: {e}")
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find maintenance events by aircraft.
        
        Args:
            aircraft_id: Aircraft identifier
            limit: Maximum number of results
            
        Returns:
            List of maintenance events
        """
        try:
            query = """
            MATCH (a:Aircraft {aircraft_id: $aircraft_id})<-[:AFFECTS_AIRCRAFT]-(m:MaintenanceEvent)
            RETURN m
            ORDER BY m.reported_at DESC
            LIMIT $limit
            """
            result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
            return [MaintenanceEvent(**dict(record["m"])) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find maintenance events: {e}")
    
    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find maintenance events by severity.
        
        Args:
            severity: Severity level
            limit: Maximum number of results
            
        Returns:
            List of maintenance events
        """
        try:
            query = """
            MATCH (m:MaintenanceEvent {severity: $severity})
            RETURN m
            ORDER BY m.reported_at DESC
            LIMIT $limit
            """
            result = self.session.run(query, severity=severity, limit=limit)
            return [MaintenanceEvent(**dict(record["m"])) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find maintenance events: {e}")
    
    def find_all(self, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find all maintenance events.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List of maintenance events
        """
        try:
            query = "MATCH (m:MaintenanceEvent) RETURN m LIMIT $limit"
            result = self.session.run(query, limit=limit)
            return [MaintenanceEvent(**dict(record["m"])) for record in result]
        except Exception as e:
            raise QueryError(f"Failed to find maintenance events: {e}")
    
    def update(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """
        Update an existing maintenance event.
        
        Args:
            event: MaintenanceEvent with updated data
            
        Returns:
            Updated maintenance event
        """
        try:
            query = """
            MATCH (m:MaintenanceEvent {event_id: $event_id})
            SET m.aircraft_id = $aircraft_id,
                m.system_id = $system_id,
                m.component_id = $component_id,
                m.fault = $fault,
                m.severity = $severity,
                m.reported_at = $reported_at,
                m.corrective_action = $corrective_action
            RETURN m
            """
            result = self.session.run(query, **event.model_dump())
            record = result.single()
            if not record:
                raise NotFoundError(f"Maintenance event not found: {event.event_id}")
            return MaintenanceEvent(**dict(record["m"]))
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Failed to update maintenance event: {e}")
    
    def delete(self, event_id: str) -> bool:
        """
        Delete a maintenance event.
        
        Args:
            event_id: Event identifier
            
        Returns:
            True if deleted, False if not found
        """
        try:
            query = """
            MATCH (m:MaintenanceEvent {event_id: $event_id})
            DETACH DELETE m
            RETURN count(m) as deleted
            """
            result = self.session.run(query, event_id=event_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Failed to delete maintenance event: {e}")
