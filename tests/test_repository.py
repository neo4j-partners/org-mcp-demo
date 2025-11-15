"""Integration tests for Neo4j repositories."""

import pytest
from neo4j_client import (
    Aircraft,
    Airport,
    Flight,
    MaintenanceEvent,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    NotFoundError,
)


class TestAircraftRepository:
    """Test cases for AircraftRepository."""
    
    def test_create_aircraft(self, clean_database):
        """Test creating a new aircraft."""
        repo = AircraftRepository(clean_database)
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        
        result = repo.create(aircraft)
        assert result.aircraft_id == "AC001"
        assert result.tail_number == "N12345"
    
    def test_find_by_id(self, clean_database):
        """Test finding aircraft by ID."""
        repo = AircraftRepository(clean_database)
        aircraft = Aircraft(
            aircraft_id="AC002",
            tail_number="N67890",
            icao24="A67890",
            model="Airbus A320",
            operator="Test Airlines",
            manufacturer="Airbus"
        )
        repo.create(aircraft)
        
        found = repo.find_by_id("AC002")
        assert found is not None
        assert found.aircraft_id == "AC002"
        assert found.model == "Airbus A320"
    
    def test_find_by_id_not_found(self, clean_database):
        """Test finding non-existent aircraft."""
        repo = AircraftRepository(clean_database)
        found = repo.find_by_id("NONEXISTENT")
        assert found is None
    
    def test_find_by_tail_number(self, clean_database):
        """Test finding aircraft by tail number."""
        repo = AircraftRepository(clean_database)
        aircraft = Aircraft(
            aircraft_id="AC003",
            tail_number="N99999",
            icao24="A99999",
            model="Boeing 777",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        found = repo.find_by_tail_number("N99999")
        assert found is not None
        assert found.aircraft_id == "AC003"
    
    def test_find_all(self, clean_database):
        """Test finding all aircraft."""
        repo = AircraftRepository(clean_database)
        
        aircraft1 = Aircraft(
            aircraft_id="AC004",
            tail_number="N11111",
            icao24="A11111",
            model="Boeing 737",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        aircraft2 = Aircraft(
            aircraft_id="AC005",
            tail_number="N22222",
            icao24="A22222",
            model="Airbus A320",
            operator="Test Airlines",
            manufacturer="Airbus"
        )
        
        repo.create(aircraft1)
        repo.create(aircraft2)
        
        all_aircraft = repo.find_all()
        assert len(all_aircraft) == 2
    
    def test_update_aircraft(self, clean_database):
        """Test updating an aircraft."""
        repo = AircraftRepository(clean_database)
        aircraft = Aircraft(
            aircraft_id="AC006",
            tail_number="N33333",
            icao24="A33333",
            model="Boeing 737-800",
            operator="Old Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        aircraft.operator = "New Airlines"
        updated = repo.update(aircraft)
        
        found = repo.find_by_id("AC006")
        assert found.operator == "New Airlines"
    
    def test_update_nonexistent(self, clean_database):
        """Test updating non-existent aircraft raises error."""
        repo = AircraftRepository(clean_database)
        aircraft = Aircraft(
            aircraft_id="NONEXISTENT",
            tail_number="N00000",
            icao24="A00000",
            model="Test",
            operator="Test",
            manufacturer="Test"
        )
        
        with pytest.raises(NotFoundError):
            repo.update(aircraft)
    
    def test_delete_aircraft(self, clean_database):
        """Test deleting an aircraft."""
        repo = AircraftRepository(clean_database)
        aircraft = Aircraft(
            aircraft_id="AC007",
            tail_number="N44444",
            icao24="A44444",
            model="Boeing 787",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        deleted = repo.delete("AC007")
        assert deleted is True
        
        found = repo.find_by_id("AC007")
        assert found is None
    
    def test_delete_nonexistent(self, clean_database):
        """Test deleting non-existent aircraft returns False."""
        repo = AircraftRepository(clean_database)
        deleted = repo.delete("NONEXISTENT")
        assert deleted is False


class TestAirportRepository:
    """Test cases for AirportRepository."""
    
    def test_create_airport(self, clean_database):
        """Test creating a new airport."""
        repo = AirportRepository(clean_database)
        airport = Airport(
            airport_id="AP001",
            iata="LAX",
            icao="KLAX",
            name="Los Angeles International",
            city="Los Angeles",
            country="USA",
            lat=33.9425,
            lon=-118.408
        )
        
        result = repo.create(airport)
        assert result.airport_id == "AP001"
        assert result.iata == "LAX"
    
    def test_find_by_iata(self, clean_database):
        """Test finding airport by IATA code."""
        repo = AirportRepository(clean_database)
        airport = Airport(
            airport_id="AP002",
            iata="JFK",
            icao="KJFK",
            name="John F Kennedy International",
            city="New York",
            country="USA",
            lat=40.6413,
            lon=-73.7781
        )
        repo.create(airport)
        
        found = repo.find_by_iata("JFK")
        assert found is not None
        assert found.airport_id == "AP002"
        assert found.name == "John F Kennedy International"


class TestFlightRepository:
    """Test cases for FlightRepository."""
    
    def test_create_flight(self, clean_database):
        """Test creating a new flight."""
        repo = FlightRepository(clean_database)
        flight = Flight(
            flight_id="FL001",
            flight_number="AA100",
            aircraft_id="AC001",
            operator="American Airlines",
            origin="LAX",
            destination="JFK",
            scheduled_departure="2024-01-01T10:00:00Z",
            scheduled_arrival="2024-01-01T18:00:00Z"
        )
        
        result = repo.create(flight)
        assert result.flight_id == "FL001"
        assert result.flight_number == "AA100"
    
    def test_find_by_id(self, clean_database):
        """Test finding flight by ID."""
        repo = FlightRepository(clean_database)
        flight = Flight(
            flight_id="FL002",
            flight_number="UA200",
            aircraft_id="AC002",
            operator="United Airlines",
            origin="SFO",
            destination="ORD",
            scheduled_departure="2024-01-02T08:00:00Z",
            scheduled_arrival="2024-01-02T14:00:00Z"
        )
        repo.create(flight)
        
        found = repo.find_by_id("FL002")
        assert found is not None
        assert found.flight_number == "UA200"


class TestMaintenanceEventRepository:
    """Test cases for MaintenanceEventRepository."""
    
    def test_create_maintenance_event(self, clean_database):
        """Test creating a maintenance event."""
        repo = MaintenanceEventRepository(clean_database)
        event = MaintenanceEvent(
            event_id="ME001",
            aircraft_id="AC001",
            system_id="SYS001",
            component_id="COMP001",
            fault="Hydraulic pressure low",
            severity="WARNING",
            reported_at="2024-01-01T12:00:00Z",
            corrective_action="Replaced hydraulic pump"
        )
        
        result = repo.create(event)
        assert result.event_id == "ME001"
        assert result.severity == "WARNING"
    
    def test_find_by_severity(self, clean_database):
        """Test finding events by severity."""
        repo = MaintenanceEventRepository(clean_database)
        
        event1 = MaintenanceEvent(
            event_id="ME002",
            aircraft_id="AC001",
            system_id="SYS001",
            component_id="COMP001",
            fault="Critical failure",
            severity="CRITICAL",
            reported_at="2024-01-01T10:00:00Z",
            corrective_action="Emergency repair"
        )
        event2 = MaintenanceEvent(
            event_id="ME003",
            aircraft_id="AC002",
            system_id="SYS002",
            component_id="COMP002",
            fault="Minor issue",
            severity="WARNING",
            reported_at="2024-01-01T11:00:00Z",
            corrective_action="Routine maintenance"
        )
        
        repo.create(event1)
        repo.create(event2)
        
        critical_events = repo.find_by_severity("CRITICAL")
        assert len(critical_events) == 1
        assert critical_events[0].event_id == "ME002"
