"""Tests for repository operations."""

import pytest
from neo4j_client.models import Aircraft, Airport, Flight, MaintenanceEvent
from neo4j_client.repository import (
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
)
from neo4j_client.exceptions import NotFoundError


class TestAircraftRepository:
    """Tests for AircraftRepository."""
    
    def test_create_aircraft(self, session):
        """Test creating an aircraft."""
        repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        
        created = repo.create(aircraft)
        assert created.aircraft_id == "AC001"
        assert created.tail_number == "N12345"
    
    def test_find_by_id(self, session):
        """Test finding aircraft by ID."""
        repo = AircraftRepository(session)
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
    
    def test_find_by_id_not_found(self, session):
        """Test finding non-existent aircraft."""
        repo = AircraftRepository(session)
        found = repo.find_by_id("NONEXISTENT")
        assert found is None
    
    def test_find_by_tail_number(self, session):
        """Test finding aircraft by tail number."""
        repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="AC003",
            tail_number="N11111",
            icao24="A11111",
            model="Boeing 777-300ER",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        
        repo.create(aircraft)
        found = repo.find_by_tail_number("N11111")
        
        assert found is not None
        assert found.aircraft_id == "AC003"
    
    def test_find_all(self, session):
        """Test finding all aircraft."""
        repo = AircraftRepository(session)
        
        for i in range(3):
            aircraft = Aircraft(
                aircraft_id=f"AC{i:03d}",
                tail_number=f"N{i:05d}",
                icao24=f"A{i:05d}",
                model="Boeing 737-800",
                operator="Test Airlines",
                manufacturer="Boeing"
            )
            repo.create(aircraft)
        
        all_aircraft = repo.find_all()
        assert len(all_aircraft) == 3
    
    def test_update_aircraft(self, session):
        """Test updating an aircraft."""
        repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="AC004",
            tail_number="N22222",
            icao24="A22222",
            model="Boeing 737-800",
            operator="Old Airlines",
            manufacturer="Boeing"
        )
        
        repo.create(aircraft)
        
        # Update the operator
        aircraft.operator = "New Airlines"
        updated = repo.update(aircraft)
        
        assert updated.operator == "New Airlines"
    
    def test_update_nonexistent(self, session):
        """Test updating non-existent aircraft raises error."""
        repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="NONEXISTENT",
            tail_number="N99999",
            icao24="A99999",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        
        with pytest.raises(NotFoundError):
            repo.update(aircraft)
    
    def test_delete_aircraft(self, session):
        """Test deleting an aircraft."""
        repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="AC005",
            tail_number="N33333",
            icao24="A33333",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        
        repo.create(aircraft)
        deleted = repo.delete("AC005")
        
        assert deleted is True
        assert repo.find_by_id("AC005") is None


class TestAirportRepository:
    """Tests for AirportRepository."""
    
    def test_create_airport(self, session):
        """Test creating an airport."""
        repo = AirportRepository(session)
        airport = Airport(
            airport_id="AP001",
            iata="LAX",
            icao="KLAX",
            name="Los Angeles International Airport",
            city="Los Angeles",
            country="USA",
            lat=33.9425,
            lon=-118.4081
        )
        
        created = repo.create(airport)
        assert created.airport_id == "AP001"
        assert created.iata == "LAX"
    
    def test_find_by_iata(self, session):
        """Test finding airport by IATA code."""
        repo = AirportRepository(session)
        airport = Airport(
            airport_id="AP002",
            iata="JFK",
            icao="KJFK",
            name="John F. Kennedy International Airport",
            city="New York",
            country="USA",
            lat=40.6413,
            lon=-73.7781
        )
        
        repo.create(airport)
        found = repo.find_by_iata("JFK")
        
        assert found is not None
        assert found.airport_id == "AP002"


class TestFlightRepository:
    """Tests for FlightRepository."""
    
    def test_create_flight(self, session):
        """Test creating a flight."""
        repo = FlightRepository(session)
        flight = Flight(
            flight_id="FL001",
            flight_number="AA100",
            aircraft_id="AC001",
            operator="American Airlines",
            origin="LAX",
            destination="JFK",
            scheduled_departure="2024-01-01T10:00:00",
            scheduled_arrival="2024-01-01T18:00:00"
        )
        
        created = repo.create(flight)
        assert created.flight_id == "FL001"
        assert created.flight_number == "AA100"
    
    def test_find_by_aircraft(self, session):
        """Test finding flights by aircraft ID."""
        repo = FlightRepository(session)
        
        for i in range(3):
            flight = Flight(
                flight_id=f"FL{i:03d}",
                flight_number=f"AA{i:03d}",
                aircraft_id="AC001",
                operator="American Airlines",
                origin="LAX",
                destination="JFK",
                scheduled_departure="2024-01-01T10:00:00",
                scheduled_arrival="2024-01-01T18:00:00"
            )
            repo.create(flight)
        
        flights = repo.find_by_aircraft("AC001")
        assert len(flights) == 3


class TestMaintenanceEventRepository:
    """Tests for MaintenanceEventRepository."""
    
    def test_create_event(self, session):
        """Test creating a maintenance event."""
        repo = MaintenanceEventRepository(session)
        event = MaintenanceEvent(
            event_id="ME001",
            aircraft_id="AC001",
            system_id="SYS001",
            component_id="COMP001",
            fault="Engine temperature high",
            severity="CRITICAL",
            reported_at="2024-01-01T12:00:00",
            corrective_action="Replaced sensor"
        )
        
        created = repo.create(event)
        assert created.event_id == "ME001"
        assert created.severity == "CRITICAL"
    
    def test_find_by_severity(self, session):
        """Test finding events by severity."""
        repo = MaintenanceEventRepository(session)
        
        for i in range(2):
            event = MaintenanceEvent(
                event_id=f"ME{i:03d}",
                aircraft_id="AC001",
                system_id="SYS001",
                component_id="COMP001",
                fault="Test fault",
                severity="CRITICAL",
                reported_at="2024-01-01T12:00:00",
                corrective_action="Test action"
            )
            repo.create(event)
        
        events = repo.find_by_severity("CRITICAL")
        assert len(events) == 2
