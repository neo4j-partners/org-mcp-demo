"""Integration tests for repository classes."""

import pytest
from neo4j_client.models import Aircraft, Airport, Flight, MaintenanceEvent, Delay
from neo4j_client.repository import (
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    DelayRepository,
)
from neo4j_client.exceptions import NotFoundError


class TestAircraftRepository:
    """Tests for AircraftRepository."""

    def test_create_aircraft(self, neo4j_session):
        """Test creating a new aircraft."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="A001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing",
        )

        created = repo.create(aircraft)

        assert created.aircraft_id == "A001"
        assert created.tail_number == "N12345"
        assert created.model == "Boeing 737-800"

    def test_find_by_id(self, neo4j_session):
        """Test finding an aircraft by ID."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="A002",
            tail_number="N67890",
            icao24="A67890",
            model="Airbus A320",
            operator="Test Airways",
            manufacturer="Airbus",
        )
        repo.create(aircraft)

        found = repo.find_by_id("A002")

        assert found is not None
        assert found.aircraft_id == "A002"
        assert found.tail_number == "N67890"

    def test_find_by_id_not_found(self, neo4j_session):
        """Test finding a non-existent aircraft."""
        repo = AircraftRepository(neo4j_session)

        found = repo.find_by_id("NONEXISTENT")

        assert found is None

    def test_find_by_tail_number(self, neo4j_session):
        """Test finding an aircraft by tail number."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="A003",
            tail_number="N11111",
            icao24="A11111",
            model="Boeing 777",
            operator="Global Air",
            manufacturer="Boeing",
        )
        repo.create(aircraft)

        found = repo.find_by_tail_number("N11111")

        assert found is not None
        assert found.aircraft_id == "A003"

    def test_find_all(self, neo4j_session):
        """Test finding all aircraft."""
        repo = AircraftRepository(neo4j_session)
        
        # Create multiple aircraft
        for i in range(3):
            aircraft = Aircraft(
                aircraft_id=f"A{i:03d}",
                tail_number=f"N{i:05d}",
                icao24=f"A{i:05d}",
                model="Boeing 737",
                operator="Test Airlines",
                manufacturer="Boeing",
            )
            repo.create(aircraft)

        aircraft_list = repo.find_all()

        assert len(aircraft_list) == 3

    def test_update_aircraft(self, neo4j_session):
        """Test updating an existing aircraft."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="A004",
            tail_number="N22222",
            icao24="A22222",
            model="Boeing 737-700",
            operator="Old Operator",
            manufacturer="Boeing",
        )
        repo.create(aircraft)

        # Update the aircraft
        aircraft.operator = "New Operator"
        updated = repo.update(aircraft)

        assert updated.operator == "New Operator"

        # Verify the update persisted
        found = repo.find_by_id("A004")
        assert found.operator == "New Operator"

    def test_update_nonexistent_aircraft(self, neo4j_session):
        """Test updating a non-existent aircraft."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="NONEXISTENT",
            tail_number="N99999",
            icao24="A99999",
            model="Boeing 737",
            operator="Test Airlines",
            manufacturer="Boeing",
        )

        with pytest.raises(NotFoundError):
            repo.update(aircraft)

    def test_delete_aircraft(self, neo4j_session):
        """Test deleting an aircraft."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="A005",
            tail_number="N33333",
            icao24="A33333",
            model="Airbus A380",
            operator="Mega Airlines",
            manufacturer="Airbus",
        )
        repo.create(aircraft)

        # Delete the aircraft
        deleted = repo.delete("A005")
        assert deleted is True

        # Verify it's gone
        found = repo.find_by_id("A005")
        assert found is None

    def test_delete_nonexistent_aircraft(self, neo4j_session):
        """Test deleting a non-existent aircraft."""
        repo = AircraftRepository(neo4j_session)

        deleted = repo.delete("NONEXISTENT")
        assert deleted is False


