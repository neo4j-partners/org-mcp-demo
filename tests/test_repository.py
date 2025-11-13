"""Tests for repository pattern implementations."""

import pytest
from neo4j_client.models import Aircraft, Airport, Flight, MaintenanceEvent
from neo4j_client.repository import (
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
)
from neo4j_client.exceptions import NotFoundError, QueryError


class TestAircraftRepository:
    """Tests for AircraftRepository."""
    
    def test_create_aircraft(self, session):
        """Test creating a new aircraft."""
        repo = AircraftRepository(session)
        
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="ABC123",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        
        created = repo.create(aircraft)
        
        assert created.aircraft_id == "AC001"
        assert created.tail_number == "N12345"
        assert created.model == "Boeing 737-800"
    
    def test_find_by_id(self, session):
        """Test finding aircraft by ID."""
        repo = AircraftRepository(session)
        
        aircraft = Aircraft(
            aircraft_id="AC002",
            tail_number="N67890",
            icao24="DEF456",
            model="Airbus A320",
            operator="Test Airlines",
            manufacturer="Airbus"
        )
        repo.create(aircraft)
        
        found = repo.find_by_id("AC002")
        
        assert found is not None
        assert found.aircraft_id == "AC002"
        assert found.tail_number == "N67890"
    
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
            tail_number="N99999",
            icao24="GHI789",
            model="Boeing 777",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        found = repo.find_by_tail_number("N99999")
        
        assert found is not None
        assert found.aircraft_id == "AC003"
    
    def test_find_all(self, session):
        """Test finding all aircraft."""
        repo = AircraftRepository(session)
        
        # Create multiple aircraft
        for i in range(3):
            aircraft = Aircraft(
                aircraft_id=f"AC{i:03d}",
                tail_number=f"N{i:05d}",
                icao24=f"TEST{i:02d}",
                model="Boeing 737",
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
            tail_number="N11111",
            icao24="UPD001",
            model="Boeing 737",
            operator="Old Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        aircraft.operator = "New Airlines"
        updated = repo.update(aircraft)
        
        assert updated.operator == "New Airlines"
        
        # Verify in database
        found = repo.find_by_id("AC004")
        assert found.operator == "New Airlines"
    
    def test_update_nonexistent_aircraft(self, session):
        """Test updating non-existent aircraft raises error."""
        repo = AircraftRepository(session)
        
        aircraft = Aircraft(
            aircraft_id="NONEXISTENT",
            tail_number="N00000",
            icao24="NONE",
            model="Boeing 737",
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
            tail_number="N22222",
            icao24="DEL001",
            model="Boeing 737",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        deleted = repo.delete("AC005")
        
        assert deleted is True
        assert repo.find_by_id("AC005") is None
    
    def test_delete_nonexistent_aircraft(self, session):
        """Test deleting non-existent aircraft."""
        repo = AircraftRepository(session)
        
        deleted = repo.delete("NONEXISTENT")
        
        assert deleted is False


class TestAirportRepository:
    """Tests for AirportRepository."""
    
    def test_create_airport(self, session):
        """Test creating a new airport."""
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
        assert created.name == "Los Angeles International Airport"
    
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
        assert found.name == "John F. Kennedy International Airport"
    
    def test_update_airport(self, session):
        """Test updating an airport."""
        repo = AirportRepository(session)
        
        airport = Airport(
            airport_id="AP003",
            iata="ORD",
            icao="KORD",
            name="Chicago O'Hare",
            city="Chicago",
            country="USA",
            lat=41.9742,
            lon=-87.9073
        )
        repo.create(airport)
        
        airport.name = "Chicago O'Hare International Airport"
        updated = repo.update(airport)
        
        assert updated.name == "Chicago O'Hare International Airport"


class TestFlightRepository:
    """Tests for FlightRepository."""
    
    def test_create_flight(self, session):
        """Test creating a new flight."""
        repo = FlightRepository(session)
        
        flight = Flight(
            flight_id="FL001",
            flight_number="AA100",
            aircraft_id="AC001",
            operator="American Airlines",
            origin="LAX",
            destination="JFK",
            scheduled_departure="2024-01-15T08:00:00Z",
            scheduled_arrival="2024-01-15T16:30:00Z"
        )
        
        created = repo.create(flight)
        
        assert created.flight_id == "FL001"
        assert created.flight_number == "AA100"
        assert created.origin == "LAX"
        assert created.destination == "JFK"
    
    def test_find_by_flight_number(self, session):
        """Test finding flights by flight number."""
        repo = FlightRepository(session)
        
        # Create multiple flights with same number
        for i in range(3):
            flight = Flight(
                flight_id=f"FL{i:03d}",
                flight_number="AA100",
                aircraft_id="AC001",
                operator="American Airlines",
                origin="LAX",
                destination="JFK",
                scheduled_departure=f"2024-01-{15+i:02d}T08:00:00Z",
                scheduled_arrival=f"2024-01-{15+i:02d}T16:30:00Z"
            )
            repo.create(flight)
        
        flights = repo.find_by_flight_number("AA100")
        
        assert len(flights) == 3
    
    def test_find_by_aircraft(self, session):
        """Test finding flights by aircraft with relationship."""
        # First create aircraft and flight nodes
        session.run("""
            CREATE (a:Aircraft {aircraft_id: 'AC999'})
            CREATE (f:Flight {
                flight_id: 'FL999',
                flight_number: 'TEST999',
                aircraft_id: 'AC999',
                operator: 'Test',
                origin: 'LAX',
                destination: 'JFK',
                scheduled_departure: '2024-01-15T08:00:00Z',
                scheduled_arrival: '2024-01-15T16:30:00Z'
            })
            CREATE (a)-[:OPERATES_FLIGHT]->(f)
        """)
        
        repo = FlightRepository(session)
        flights = repo.find_by_aircraft("AC999")
        
        assert len(flights) == 1
        assert flights[0].flight_id == "FL999"


class TestMaintenanceEventRepository:
    """Tests for MaintenanceEventRepository."""
    
    def test_create_maintenance_event(self, session):
        """Test creating a maintenance event."""
        repo = MaintenanceEventRepository(session)
        
        event = MaintenanceEvent(
            event_id="ME001",
            aircraft_id="AC001",
            system_id="SYS001",
            component_id="COMP001",
            fault="Hydraulic leak",
            severity="CRITICAL",
            reported_at="2024-01-15T10:30:00Z",
            corrective_action="Replaced hydraulic seal"
        )
        
        created = repo.create(event)
        
        assert created.event_id == "ME001"
        assert created.fault == "Hydraulic leak"
        assert created.severity == "CRITICAL"
    
    def test_find_by_severity(self, session):
        """Test finding events by severity."""
        repo = MaintenanceEventRepository(session)
        
        # Create events with different severities
        severities = ["CRITICAL", "WARNING", "CRITICAL"]
        for i, severity in enumerate(severities):
            event = MaintenanceEvent(
                event_id=f"ME{i:03d}",
                aircraft_id="AC001",
                system_id="SYS001",
                component_id="COMP001",
                fault=f"Fault {i}",
                severity=severity,
                reported_at=f"2024-01-{15+i:02d}T10:00:00Z",
                corrective_action="Fixed"
            )
            repo.create(event)
        
        critical_events = repo.find_by_severity("CRITICAL")
        
        assert len(critical_events) == 2
    
    def test_find_by_aircraft(self, session):
        """Test finding events by aircraft with relationship."""
        # Create aircraft and event with relationship
        session.run("""
            CREATE (a:Aircraft {aircraft_id: 'AC888'})
            CREATE (m:MaintenanceEvent {
                event_id: 'ME888',
                aircraft_id: 'AC888',
                system_id: 'SYS001',
                component_id: 'COMP001',
                fault: 'Test fault',
                severity: 'WARNING',
                reported_at: '2024-01-15T10:00:00Z',
                corrective_action: 'Fixed'
            })
            CREATE (m)-[:AFFECTS_AIRCRAFT]->(a)
        """)
        
        repo = MaintenanceEventRepository(session)
        events = repo.find_by_aircraft("AC888")
        
        assert len(events) == 1
        assert events[0].event_id == "ME888"
