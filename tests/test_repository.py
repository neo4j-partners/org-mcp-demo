"""Tests for Neo4j client repositories."""

import pytest

from neo4j_client import (
    Aircraft,
    Airport,
    Flight,
    MaintenanceEvent,
    Delay,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    DelayRepository,
    NotFoundError,
)


class TestAircraftRepository:
    """Test cases for AircraftRepository."""

    def test_create_aircraft(self, neo4j_session):
        """Test creating an aircraft."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="test_aircraft_001",
            tail_number="N12345",
            icao24="A1B2C3",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        
        created = repo.create(aircraft)
        assert created.aircraft_id == aircraft.aircraft_id
        assert created.tail_number == aircraft.tail_number

    def test_find_by_id(self, neo4j_session):
        """Test finding an aircraft by ID."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="test_aircraft_002",
            tail_number="N67890",
            icao24="D4E5F6",
            model="Airbus A320",
            operator="Test Airways",
            manufacturer="Airbus"
        )
        repo.create(aircraft)
        
        found = repo.find_by_id("test_aircraft_002")
        assert found is not None
        assert found.aircraft_id == "test_aircraft_002"
        assert found.model == "Airbus A320"

    def test_find_by_id_not_found(self, neo4j_session):
        """Test finding a non-existent aircraft."""
        repo = AircraftRepository(neo4j_session)
        found = repo.find_by_id("nonexistent")
        assert found is None

    def test_find_by_tail_number(self, neo4j_session):
        """Test finding an aircraft by tail number."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="test_aircraft_003",
            tail_number="N11111",
            icao24="G7H8I9",
            model="Boeing 777-300ER",
            operator="Global Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        found = repo.find_by_tail_number("N11111")
        assert found is not None
        assert found.tail_number == "N11111"

    def test_update_aircraft(self, neo4j_session):
        """Test updating an aircraft."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="test_aircraft_004",
            tail_number="N22222",
            icao24="J1K2L3",
            model="Boeing 787-9",
            operator="Original Operator",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        aircraft.operator = "New Operator"
        updated = repo.update(aircraft)
        assert updated.operator == "New Operator"

    def test_update_nonexistent_aircraft(self, neo4j_session):
        """Test updating a non-existent aircraft raises NotFoundError."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="nonexistent",
            tail_number="N99999",
            icao24="Z9Y8X7",
            model="Test Model",
            operator="Test Operator",
            manufacturer="Test Manufacturer"
        )
        
        with pytest.raises(NotFoundError):
            repo.update(aircraft)

    def test_delete_aircraft(self, neo4j_session):
        """Test deleting an aircraft."""
        repo = AircraftRepository(neo4j_session)
        aircraft = Aircraft(
            aircraft_id="test_aircraft_005",
            tail_number="N33333",
            icao24="M4N5O6",
            model="Airbus A350-900",
            operator="Euro Airways",
            manufacturer="Airbus"
        )
        repo.create(aircraft)
        
        deleted = repo.delete("test_aircraft_005")
        assert deleted is True
        
        found = repo.find_by_id("test_aircraft_005")
        assert found is None

    def test_delete_nonexistent_aircraft(self, neo4j_session):
        """Test deleting a non-existent aircraft returns False."""
        repo = AircraftRepository(neo4j_session)
        deleted = repo.delete("nonexistent")
        assert deleted is False


class TestAirportRepository:
    """Test cases for AirportRepository."""

    def test_create_airport(self, neo4j_session):
        """Test creating an airport."""
        repo = AirportRepository(neo4j_session)
        airport = Airport(
            airport_id="test_airport_001",
            iata="TST",
            icao="KTST",
            name="Test International Airport",
            city="Test City",
            country="Test Country",
            lat=40.7128,
            lon=-74.0060
        )
        
        created = repo.create(airport)
        assert created.airport_id == airport.airport_id
        assert created.iata == "TST"

    def test_find_by_iata(self, neo4j_session):
        """Test finding an airport by IATA code."""
        repo = AirportRepository(neo4j_session)
        airport = Airport(
            airport_id="test_airport_002",
            iata="ABC",
            icao="KABC",
            name="ABC Airport",
            city="ABC City",
            country="USA",
            lat=34.0522,
            lon=-118.2437
        )
        repo.create(airport)
        
        found = repo.find_by_iata("ABC")
        assert found is not None
        assert found.iata == "ABC"


class TestFlightRepository:
    """Test cases for FlightRepository."""

    def test_create_flight(self, neo4j_session):
        """Test creating a flight."""
        repo = FlightRepository(neo4j_session)
        flight = Flight(
            flight_id="test_flight_001",
            flight_number="TA123",
            aircraft_id="test_aircraft_001",
            operator="Test Airlines",
            origin="TST",
            destination="ABC",
            scheduled_departure="2024-01-15T08:00:00Z",
            scheduled_arrival="2024-01-15T12:00:00Z"
        )
        
        created = repo.create(flight)
        assert created.flight_id == flight.flight_id
        assert created.flight_number == "TA123"

    def test_find_by_id(self, neo4j_session):
        """Test finding a flight by ID."""
        repo = FlightRepository(neo4j_session)
        flight = Flight(
            flight_id="test_flight_002",
            flight_number="TA456",
            aircraft_id="test_aircraft_001",
            operator="Test Airlines",
            origin="ABC",
            destination="TST",
            scheduled_departure="2024-01-16T14:00:00Z",
            scheduled_arrival="2024-01-16T18:00:00Z"
        )
        repo.create(flight)
        
        found = repo.find_by_id("test_flight_002")
        assert found is not None
        assert found.flight_number == "TA456"


class TestMaintenanceEventRepository:
    """Test cases for MaintenanceEventRepository."""

    def test_create_maintenance_event(self, neo4j_session):
        """Test creating a maintenance event."""
        repo = MaintenanceEventRepository(neo4j_session)
        event = MaintenanceEvent(
            event_id="test_event_001",
            aircraft_id="test_aircraft_001",
            system_id="test_system_001",
            component_id="test_component_001",
            fault="Test fault description",
            severity="WARNING",
            reported_at="2024-01-15T10:30:00Z",
            corrective_action="Test corrective action"
        )
        
        created = repo.create(event)
        assert created.event_id == event.event_id
        assert created.severity == "WARNING"

    def test_find_by_severity(self, neo4j_session):
        """Test finding maintenance events by severity."""
        repo = MaintenanceEventRepository(neo4j_session)
        event = MaintenanceEvent(
            event_id="test_event_002",
            aircraft_id="test_aircraft_001",
            system_id="test_system_001",
            component_id="test_component_001",
            fault="Critical fault",
            severity="CRITICAL",
            reported_at="2024-01-15T11:00:00Z",
            corrective_action="Immediate repair"
        )
        repo.create(event)
        
        events = repo.find_by_severity("CRITICAL")
        assert len(events) > 0
        assert any(e.event_id == "test_event_002" for e in events)


class TestDelayRepository:
    """Test cases for DelayRepository."""

    def test_create_delay(self, neo4j_session):
        """Test creating a delay."""
        repo = DelayRepository(neo4j_session)
        delay = Delay(
            delay_id="test_delay_001",
            flight_id="test_flight_001",
            cause="Weather",
            minutes=45
        )
        
        created = repo.create(delay)
        assert created.delay_id == delay.delay_id
        assert created.minutes == 45

    def test_find_significant_delays(self, neo4j_session):
        """Test finding significant delays."""
        repo = DelayRepository(neo4j_session)
        delay = Delay(
            delay_id="test_delay_002",
            flight_id="test_flight_001",
            cause="Mechanical",
            minutes=120
        )
        repo.create(delay)
        
        delays = repo.find_significant_delays(min_minutes=60)
        assert len(delays) > 0
        assert any(d.delay_id == "test_delay_002" for d in delays)