class TestAirportRepository:
    """Tests for AirportRepository."""

    def test_create_airport(self, neo4j_session):
        """Test creating a new airport."""
        repo = AirportRepository(neo4j_session)
        airport = Airport(
            airport_id="AP001",
            iata="LAX",
            icao="KLAX",
            name="Los Angeles International Airport",
            city="Los Angeles",
            country="United States",
            lat=33.9425,
            lon=-118.408,
        )

        created = repo.create(airport)

        assert created.airport_id == "AP001"
        assert created.iata == "LAX"
        assert created.name == "Los Angeles International Airport"

    def test_find_by_iata(self, neo4j_session):
        """Test finding an airport by IATA code."""
        repo = AirportRepository(neo4j_session)
        airport = Airport(
            airport_id="AP002",
            iata="JFK",
            icao="KJFK",
            name="John F. Kennedy International Airport",
            city="New York",
            country="United States",
            lat=40.6413,
            lon=-73.7781,
        )
        repo.create(airport)

        found = repo.find_by_iata("JFK")

        assert found is not None
        assert found.airport_id == "AP002"

    def test_delete_airport(self, neo4j_session):
        """Test deleting an airport."""
        repo = AirportRepository(neo4j_session)
        airport = Airport(
            airport_id="AP003",
            iata="ORD",
            icao="KORD",
            name="O'Hare International Airport",
            city="Chicago",
            country="United States",
            lat=41.9742,
            lon=-87.9073,
        )
        repo.create(airport)

        deleted = repo.delete("AP003")
        assert deleted is True


class TestFlightRepository:
    """Tests for FlightRepository."""

    def test_create_flight(self, neo4j_session):
        """Test creating a new flight."""
        repo = FlightRepository(neo4j_session)
        flight = Flight(
            flight_id="F001",
            flight_number="AA100",
            aircraft_id="A001",
            operator="American Airlines",
            origin="LAX",
            destination="JFK",
            scheduled_departure="2024-01-15T08:00:00Z",
            scheduled_arrival="2024-01-15T16:30:00Z",
        )

        created = repo.create(flight)

        assert created.flight_id == "F001"
        assert created.flight_number == "AA100"
        assert created.origin == "LAX"

    def test_find_by_aircraft(self, neo4j_session):
        """Test finding flights for a specific aircraft."""
        # Create aircraft and flights with relationships
        neo4j_session.run("""
            CREATE (a:Aircraft {aircraft_id: 'A010'})
            CREATE (f1:Flight {
                flight_id: 'F010',
                flight_number: 'AA100',
                aircraft_id: 'A010',
                operator: 'American Airlines',
                origin: 'LAX',
                destination: 'JFK',
                scheduled_departure: '2024-01-15T08:00:00Z',
                scheduled_arrival: '2024-01-15T16:30:00Z'
            })
            CREATE (f2:Flight {
                flight_id: 'F011',
                flight_number: 'AA101',
                aircraft_id: 'A010',
                operator: 'American Airlines',
                origin: 'JFK',
                destination: 'LAX',
                scheduled_departure: '2024-01-16T08:00:00Z',
                scheduled_arrival: '2024-01-16T16:30:00Z'
            })
            CREATE (a)-[:OPERATES_FLIGHT]->(f1)
            CREATE (a)-[:OPERATES_FLIGHT]->(f2)
        """)

        repo = FlightRepository(neo4j_session)
        flights = repo.find_by_aircraft("A010")

        assert len(flights) == 2

    def test_delete_flight(self, neo4j_session):
        """Test deleting a flight."""
        repo = FlightRepository(neo4j_session)
        flight = Flight(
            flight_id="F002",
            flight_number="DL200",
            aircraft_id="A002",
            operator="Delta Airlines",
            origin="ATL",
            destination="LAX",
            scheduled_departure="2024-01-15T10:00:00Z",
            scheduled_arrival="2024-01-15T12:30:00Z",
        )
        repo.create(flight)

        deleted = repo.delete("F002")
        assert deleted is True


