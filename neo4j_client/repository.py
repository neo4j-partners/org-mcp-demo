"""Repository pattern implementation for Neo4j entities."""

from typing import List, Optional
from neo4j import Session
from .models import (
    Aircraft, Airport, Flight, System, Component, Sensor,
    Reading, MaintenanceEvent, Delay
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
            aircraft: Aircraft model instance
            
        Returns:
            Created aircraft instance
            
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
            if record:
                return Aircraft(**record["a"])
            raise QueryError("Failed to create aircraft")
        except Exception as e:
            raise QueryError(f"Error creating aircraft: {str(e)}")
    
    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """
        Find an aircraft by ID.
        
        Args:
            aircraft_id: Aircraft ID to search for
            
        Returns:
            Aircraft instance if found, None otherwise
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a
        """
        result = self.session.run(query, aircraft_id=aircraft_id)
        record = result.single()
        if record:
            return Aircraft(**record["a"])
        return None
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """Find an aircraft by tail number."""
        query = """
        MATCH (a:Aircraft {tail_number: $tail_number})
        RETURN a
        """
        result = self.session.run(query, tail_number=tail_number)
        record = result.single()
        if record:
            return Aircraft(**record["a"])
        return None
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """
        Find all aircraft.
        
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
        result = self.session.run(query, limit=limit)
        return [Aircraft(**record["a"]) for record in result]
    
    def update(self, aircraft: Aircraft) -> Aircraft:
        """Update an existing aircraft."""
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
        if record:
            return Aircraft(**record["a"])
        raise NotFoundError(f"Aircraft not found: {aircraft.aircraft_id}")
    
    def delete(self, aircraft_id: str) -> bool:
        """Delete an aircraft by ID."""
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        DETACH DELETE a
        RETURN count(a) as deleted
        """
        result = self.session.run(query, aircraft_id=aircraft_id)
        record = result.single()
        return record["deleted"] > 0 if record else False


class AirportRepository:
    """Repository for Airport entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, airport: Airport) -> Airport:
        """Create a new airport in the database."""
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
                return Airport(**record["a"])
            raise QueryError("Failed to create airport")
        except Exception as e:
            raise QueryError(f"Error creating airport: {str(e)}")
    
    def find_by_id(self, airport_id: str) -> Optional[Airport]:
        """Find an airport by ID."""
        query = """
        MATCH (a:Airport {airport_id: $airport_id})
        RETURN a
        """
        result = self.session.run(query, airport_id=airport_id)
        record = result.single()
        if record:
            return Airport(**record["a"])
        return None
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """Find an airport by IATA code."""
        query = """
        MATCH (a:Airport {iata: $iata})
        RETURN a
        """
        result = self.session.run(query, iata=iata)
        record = result.single()
        if record:
            return Airport(**record["a"])
        return None
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """Find all airports."""
        query = """
        MATCH (a:Airport)
        RETURN a
        LIMIT $limit
        """
        result = self.session.run(query, limit=limit)
        return [Airport(**record["a"]) for record in result]


class FlightRepository:
    """Repository for Flight entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, flight: Flight) -> Flight:
        """Create a new flight in the database."""
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
                return Flight(**record["f"])
            raise QueryError("Failed to create flight")
        except Exception as e:
            raise QueryError(f"Error creating flight: {str(e)}")
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """Find a flight by ID."""
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        RETURN f
        """
        result = self.session.run(query, flight_id=flight_id)
        record = result.single()
        if record:
            return Flight(**record["f"])
        return None
    
    def find_by_flight_number(self, flight_number: str) -> List[Flight]:
        """Find flights by flight number."""
        query = """
        MATCH (f:Flight {flight_number: $flight_number})
        RETURN f
        """
        result = self.session.run(query, flight_number=flight_number)
        return [Flight(**record["f"]) for record in result]
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """Find flights operated by a specific aircraft."""
        query = """
        MATCH (f:Flight {aircraft_id: $aircraft_id})
        RETURN f
        LIMIT $limit
        """
        result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
        return [Flight(**record["f"]) for record in result]


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """Create a new maintenance event in the database."""
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
                return MaintenanceEvent(**record["m"])
            raise QueryError("Failed to create maintenance event")
        except Exception as e:
            raise QueryError(f"Error creating maintenance event: {str(e)}")
    
    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """Find a maintenance event by ID."""
        query = """
        MATCH (m:MaintenanceEvent {event_id: $event_id})
        RETURN m
        """
        result = self.session.run(query, event_id=event_id)
        record = result.single()
        if record:
            return MaintenanceEvent(**record["m"])
        return None
    
    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find maintenance events for a specific aircraft."""
        query = """
        MATCH (m:MaintenanceEvent {aircraft_id: $aircraft_id})
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
        return [MaintenanceEvent(**record["m"]) for record in result]
    
    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find maintenance events by severity level."""
        query = """
        MATCH (m:MaintenanceEvent {severity: $severity})
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        result = self.session.run(query, severity=severity, limit=limit)
        return [MaintenanceEvent(**record["m"]) for record in result]


class SystemRepository:
    """Repository for System entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, system: System) -> System:
        """Create a new system in the database."""
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
                return System(**record["s"])
            raise QueryError("Failed to create system")
        except Exception as e:
            raise QueryError(f"Error creating system: {str(e)}")
    
    def find_by_id(self, system_id: str) -> Optional[System]:
        """Find a system by ID."""
        query = """
        MATCH (s:System {system_id: $system_id})
        RETURN s
        """
        result = self.session.run(query, system_id=system_id)
        record = result.single()
        if record:
            return System(**record["s"])
        return None
    
    def find_by_aircraft(self, aircraft_id: str) -> List[System]:
        """Find all systems for a specific aircraft."""
        query = """
        MATCH (s:System {aircraft_id: $aircraft_id})
        RETURN s
        """
        result = self.session.run(query, aircraft_id=aircraft_id)
        return [System(**record["s"]) for record in result]


