"""Repository pattern implementations for Neo4j entities."""

from typing import List, Optional
from neo4j import Session
from .models import Aircraft, Flight, Airport, MaintenanceEvent, Delay
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def create(self, aircraft: Aircraft) -> Aircraft:
        """Create a new aircraft in the database.
        
        Args:
            aircraft: Aircraft object to create
            
        Returns:
            Created aircraft object
        """
        query = """
        MERGE (a:Aircraft {aircraft_id: $aircraft_id})
        SET a.tail_number = $tail_number,
            a.manufacturer = $manufacturer,
            a.model = $model,
            a.operator = $operator,
            a.icao24 = $icao24
        RETURN a
        """
        try:
            result = self.session.run(query, **aircraft.model_dump())
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
            Aircraft object if found, None otherwise
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            if record:
                node = record["a"]
                return Aircraft(
                    aircraft_id=node["aircraft_id"],
                    tail_number=node["tail_number"],
                    manufacturer=node["manufacturer"],
                    model=node["model"],
                    operator=node["operator"],
                    icao24=node.get("icao24")
                )
            return None
        except Exception as e:
            raise QueryError(f"Error finding aircraft: {str(e)}")
    
    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """Find an aircraft by its tail number.
        
        Args:
            tail_number: Tail number to search for
            
        Returns:
            Aircraft object if found, None otherwise
        """
        query = """
        MATCH (a:Aircraft {tail_number: $tail_number})
        RETURN a
        """
        try:
            result = self.session.run(query, tail_number=tail_number)
            record = result.single()
            if record:
                node = record["a"]
                return Aircraft(
                    aircraft_id=node["aircraft_id"],
                    tail_number=node["tail_number"],
                    manufacturer=node["manufacturer"],
                    model=node["model"],
                    operator=node["operator"],
                    icao24=node.get("icao24")
                )
            return None
        except Exception as e:
            raise QueryError(f"Error finding aircraft by tail number: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """Find all aircraft in the database.
        
        Args:
            limit: Maximum number of aircraft to return
            
        Returns:
            List of Aircraft objects
        """
        query = """
        MATCH (a:Aircraft)
        RETURN a
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            aircraft_list = []
            for record in result:
                node = record["a"]
                aircraft_list.append(Aircraft(
                    aircraft_id=node["aircraft_id"],
                    tail_number=node["tail_number"],
                    manufacturer=node["manufacturer"],
                    model=node["model"],
                    operator=node["operator"],
                    icao24=node.get("icao24")
                ))
            return aircraft_list
        except Exception as e:
            raise QueryError(f"Error finding all aircraft: {str(e)}")
    
    def find_by_operator(self, operator: str) -> List[Aircraft]:
        """Find all aircraft operated by a specific operator.
        
        Args:
            operator: Operator name to search for
            
        Returns:
            List of Aircraft objects
        """
        query = """
        MATCH (a:Aircraft {operator: $operator})
        RETURN a
        """
        try:
            result = self.session.run(query, operator=operator)
            aircraft_list = []
            for record in result:
                node = record["a"]
                aircraft_list.append(Aircraft(
                    aircraft_id=node["aircraft_id"],
                    tail_number=node["tail_number"],
                    manufacturer=node["manufacturer"],
                    model=node["model"],
                    operator=node["operator"],
                    icao24=node.get("icao24")
                ))
            return aircraft_list
        except Exception as e:
            raise QueryError(f"Error finding aircraft by operator: {str(e)}")
    
    def update(self, aircraft: Aircraft) -> Aircraft:
        """Update an existing aircraft.
        
        Args:
            aircraft: Aircraft object with updated data
            
        Returns:
            Updated aircraft object
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        SET a.tail_number = $tail_number,
            a.manufacturer = $manufacturer,
            a.model = $model,
            a.operator = $operator,
            a.icao24 = $icao24
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
            raise QueryError(f"Error updating aircraft: {str(e)}")
    
    def delete(self, aircraft_id: str) -> bool:
        """Delete an aircraft by ID.
        
        Args:
            aircraft_id: Aircraft ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        DETACH DELETE a
        RETURN count(a) as deleted_count
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            return record["deleted_count"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Error deleting aircraft: {str(e)}")


class FlightRepository:
    """Repository for Flight entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def create(self, flight: Flight) -> Flight:
        """Create a new flight in the database.
        
        Args:
            flight: Flight object to create
            
        Returns:
            Created flight object
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
                return flight
            raise QueryError("Failed to create flight")
        except Exception as e:
            raise QueryError(f"Error creating flight: {str(e)}")
    
    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """Find a flight by its ID.
        
        Args:
            flight_id: Flight ID to search for
            
        Returns:
            Flight object if found, None otherwise
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        RETURN f
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
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
    
    def find_by_flight_number(self, flight_number: str) -> List[Flight]:
        """Find flights by flight number.
        
        Args:
            flight_number: Flight number to search for
            
        Returns:
            List of Flight objects
        """
        query = """
        MATCH (f:Flight {flight_number: $flight_number})
        RETURN f
        """
        try:
            result = self.session.run(query, flight_number=flight_number)
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
            raise QueryError(f"Error finding flights by number: {str(e)}")
    
    def find_by_aircraft(self, aircraft_id: str) -> List[Flight]:
        """Find all flights operated by a specific aircraft.
        
        Args:
            aircraft_id: Aircraft ID to search for
            
        Returns:
            List of Flight objects
        """
        query = """
        MATCH (f:Flight {aircraft_id: $aircraft_id})
        RETURN f
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
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
            raise QueryError(f"Error finding flights by aircraft: {str(e)}")
    
    def delete(self, flight_id: str) -> bool:
        """Delete a flight by ID.
        
        Args:
            flight_id: Flight ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        DETACH DELETE f
        RETURN count(f) as deleted_count
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
            record = result.single()
            return record["deleted_count"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Error deleting flight: {str(e)}")


class AirportRepository:
    """Repository for Airport entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def create(self, airport: Airport) -> Airport:
        """Create a new airport in the database.
        
        Args:
            airport: Airport object to create
            
        Returns:
            Created airport object
        """
        query = """
        MERGE (a:Airport {airport_id: $airport_id})
        SET a.name = $name,
            a.iata = $iata,
            a.icao = $icao,
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
                return airport
            raise QueryError("Failed to create airport")
        except Exception as e:
            raise QueryError(f"Error creating airport: {str(e)}")
    
    def find_by_id(self, airport_id: str) -> Optional[Airport]:
        """Find an airport by its ID.
        
        Args:
            airport_id: Airport ID to search for
            
        Returns:
            Airport object if found, None otherwise
        """
        query = """
        MATCH (a:Airport {airport_id: $airport_id})
        RETURN a
        """
        try:
            result = self.session.run(query, airport_id=airport_id)
            record = result.single()
            if record:
                node = record["a"]
                return Airport(
                    airport_id=node["airport_id"],
                    name=node["name"],
                    iata=node["iata"],
                    icao=node["icao"],
                    city=node["city"],
                    country=node["country"],
                    lat=node["lat"],
                    lon=node["lon"]
                )
            return None
        except Exception as e:
            raise QueryError(f"Error finding airport: {str(e)}")
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """Find an airport by its IATA code.
        
        Args:
            iata: IATA code to search for
            
        Returns:
            Airport object if found, None otherwise
        """
        query = """
        MATCH (a:Airport {iata: $iata})
        RETURN a
        """
        try:
            result = self.session.run(query, iata=iata)
            record = result.single()
            if record:
                node = record["a"]
                return Airport(
                    airport_id=node["airport_id"],
                    name=node["name"],
                    iata=node["iata"],
                    icao=node["icao"],
                    city=node["city"],
                    country=node["country"],
                    lat=node["lat"],
                    lon=node["lon"]
                )
            return None
        except Exception as e:
            raise QueryError(f"Error finding airport by IATA: {str(e)}")
    
    def find_all(self, limit: int = 100) -> List[Airport]:
        """Find all airports in the database.
        
        Args:
            limit: Maximum number of airports to return
            
        Returns:
            List of Airport objects
        """
        query = """
        MATCH (a:Airport)
        RETURN a
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            airports = []
            for record in result:
                node = record["a"]
                airports.append(Airport(
                    airport_id=node["airport_id"],
                    name=node["name"],
                    iata=node["iata"],
                    icao=node["icao"],
                    city=node["city"],
                    country=node["country"],
                    lat=node["lat"],
                    lon=node["lon"]
                ))
            return airports
        except Exception as e:
            raise QueryError(f"Error finding all airports: {str(e)}")
    
    def delete(self, airport_id: str) -> bool:
        """Delete an airport by ID.
        
        Args:
            airport_id: Airport ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        query = """
        MATCH (a:Airport {airport_id: $airport_id})
        DETACH DELETE a
        RETURN count(a) as deleted_count
        """
        try:
            result = self.session.run(query, airport_id=airport_id)
            record = result.single()
            return record["deleted_count"] > 0 if record else False
        except Exception as e:
            raise QueryError(f"Error deleting airport: {str(e)}")


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entity operations."""
    
    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session
    
    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """Create a new maintenance event in the database.
        
        Args:
            event: MaintenanceEvent object to create
            
        Returns:
            Created maintenance event object
        """
        query = """
        MERGE (e:MaintenanceEvent {event_id: $event_id})
        SET e.aircraft_id = $aircraft_id,
            e.system_id = $system_id,
            e.component_id = $component_id,
            e.fault = $fault,
            e.severity = $severity,
            e.corrective_action = $corrective_action,
            e.reported_at = $reported_at
        RETURN e
        """
        try:
            result = self.session.run(query, **event.model_dump())
            record = result.single()
            if record:
                return event
            raise QueryError("Failed to create maintenance event")
        except Exception as e:
            raise QueryError(f"Error creating maintenance event: {str(e)}")
    
    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """Find a maintenance event by its ID.
        
        Args:
            event_id: Event ID to search for
            
        Returns:
            MaintenanceEvent object if found, None otherwise
        """
        query = """
        MATCH (e:MaintenanceEvent {event_id: $event_id})
        RETURN e
        """
        try:
            result = self.session.run(query, event_id=event_id)
            record = result.single()
            if record:
                node = record["e"]
                return MaintenanceEvent(
                    event_id=node["event_id"],
                    aircraft_id=node["aircraft_id"],
                    system_id=node.get("system_id"),
                    component_id=node.get("component_id"),
                    fault=node["fault"],
                    severity=node["severity"],
                    corrective_action=node["corrective_action"],
                    reported_at=node["reported_at"]
                )
            return None
        except Exception as e:
            raise QueryError(f"Error finding maintenance event: {str(e)}")
    
    def find_by_aircraft(self, aircraft_id: str) -> List[MaintenanceEvent]:
        """Find all maintenance events for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft ID to search for
            
        Returns:
            List of MaintenanceEvent objects
        """
        query = """
        MATCH (e:MaintenanceEvent {aircraft_id: $aircraft_id})
        RETURN e
        ORDER BY e.reported_at DESC
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            events = []
            for record in result:
                node = record["e"]
                events.append(MaintenanceEvent(
                    event_id=node["event_id"],
                    aircraft_id=node["aircraft_id"],
                    system_id=node.get("system_id"),
                    component_id=node.get("component_id"),
                    fault=node["fault"],
                    severity=node["severity"],
                    corrective_action=node["corrective_action"],
                    reported_at=node["reported_at"]
                ))
            return events
        except Exception as e:
            raise QueryError(f"Error finding maintenance events by aircraft: {str(e)}")