class TestMaintenanceEventRepository:
    """Tests for MaintenanceEventRepository."""

    def test_create_maintenance_event(self, neo4j_session):
        """Test creating a new maintenance event."""
        repo = MaintenanceEventRepository(neo4j_session)
        event = MaintenanceEvent(
            event_id="M001",
            aircraft_id="A001",
            system_id="S001",
            component_id="C001",
            fault="Hydraulic pressure low",
            severity="WARNING",
            reported_at="2024-01-15T10:30:00Z",
            corrective_action="Replaced hydraulic pump",
        )

        created = repo.create(event)

        assert created.event_id == "M001"
        assert created.fault == "Hydraulic pressure low"
        assert created.severity == "WARNING"

    def test_find_by_severity(self, neo4j_session):
        """Test finding maintenance events by severity."""
        repo = MaintenanceEventRepository(neo4j_session)
        
        # Create events with different severities
        critical_event = MaintenanceEvent(
            event_id="M002",
            aircraft_id="A001",
            system_id="S001",
            component_id="C001",
            fault="Engine failure",
            severity="CRITICAL",
            reported_at="2024-01-15T11:00:00Z",
            corrective_action="Engine replaced",
        )
        warning_event = MaintenanceEvent(
            event_id="M003",
            aircraft_id="A001",
            system_id="S002",
            component_id="C002",
            fault="Minor leak",
            severity="WARNING",
            reported_at="2024-01-15T12:00:00Z",
            corrective_action="Seal replaced",
        )
        
        repo.create(critical_event)
        repo.create(warning_event)

        critical_events = repo.find_by_severity("CRITICAL")

        assert len(critical_events) == 1
        assert critical_events[0].event_id == "M002"

    def test_find_by_aircraft(self, neo4j_session):
        """Test finding maintenance events for a specific aircraft."""
        # Create aircraft and maintenance events with relationships
        neo4j_session.run("""
            CREATE (a:Aircraft {aircraft_id: 'A020'})
            CREATE (m1:MaintenanceEvent {
                event_id: 'M020',
                aircraft_id: 'A020',
                system_id: 'S020',
                component_id: 'C020',
                fault: 'Test fault 1',
                severity: 'WARNING',
                reported_at: '2024-01-15T10:00:00Z',
                corrective_action: 'Fixed'
            })
            CREATE (m2:MaintenanceEvent {
                event_id: 'M021',
                aircraft_id: 'A020',
                system_id: 'S021',
                component_id: 'C021',
                fault: 'Test fault 2',
                severity: 'CRITICAL',
                reported_at: '2024-01-16T10:00:00Z',
                corrective_action: 'Fixed'
            })
            CREATE (m1)-[:AFFECTS_AIRCRAFT]->(a)
            CREATE (m2)-[:AFFECTS_AIRCRAFT]->(a)
        """)

        repo = MaintenanceEventRepository(neo4j_session)
        events = repo.find_by_aircraft("A020")

        assert len(events) == 2


class TestDelayRepository:
    """Tests for DelayRepository."""

    def test_create_delay(self, neo4j_session):
        """Test creating a new delay."""
        repo = DelayRepository(neo4j_session)
        delay = Delay(
            delay_id="D001",
            flight_id="F001",
            cause="Weather",
            minutes=45,
        )

        created = repo.create(delay)

        assert created.delay_id == "D001"
        assert created.cause == "Weather"
        assert created.minutes == 45

    def test_find_significant_delays(self, neo4j_session):
        """Test finding delays exceeding a minimum duration."""
        repo = DelayRepository(neo4j_session)
        
        # Create delays with different durations
        short_delay = Delay(
            delay_id="D002",
            flight_id="F002",
            cause="Boarding",
            minutes=15,
        )
        long_delay = Delay(
            delay_id="D003",
            flight_id="F003",
            cause="Maintenance",
            minutes=120,
        )
        
        repo.create(short_delay)
        repo.create(long_delay)

        significant_delays = repo.find_significant_delays(min_minutes=30)

        assert len(significant_delays) == 1
        assert significant_delays[0].delay_id == "D003"
        assert significant_delays[0].minutes == 120

    def test_find_by_flight(self, neo4j_session):
        """Test finding delays for a specific flight."""
        # Create flight and delays with relationships
        neo4j_session.run("""
            CREATE (f:Flight {flight_id: 'F030'})
            CREATE (d1:Delay {
                delay_id: 'D030',
                flight_id: 'F030',
                cause: 'Weather',
                minutes: 30
            })
            CREATE (d2:Delay {
                delay_id: 'D031',
                flight_id: 'F030',
                cause: 'Mechanical',
                minutes: 60
            })
            CREATE (f)-[:HAS_DELAY]->(d1)
            CREATE (f)-[:HAS_DELAY]->(d2)
        """)

        repo = DelayRepository(neo4j_session)
        delays = repo.find_by_flight("F030")

        assert len(delays) == 2