class SensorRepository:
    """Repository for Sensor entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, sensor: Sensor) -> Sensor:
        """Create a new sensor in the database."""
        query = """
        MERGE (s:Sensor {sensor_id: $sensor_id})
        SET s.system_id = $system_id,
            s.name = $name,
            s.type = $type,
            s.unit = $unit
        RETURN s
        """
        try:
            result = self.session.run(query, **sensor.model_dump())
            record = result.single()
            if record:
                return Sensor(**record["s"])
            raise QueryError("Failed to create sensor")
        except Exception as e:
            raise QueryError(f"Error creating sensor: {str(e)}")
    
    def find_by_id(self, sensor_id: str) -> Optional[Sensor]:
        """Find a sensor by ID."""
        query = """
        MATCH (s:Sensor {sensor_id: $sensor_id})
        RETURN s
        """
        result = self.session.run(query, sensor_id=sensor_id)
        record = result.single()
        if record:
            return Sensor(**record["s"])
        return None
    
    def find_by_system(self, system_id: str) -> List[Sensor]:
        """Find all sensors for a specific system."""
        query = """
        MATCH (s:Sensor {system_id: $system_id})
        RETURN s
        """
        result = self.session.run(query, system_id=system_id)
        return [Sensor(**record["s"]) for record in result]


class ReadingRepository:
    """Repository for Reading entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, reading: Reading) -> Reading:
        """Create a new reading in the database."""
        query = """
        CREATE (r:Reading {
            reading_id: $reading_id,
            sensor_id: $sensor_id,
            timestamp: $timestamp,
            value: $value
        })
        RETURN r
        """
        try:
            result = self.session.run(query, **reading.model_dump())
            record = result.single()
            if record:
                return Reading(**record["r"])
            raise QueryError("Failed to create reading")
        except Exception as e:
            raise QueryError(f"Error creating reading: {str(e)}")
    
    def find_by_sensor(self, sensor_id: str, limit: int = 100) -> List[Reading]:
        """Find readings for a specific sensor."""
        query = """
        MATCH (r:Reading {sensor_id: $sensor_id})
        RETURN r
        ORDER BY r.timestamp DESC
        LIMIT $limit
        """
        result = self.session.run(query, sensor_id=sensor_id, limit=limit)
        return [Reading(**record["r"]) for record in result]


class DelayRepository:
    """Repository for Delay entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session."""
        self.session = session
    
    def create(self, delay: Delay) -> Delay:
        """Create a new delay in the database."""
        query = """
        MERGE (d:Delay {delay_id: $delay_id})
        SET d.flight_id = $flight_id,
            d.cause = $cause,
            d.minutes = $minutes
        RETURN d
        """
        try:
            result = self.session.run(query, **delay.model_dump())
            record = result.single()
            if record:
                return Delay(**record["d"])
            raise QueryError("Failed to create delay")
        except Exception as e:
            raise QueryError(f"Error creating delay: {str(e)}")
    
    def find_by_id(self, delay_id: str) -> Optional[Delay]:
        """Find a delay by ID."""
        query = """
        MATCH (d:Delay {delay_id: $delay_id})
        RETURN d
        """
        result = self.session.run(query, delay_id=delay_id)
        record = result.single()
        if record:
            return Delay(**record["d"])
        return None
    
    def find_by_flight(self, flight_id: str) -> List[Delay]:
        """Find all delays for a specific flight."""
        query = """
        MATCH (d:Delay {flight_id: $flight_id})
        RETURN d
        """
        result = self.session.run(query, flight_id=flight_id)
        return [Delay(**record["d"]) for record in result]
