"""Repository pattern for querying Neo4j entities."""

from typing import List, Optional
from neo4j import Session

from .models import (
    Aircraft, Airport, Flight, System, Component,
    Sensor, Reading, MaintenanceEvent, Delay
)
from .exceptions import QueryError, NotFoundError


class AircraftRepository:
    """Repository for Aircraft entities."""

    def __init__(self, session: Session):
        """
        Initialize the repository.

        Args:
            session: Neo4j session instance
        """
        self.session = session

    def create(self, aircraft: Aircraft) -> Aircraft:
        """
        Create a new aircraft.

        Args:
            aircraft: Aircraft model to create

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
            if record:
                return Aircraft(**dict(record["a"]))
            raise QueryError("Failed to create aircraft")
        except Exception as e:
            raise QueryError(f"Error creating aircraft: {e}")

    def find_by_id(self, aircraft_id: str) -> Optional[Aircraft]:
        """
        Find an aircraft by ID.

        Args:
            aircraft_id: Aircraft ID to search for

        Returns:
            Aircraft if found, None otherwise
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a
        """
        result = self.session.run(query, aircraft_id=aircraft_id)
        record = result.single()
        if record:
            return Aircraft(**dict(record["a"]))
        return None

    def find_by_tail_number(self, tail_number: str) -> Optional[Aircraft]:
        """
        Find an aircraft by tail number.

        Args:
            tail_number: Tail number to search for

        Returns:
            Aircraft if found, None otherwise
        """
        query = """
        MATCH (a:Aircraft {tail_number: $tail_number})
        RETURN a
        """
        result = self.session.run(query, tail_number=tail_number)
        record = result.single()
        if record:
            return Aircraft(**dict(record["a"]))
        return None

    def find_all(self, limit: int = 100) -> List[Aircraft]:
        """
        Find all aircraft.

        Args:
            limit: Maximum number of results (default: 100)

        Returns:
            List of aircraft
        """
        query = """
        MATCH (a:Aircraft)
        RETURN a
        LIMIT $limit
        """
        result = self.session.run(query, limit=limit)
        return [Aircraft(**dict(record["a"])) for record in result]

    def update(self, aircraft: Aircraft) -> Aircraft:
        """
        Update an existing aircraft.

        Args:
            aircraft: Aircraft model with updated data

        Returns:
            Updated aircraft

        Raises:
            NotFoundError: If aircraft not found
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
            if record:
                return Aircraft(**dict(record["a"]))
            raise NotFoundError(f"Aircraft not found: {aircraft.aircraft_id}")
        except NotFoundError:
            raise
        except Exception as e:
            raise QueryError(f"Error updating aircraft: {e}")

    def delete(self, aircraft_id: str) -> bool:
        """
        Delete an aircraft.

        Args:
            aircraft_id: Aircraft ID to delete

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


class AirportRepository:
    """Repository for Airport entities."""

    def __init__(self, session: Session):
        """
        Initialize the repository.

        Args:
            session: Neo4j session instance
        """
        self.session = session

    def create(self, airport: Airport) -> Airport:
        """
        Create a new airport.

        Args:
            airport: Airport model to create

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
            if record:
                return Airport(**dict(record["a"]))
            raise QueryError("Failed to create airport")
        except Exception as e:
            raise QueryError(f"Error creating airport: {e}")

    def find_by_id(self, airport_id: str) -> Optional[Airport]:
        """
        Find an airport by ID.

        Args:
            airport_id: Airport ID to search for

        Returns:
            Airport if found, None otherwise
        """
        query = """
        MATCH (a:Airport {airport_id: $airport_id})
        RETURN a
        """
        result = self.session.run(query, airport_id=airport_id)
        record = result.single()
        if record:
            return Airport(**dict(record["a"]))
        return None

    def find_by_iata(self, iata: str) -> Optional[Airport]:
        """
        Find an airport by IATA code.

        Args:
            iata: IATA code to search for

        Returns:
            Airport if found, None otherwise
        """
        query = """
        MATCH (a:Airport {iata: $iata})
        RETURN a
        """
        result = self.session.run(query, iata=iata)
        record = result.single()
        if record:
            return Airport(**dict(record["a"]))
        return None

    def find_all(self, limit: int = 100) -> List[Airport]:
        """
        Find all airports.

        Args:
            limit: Maximum number of results (default: 100)

        Returns:
            List of airports
        """
        query = """
        MATCH (a:Airport)
        RETURN a
        LIMIT $limit
        """
        result = self.session.run(query, limit=limit)
        return [Airport(**dict(record["a"])) for record in result]


