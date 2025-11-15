"""Repository pattern implementations for Neo4j entities."""

from typing import Optional, List
from neo4j import Session
from neo4j.exceptions import Neo4jError

from neo4j_client.models import (
    Aircraft,
    Airport,
    Flight,
    System,
    Component,
    MaintenanceEvent,
    Delay,
)
from neo4j_client.exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entities."""

    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session

    def create(self, aircraft: Aircraft) -> Aircraft:
        """Create a new aircraft node.
        
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
            result = self.session.run(query, **aircraft.model_dump())
            record = result.single()
            if record:
                return Aircraft(**record["a"])
            raise QueryError("Failed to create aircraft")
        except Neo4jError as e:
            raise QueryError(f"Error creating aircraft: {e}") from e

    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """Find an aircraft by its ID.
        
        Args:
            aircraft_id: Aircraft ID to search for
        
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
            return Aircraft(**record["a"]) if record else None
        except Neo4jError as e:
            raise QueryError(f"Error finding aircraft: {e}") from e

    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """Find an aircraft by its tail number.
        
        Args:
            tail_number: Tail number to search for
        
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
            return Aircraft(**record["a"]) if record else None
        except Neo4jError as e:
            raise QueryError(f"Error finding aircraft: {e}") from e

    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """Find all aircraft with optional limit.
        
        Args:
            limit: Maximum number of results to return
        
        Returns:
            List of aircraft objects
        
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
            return [Aircraft(**record["a"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Error finding aircraft: {e}") from e

    def update(self, aircraft: Aircraft) -> Aircraft:
        """Update an existing aircraft.
        
        Args:
            aircraft: Aircraft object with updated data
        
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
            result = self.session.run(query, **aircraft.model_dump())
            record = result.single()
            if record:
                return Aircraft(**record["a"])
            raise NotFoundError(f"Aircraft {aircraft.aircraft_id} not found")
        except Neo4jError as e:
            raise QueryError(f"Error updating aircraft: {e}") from e

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
        DETACH DELETE a
        RETURN count(a) as deleted
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Neo4jError as e:
            raise QueryError(f"Error deleting aircraft: {e}") from e


