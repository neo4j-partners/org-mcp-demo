"""Tests for repository pattern."""

import pytest
from neo4j_client import (
    AircraftRepository,
    FlightRepository,
    MaintenanceEventRepository,
    Aircraft,
    Flight,
    MaintenanceEvent,
)


class TestAircraftRepository:
    """Tests for AircraftRepository."""
    
    @pytest.fixture
    def aircraft_repo(self, neo4j_connection):
        """Create AircraftRepository instance."""
        return AircraftRepository(neo4j_connection)
    
    @pytest.fixture
    def sample_aircraft(self):
        """Create a sample aircraft for testing."""
        return Aircraft(
            aircraft_id="A001",
            tail_number="N12345",
            icao24="ABC123",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
    
    def test_create_aircraft(self, aircraft_repo, sample_aircraft):
        """Test creating an aircraft."""
        created = aircraft_repo.create(sample_aircraft)
        assert created.aircraft_id == sample_aircraft.aircraft_id
        assert created.tail_number == sample_aircraft.tail_number
        assert created.model == sample_aircraft.model
    
    def test_find_by_id(self, aircraft_repo, sample_aircraft):
        """Test finding aircraft by ID."""
        aircraft_repo.create(sample_aircraft)
        found = aircraft_repo.find_by_id(sample_aircraft.aircraft_id)
        assert found is not None
        assert found.aircraft_id == sample_aircraft.aircraft_id
        assert found.tail_number == sample_aircraft.tail_number
    
    def test_find_by_id_not_found(self, aircraft_repo):
        """Test finding non-existent aircraft."""
        found = aircraft_repo.find_by_id("NONEXISTENT")
        assert found is None
    
    def test_find_by_tail_number(self, aircraft_repo, sample_aircraft):
        """Test finding aircraft by tail number."""
        aircraft_repo.create(sample_aircraft)
        found = aircraft_repo.find_by_tail_number(sample_aircraft.tail_number)
        assert found is not None
        assert found.tail_number == sample_aircraft.tail_number
    
    def test_find_all(self, aircraft_repo, sample_aircraft):
        """Test finding all aircraft."""
        aircraft_repo.create(sample_aircraft)
        
        # Create a second aircraft
        aircraft2 = Aircraft(
            aircraft_id="A002",
            tail_number="N67890",
            icao24="DEF456",
            model="Airbus A320",
            operator="Test Airlines",
            manufacturer="Airbus"
        )
        aircraft_repo.create(aircraft2)
        
        all_aircraft = aircraft_repo.find_all()
        assert len(all_aircraft) == 2
    
    def test_update_aircraft(self, aircraft_repo, sample_aircraft):
        """Test updating an aircraft."""
        aircraft_repo.create(sample_aircraft)
        
        # Update the aircraft
        sample_aircraft.operator = "Updated Airlines"
        updated = aircraft_repo.update(sample_aircraft)
        assert updated.operator == "Updated Airlines"
        
        # Verify update persisted
        found = aircraft_repo.find_by_id(sample_aircraft.aircraft_id)
        assert found.operator == "Updated Airlines"
    
    def test_delete_aircraft(self, aircraft_repo, sample_aircraft):
        """Test deleting an aircraft."""
        aircraft_repo.create(sample_aircraft)
        
        # Delete the aircraft
        deleted = aircraft_repo.delete(sample_aircraft.aircraft_id)
        assert deleted is True
        
        # Verify deletion
        found = aircraft_repo.find_by_id(sample_aircraft.aircraft_id)
        assert found is None
    
    def test_delete_nonexistent_aircraft(self, aircraft_repo):
        """Test deleting a non-existent aircraft."""
        deleted = aircraft_repo.delete("NONEXISTENT")
        assert deleted is False


class TestFlightRepository:
    """Tests for FlightRepository."""
    
    @pytest.fixture
    def flight_repo(self, neo4j_connection):
        """Create FlightRepository instance."""
        return FlightRepository(neo4j_connection)
    
    @pytest.fixture
    def sample_flight(self):
        """Create a sample flight for testing."""
        return Flight(
            flight_id="F001",
            flight_number="AA100",
            aircraft_id="A001",
            operator="Test Airlines",
            origin="LAX",
            destination="JFK",
            scheduled_departure="2024-01-01T10:00:00Z",
            scheduled_arrival="2024-01-01T18:00:00Z"
        )
    
    def test_create_flight(self, flight_repo, sample_flight):
        """Test creating a flight."""
        created = flight_repo.create(sample_flight)
        assert created.flight_id == sample_flight.flight_id
        assert created.flight_number == sample_flight.flight_number
        assert created.origin == sample_flight.origin
        assert created.destination == sample_flight.destination
    
    def test_find_by_id(self, flight_repo, sample_flight):
        """Test finding flight by ID."""
        flight_repo.create(sample_flight)
        found = flight_repo.find_by_id(sample_flight.flight_id)
        assert found is not None
        assert found.flight_id == sample_flight.flight_id
    
    def test_find_by_flight_number(self, flight_repo, sample_flight):
        """Test finding flights by flight number."""
        flight_repo.create(sample_flight)
        flights = flight_repo.find_by_flight_number(sample_flight.flight_number)
        assert len(flights) == 1
        assert flights[0].flight_number == sample_flight.flight_number
    
    def test_find_all(self, flight_repo, sample_flight):
        """Test finding all flights."""
        flight_repo.create(sample_flight)
        all_flights = flight_repo.find_all()
        assert len(all_flights) >= 1


class TestMaintenanceEventRepository:
    """Tests for MaintenanceEventRepository."""
    
    @pytest.fixture
    def maintenance_repo(self, neo4j_connection):
        """Create MaintenanceEventRepository instance."""
        return MaintenanceEventRepository(neo4j_connection)
    
    @pytest.fixture
    def sample_event(self):
        """Create a sample maintenance event for testing."""
        return MaintenanceEvent(
            event_id="E001",
            aircraft_id="A001",
            system_id="S001",
            component_id="C001",
            fault="Hydraulic leak detected",
            severity="CRITICAL",
            reported_at="2024-01-01T12:00:00Z",
            corrective_action="Replaced hydraulic pump"
        )
    
    def test_create_maintenance_event(self, maintenance_repo, sample_event):
        """Test creating a maintenance event."""
        created = maintenance_repo.create(sample_event)
        assert created.event_id == sample_event.event_id
        assert created.fault == sample_event.fault
        assert created.severity == sample_event.severity
    
    def test_find_by_id(self, maintenance_repo, sample_event):
        """Test finding maintenance event by ID."""
        maintenance_repo.create(sample_event)
        found = maintenance_repo.find_by_id(sample_event.event_id)
        assert found is not None
        assert found.event_id == sample_event.event_id
    
    def test_find_by_severity(self, maintenance_repo, sample_event):
        """Test finding maintenance events by severity."""
        maintenance_repo.create(sample_event)
        
        # Create another event with different severity
        event2 = MaintenanceEvent(
            event_id="E002",
            aircraft_id="A001",
            system_id="S001",
            component_id="C002",
            fault="Minor sensor issue",
            severity="WARNING",
            reported_at="2024-01-02T12:00:00Z",
            corrective_action="Recalibrated sensor"
        )
        maintenance_repo.create(event2)
        
        critical_events = maintenance_repo.find_by_severity("CRITICAL")
        assert len(critical_events) == 1
        assert critical_events[0].severity == "CRITICAL"
        
        warning_events = maintenance_repo.find_by_severity("WARNING")
        assert len(warning_events) == 1
        assert warning_events[0].severity == "WARNING"
    
    def test_find_all(self, maintenance_repo, sample_event):
        """Test finding all maintenance events."""
        maintenance_repo.create(sample_event)
        all_events = maintenance_repo.find_all()
        assert len(all_events) >= 1