class FlightRepository:
    """Repository for Flight entities."""

    def __init__(self, session: Session):
        """
        Initialize the repository.

        Args:
            session: Neo4j session instance
        """
        self.session = session

    def create(self, flight: Flight) -> Flight:
        """
        Create a new flight.

        Args:
            flight: Flight model to create

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
            if record:
                return Flight(**dict(record["f"]))
            raise QueryError("Failed to create flight")
        except Exception as e:
            raise QueryError(f"Error creating flight: {e}")

    def find_by_id(self, flight_id: str) -> Optional[Flight]:
        """
        Find a flight by ID.

        Args:
            flight_id: Flight ID to search for

        Returns:
            Flight if found, None otherwise
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})
        RETURN f
        """
        result = self.session.run(query, flight_id=flight_id)
        record = result.single()
        if record:
            return Flight(**dict(record["f"]))
        return None

    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[Flight]:
        """
        Find flights operated by an aircraft.

        Args:
            aircraft_id: Aircraft ID to search for
            limit: Maximum number of results (default: 100)

        Returns:
            List of flights
        """
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})-[:OPERATES_FLIGHT]->(f:Flight)
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        result = self.session.run(query, aircraft_id=aircraft_id, limit=limit)
        return [Flight(**dict(record["f"])) for record in result]

    def find_all(self, limit: int = 100) -> List[Flight]:
        """
        Find all flights.

        Args:
            limit: Maximum number of results (default: 100)

        Returns:
            List of flights
        """
        query = """
        MATCH (f:Flight)
        RETURN f
        ORDER BY f.scheduled_departure DESC
        LIMIT $limit
        """
        result = self.session.run(query, limit=limit)
        return [Flight(**dict(record["f"])) for record in result]


class MaintenanceEventRepository:
    """Repository for MaintenanceEvent entities."""

    def __init__(self, session: Session):
        """
        Initialize the repository.

        Args:
            session: Neo4j session instance
        """
        self.session = session

    def create(self, event: MaintenanceEvent) -> MaintenanceEvent:
        """
        Create a new maintenance event.

        Args:
            event: MaintenanceEvent model to create

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
            if record:
                return MaintenanceEvent(**dict(record["m"]))
            raise QueryError("Failed to create maintenance event")
        except Exception as e:
            raise QueryError(f"Error creating maintenance event: {e}")

    def find_by_id(self, event_id: str) -> Optional[MaintenanceEvent]:
        """
        Find a maintenance event by ID.

        Args:
            event_id: Event ID to search for

        Returns:
            MaintenanceEvent if found, None otherwise
        """
        query = """
        MATCH (m:MaintenanceEvent {event_id: $event_id})
        RETURN m
        """
        result = self.session.run(query, event_id=event_id)
        record = result.single()
        if record:
            return MaintenanceEvent(**dict(record["m"]))
        return None

    def find_by_aircraft(self, aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find maintenance events for an aircraft.

        Args:
            aircraft_id: Aircraft ID to search for
            limit: Maximum number of results (default: 100)

        Returns:
            List of maintenance events
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
            List of maintenance events
        """
        query = """
        MATCH (m:MaintenanceEvent {severity: $severity})
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        result = self.session.run(query, severity=severity, limit=limit)
        return [MaintenanceEvent(**dict(record["m"])) for record in result]

    def find_all(self, limit: int = 100) -> List[MaintenanceEvent]:
        """
        Find all maintenance events.

        Args:
            limit: Maximum number of results (default: 100)

        Returns:
            List of maintenance events
        """
        query = """
        MATCH (m:MaintenanceEvent)
        RETURN m
        ORDER BY m.reported_at DESC
        LIMIT $limit
        """
        result = self.session.run(query, limit=limit)
        return [MaintenanceEvent(**dict(record["m"])) for record in result]


class DelayRepository:
    """Repository for Delay entities."""

    def __init__(self, session: Session):
        """
        Initialize the repository.

        Args:
            session: Neo4j session instance
        """
        self.session = session

    def create(self, delay: Delay) -> Delay:
        """
        Create a new delay.

        Args:
            delay: Delay model to create

        Returns:
            Created delay

        Raises:
            QueryError: If creation fails
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
                return Delay(**dict(record["d"]))
            raise QueryError("Failed to create delay")
        except Exception as e:
            raise QueryError(f"Error creating delay: {e}")

    def find_by_id(self, delay_id: str) -> Optional[Delay]:
        """
        Find a delay by ID.

        Args:
            delay_id: Delay ID to search for

        Returns:
            Delay if found, None otherwise
        """
        query = """
        MATCH (d:Delay {delay_id: $delay_id})
        RETURN d
        """
        result = self.session.run(query, delay_id=delay_id)
        record = result.single()
        if record:
            return Delay(**dict(record["d"]))
        return None

    def find_by_flight(self, flight_id: str) -> List[Delay]:
        """
        Find delays for a flight.

        Args:
            flight_id: Flight ID to search for

        Returns:
            List of delays
        """
        query = """
        MATCH (f:Flight {flight_id: $flight_id})-[:HAS_DELAY]->(d:Delay)
        RETURN d
        """
        result = self.session.run(query, flight_id=flight_id)
        return [Delay(**dict(record["d"])) for record in result]

    def find_significant_delays(self, min_minutes: int = 30, limit: int = 100) -> List[Delay]:
        """
        Find significant delays.

        Args:
            min_minutes: Minimum delay duration in minutes (default: 30)
            limit: Maximum number of results (default: 100)

        Returns:
            List of delays
        """
        query = """
        MATCH (d:Delay)
        WHERE d.minutes >= $min_minutes
        RETURN d
        ORDER BY d.minutes DESC
        LIMIT $limit
        """
        result = self.session.run(query, min_minutes=min_minutes, limit=limit)
        return [Delay(**dict(record["d"])) for record in result]

    def find_all(self, limit: int = 100) -> List[Delay]:
        """
        Find all delays.

        Args:
            limit: Maximum number of results (default: 100)

        Returns:
            List of delays
        """
        query = """
        MATCH (d:Delay)
        RETURN d
        LIMIT $limit
        """
        result = self.session.run(query, limit=limit)
        return [Delay(**dict(record["d"])) for record in result]