class AirportRepository:
    """Repository for Airport entities."""

    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session

    def create(self, airport: Airport) -> Airport:
        """Create a new airport node.
        
        Args:
            airport: Airport object to create
        
        Returns:
            The created airport
        
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
                return Airport(**record["a"])
            raise QueryError("Failed to create airport")
        except Neo4jError as e:
            raise QueryError(f"Error creating airport: {e}") from e

    def find_by_id(self, airport_id: str) -> Optional[Airport]:
        """Find an airport by its ID.
        
        Args:
            airport_id: Airport ID to search for
        
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
            return Airport(**record["a"]) if record else None
        except Neo4jError as e:
            raise QueryError(f"Error finding airport: {e}") from e

    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """Find an airport by its IATA code.
        
        Args:
            iata: IATA code to search for
        
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
            return Airport(**record["a"]) if record else None
        except Neo4jError as e:
            raise QueryError(f"Error finding airport: {e}") from e

    def find_all(self, limit: int = 100) -> List[Airport]:
        """Find all airports with optional limit.
        
        Args:
            limit: Maximum number of results to return
        
        Returns:
            List of airport objects
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Airport)
        RETURN a
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            return [Airport(**record["a"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Error finding airports: {e}") from e

    def delete(self, airport_id: str) -> bool:
        """Delete an airport by ID.
        
        Args:
            airport_id: Airport ID to delete
        
        Returns:
            True if deleted, False if not found
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Airport {airport_id: $airport_id})
        DETACH DELETE a
        RETURN count(a) as deleted
        """
        try:
            result = self.session.run(query, airport_id=airport_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Neo4jError as e:
            raise QueryError(f"Error deleting airport: {e}") from e


class FlightRepository:
    """Repository for Flight entities."""

    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session

    def create(self, flight: Flight) -> Flight:
        """Create a new flight node.
        
        Args:
            flight: Flight object to create
        
        Returns:
            The created flight
        
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
                return Flight(**record["f"])
            raise QueryError("Failed to create flight")
        except Neo4jError as e:
            raise QueryError(f"Error creating flight: {e}") from e

    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """Find a flight by its ID.
        
        Args:
            flight_id: Flight ID to search for
        
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
            return Flight(**record["f"]) if record else None
        except Neo4jError as e:
            raise QueryError(f"Error finding flight: {e}") from e

    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """Find flights for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft ID to search for
            limit: Maximum number of results to return
        
        Returns:
            List of flight objects
        
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
            return [Flight(**record["f"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Error finding flights: {e}") from e

    def find_all(self, limit: int = 100) -> List[Flight]:
        """Find all flights with optional limit.
        
        Args:
            limit: Maximum number of results to return
        
        Returns:
            List of flight objects
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (f:Flight)
        RETURN f
        LIMIT $limit
        """
        try:
            result = self.session.run(query, limit=limit)
            return [Flight(**record["f"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Error finding flights: {e}") from e

    def delete(self, flight_id: str) -> bool:
        """Delete a flight by ID.
        
        Args:
            flight_id: Flight ID to delete
        
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
        except Neo4jError as e:
            raise QueryError(f"Error deleting flight: {e}") from e


class SystemRepository:
    """Repository for System entities."""

    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session

    def create(self, system: System) -> System:
        """Create a new system node.
        
        Args:
            system: System object to create
        
        Returns:
            The created system
        
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
                return System(**record["s"])
            raise QueryError("Failed to create system")
        except Neo4jError as e:
            raise QueryError(f"Error creating system: {e}") from e

    def find_by_id(self, system_id: str) -> Optional[System]:
        """Find a system by its ID.
        
        Args:
            system_id: System ID to search for
        
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
            return System(**record["s"]) if record else None
        except Neo4jError as e:
            raise QueryError(f"Error finding system: {e}") from e

    def find_by_aircraft(self, aircraft_id: str) -> List[System]:
        """Find systems for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft ID to search for
        
        Returns:
            List of system objects
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:HAS_SYSTEM]->(s:System)
        RETURN s
        """
        try:
            result = self.session.run(query, aircraft_id=aircraft_id)
            return [System(**record["s"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Error finding systems: {e}") from e

    def delete(self, system_id: str) -> bool:
        """Delete a system by ID.
        
        Args:
            system_id: System ID to delete
        
        Returns:
            True if deleted, False if not found
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (s:System {system_id: $system_id})
        DETACH DELETE s
        RETURN count(s) as deleted
        """
        try:
            result = self.session.run(query, system_id=system_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Neo4jError as e:
            raise QueryError(f"Error deleting system: {e}") from e


class ComponentRepository:
    """Repository for Component entities."""

    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session

    def create(self, component: Component) -> Component:
        """Create a new component node.
        
        Args:
            component: Component object to create
        
        Returns:
            The created component
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MERGE (c:Component {component_id: $component_id})
        SET c.system_id = $system_id,
            c.name = $name,
            c.type = $type
        RETURN c
        """
        try:
            result = self.session.run(query, **component.model_dump())
            record = result.single()
            if record:
                return Component(**record["c"])
            raise QueryError("Failed to create component")
        except Neo4jError as e:
            raise QueryError(f"Error creating component: {e}") from e

    def find_by_id(self, component_id: str) -> Optional[Component]:
        """Find a component by its ID.
        
        Args:
            component_id: Component ID to search for
        
        Returns:
            Component object if found, None otherwise
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (c:Component {component_id: $component_id})
        RETURN c
        """
        try:
            result = self.session.run(query, component_id=component_id)
            record = result.single()
            return Component(**record["c"]) if record else None
        except Neo4jError as e:
            raise QueryError(f"Error finding component: {e}") from e

    def find_by_system(self, system_id: str) -> List[Component]:
        """Find components for a specific system.
        
        Args:
            system_id: System ID to search for
        
        Returns:
            List of component objects
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (s:System {system_id: $system_id})-[:HAS_COMPONENT]->(c:Component)
        RETURN c
        """
        try:
            result = self.session.run(query, system_id=system_id)
            return [Component(**record["c"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Error finding components: {e}") from e

    def delete(self, component_id: str) -> bool:
        """Delete a component by ID.
        
        Args:
            component_id: Component ID to delete
        
        Returns:
            True if deleted, False if not found
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (c:Component {component_id: $component_id})
        DETACH DELETE c
        RETURN count(c) as deleted
        """
        try:
            result = self.session.run(query, component_id=component_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Neo4jError as e:
            raise QueryError(f"Error deleting component: {e}") from e


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entities."""

    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session

    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """Create a new maintenance event node.
        
        Args:
            event: MaintenanceEvent object to create
        
        Returns:
            The created maintenance event
        
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
                return MaintenanceEvent(**record["m"])
            raise QueryError("Failed to create maintenance event")
        except Neo4jError as e:
            raise QueryError(f"Error creating maintenance event: {e}") from e

    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """Find a maintenance event by its ID.
        
        Args:
            event_id: Event ID to search for
        
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
            return MaintenanceEvent(**record["m"]) if record else None
        except Neo4jError as e:
            raise QueryError(f"Error finding maintenance event: {e}") from e

    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find maintenance events for a specific aircraft.
        
        Args:
            aircraft_id: Aircraft ID to search for
            limit: Maximum number of results to return
        
        Returns:
            List of maintenance event objects
        
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
            return [MaintenanceEvent(**record["m"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Error finding maintenance events: {e}") from e

    def find_by_severity(self, severity: str, limit: int = 100) -> List[MaintenanceEvent]:
        """Find maintenance events by severity level.
        
        Args:
            severity: Severity level to search for
            limit: Maximum number of results to return
        
        Returns:
            List of maintenance event objects
        
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
            return [MaintenanceEvent(**record["m"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Error finding maintenance events: {e}") from e

    def delete(self, event_id: str) -> bool:
        """Delete a maintenance event by ID.
        
        Args:
            event_id: Event ID to delete
        
        Returns:
            True if deleted, False if not found
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (m:MaintenanceEvent {event_id: $event_id})
        DETACH DELETE m
        RETURN count(m) as deleted
        """
        try:
            result = self.session.run(query, event_id=event_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Neo4jError as e:
            raise QueryError(f"Error deleting maintenance event: {e}") from e


class DelayRepository:
    """Repository for Delay entities."""

    def __init__(self, session: Session):
        """Initialize repository with a Neo4j session.
        
        Args:
            session: Active Neo4j session
        """
        self.session = session

    def create(self, delay: Delay) -> Delay:
        """Create a new delay node.
        
        Args:
            delay: Delay object to create
        
        Returns:
            The created delay
        
        Raises:
            QueryError: If the query fails
        """
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
        except Neo4jError as e:
            raise QueryError(f"Error creating delay: {e}") from e

    def find_by_id(self, delay_id: str) -> Optional[Delay]:
        """Find a delay by its ID.
        
        Args:
            delay_id: Delay ID to search for
        
        Returns:
            Delay object if found, None otherwise
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (d:Delay {delay_id: $delay_id})
        RETURN d
        """
        try:
            result = self.session.run(query, delay_id=delay_id)
            record = result.single()
            return Delay(**record["d"]) if record else None
        except Neo4jError as e:
            raise QueryError(f"Error finding delay: {e}") from e

    def find_by_flight(self, flight_id: str) -> List[Delay]:
        """Find delays for a specific flight.
        
        Args:
            flight_id: Flight ID to search for
        
        Returns:
            List of delay objects
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})-[:HAS_DELAY]->(d:Delay)
        RETURN d
        """
        try:
            result = self.session.run(query, flight_id=flight_id)
            return [Delay(**record["d"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Error finding delays: {e}") from e

    def find_significant_delays(self, min_minutes: int = 30, limit: int = 100) -> List[Delay]:
        """Find delays exceeding a minimum duration.
        
        Args:
            min_minutes: Minimum delay duration in minutes
            limit: Maximum number of results to return
        
        Returns:
            List of delay objects
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (d:Delay)
        WHERE d.minutes >= $min_minutes
        RETURN d
        ORDER BY d.minutes DESC
        LIMIT $limit
        """
        try:
            result = self.session.run(query, min_minutes=min_minutes, limit=limit)
            return [Delay(**record["d"]) for record in result]
        except Neo4jError as e:
            raise QueryError(f"Error finding delays: {e}") from e

    def delete(self, delay_id: str) -> bool:
        """Delete a delay by ID.
        
        Args:
            delay_id: Delay ID to delete
        
        Returns:
            True if deleted, False if not found
        
        Raises:
            QueryError: If the query fails
        """
        query = """
        MATCH (d:Delay {delay_id: $delay_id})
        DETACH DELETE d
        RETURN count(d) as deleted
        """
        try:
            result = self.session.run(query, delay_id=delay_id)
            record = result.single()
            return record["deleted"] > 0 if record else False
        except Neo4jError as e:
            raise QueryError(f"Error deleting delay: {e}") from e
