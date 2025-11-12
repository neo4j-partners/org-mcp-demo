"""
Integration tests for Neo4j aircraft client repository operations.

These tests verify the CRUD operations for each repository using a test
Neo4j database instance.
"""

import pytest
from neo4j_aircraft_client import (
    Aircraft,
    Airport,
    Flight,
    System,
    MaintenanceEvent,
    AircraftRepository,
    FlightRepository,
    AirportRepository,
    SystemRepository,
    MaintenanceEventRepository,
    NotFoundError,
    QueryError,
)


class TestAircraftRepository:
    """Tests for AircraftRepository CRUD operations."""
    
    def test_create_aircraft(self, session):
        """Test creating a new aircraft."""
        repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="TEST-001",
            tail_number="N12345",
            icao24="ABC123",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing",
        )
        
        created = repo.create(aircraft)
        assert created.aircraft_id == "TEST-001"
        assert created.tail_number == "N12345"
        assert created.model == "Boeing 737-800"
    
    def test_find_by_id(self, session):
        """Test finding an aircraft by ID."""
        repo = AircraftRepository(session)
        
        # Create test aircraft
        aircraft = Aircraft(
            aircraft_id="TEST-002",
            tail_number="N67890",
            icao24="DEF456",
            model="Airbus A320",
            operator="Test Airlines",
            manufacturer="Airbus",
        )
        repo.create(aircraft)
        
        # Find by ID
        found = repo.find_by_id("TEST-002")
        assert found is not None
        assert found.aircraft_id == "TEST-002"
        assert found.tail_number == "N67890"
        
        # Test not found
        not_found = repo.find_by_id("NONEXISTENT")
        assert not_found is None
    
    def test_find_by_tail_number(self, session):
        """Test finding an aircraft by tail number."""
        repo = AircraftRepository(session)
        
        # Create test aircraft
        aircraft = Aircraft(
            aircraft_id="TEST-003",
            tail_number="N99999",
            icao24="GHI789",
            model="Boeing 777",
            operator="Test Airlines",
            manufacturer="Boeing",
        )
        repo.create(aircraft)
        
        # Find by tail number
        found = repo.find_by_tail_number("N99999")
        assert found is not None
        assert found.aircraft_id == "TEST-003"
        assert found.model == "Boeing 777"
    
    def test_find_all(self, session):
        """Test finding all aircraft."""
        repo = AircraftRepository(session)
        
        # Create multiple aircraft
        for i in range(3):
            aircraft = Aircraft(
                aircraft_id=f"TEST-ALL-{i}",
                tail_number=f"N-ALL-{i}",
                icao24=f"ALL-{i}",
                model="Test Model",
                operator="Test Airlines",
                manufacturer="Test Manufacturer",
            )
            repo.create(aircraft)
        
        # Find all (with limit)
        all_aircraft = repo.find_all(limit=10)
        assert len(all_aircraft) >= 3
    
    def test_update_aircraft(self, session):
        """Test updating an aircraft."""
        repo = AircraftRepository(session)
        
        # Create aircraft
        aircraft = Aircraft(
            aircraft_id="TEST-UPDATE",
            tail_number="N-UPDATE",
            icao24="UPD123",
            model="Original Model",
            operator="Original Operator",
            manufacturer="Original Manufacturer",
        )
        repo.create(aircraft)
        
        # Update aircraft
        aircraft.model = "Updated Model"
        aircraft.operator = "Updated Operator"
        updated = repo.update(aircraft)
        
        assert updated.model == "Updated Model"
        assert updated.operator == "Updated Operator"
        
        # Verify update persisted
        found = repo.find_by_id("TEST-UPDATE")
        assert found.model == "Updated Model"
    
    def test_update_nonexistent_aircraft(self, session):
        """Test updating a non-existent aircraft raises NotFoundError."""
        repo = AircraftRepository(session)
        
        aircraft = Aircraft(
            aircraft_id="NONEXISTENT-UPDATE",
            tail_number="N-NONE",
            icao24="NONE",
            model="Test",
            operator="Test",
            manufacturer="Test",
        )
        
        with pytest.raises(NotFoundError):
            repo.update(aircraft)
    
    def test_delete_aircraft(self, session):
        """Test deleting an aircraft."""
        repo = AircraftRepository(session)
        
        # Create aircraft
        aircraft = Aircraft(
            aircraft_id="TEST-DELETE",
            tail_number="N-DELETE",
            icao24="DEL123",
            model="Test Model",
            operator="Test Operator",
            manufacturer="Test Manufacturer",
        )
        repo.create(aircraft)
        
        # Delete aircraft
        deleted = repo.delete("TEST-DELETE")
        assert deleted is True
        
        # Verify deletion
        found = repo.find_by_id("TEST-DELETE")
        assert found is None
        
        # Test deleting non-existent aircraft
        not_deleted = repo.delete("NONEXISTENT-DELETE")
        assert not_deleted is False


class TestFlightRepository:
    """Tests for FlightRepository CRUD operations."""
    
    def test_create_flight(self, session):
        """Test creating a new flight."""
        repo = FlightRepository(session)
        flight = Flight(
            flight_id="FL-TEST-001",
            flight_number="TA100",
            aircraft_id="AC-001",
            operator="Test Airlines",
            origin="LAX",
            destination="JFK",
            scheduled_departure="2024-01-01T10:00:00Z",
            scheduled_arrival="2024-01-01T18:00:00Z",
        )
        
        created = repo.create(flight)
        assert created.flight_id == "FL-TEST-001"
        assert created.flight_number == "TA100"
        assert created.origin == "LAX"
        assert created.destination == "JFK"
    
    def test_find_by_id(self, session):
        """Test finding a flight by ID."""
        repo = FlightRepository(session)
        
        flight = Flight(
            flight_id="FL-TEST-002",
            flight_number="TA200",
            aircraft_id="AC-002",
            operator="Test Airlines",
            origin="SFO",
            destination="ORD",
            scheduled_departure="2024-01-02T09:00:00Z",
            scheduled_arrival="2024-01-02T15:00:00Z",
        )
        repo.create(flight)
        
        found = repo.find_by_id("FL-TEST-002")
        assert found is not None
        assert found.flight_number == "TA200"
    
    def test_find_all(self, session):
        """Test finding all flights."""
        repo = FlightRepository(session)
        
        for i in range(3):
            flight = Flight(
                flight_id=f"FL-ALL-{i}",
                flight_number=f"TA{300+i}",
                aircraft_id=f"AC-{i}",
                operator="Test Airlines",
                origin="LAX",
                destination="JFK",
                scheduled_departure=f"2024-01-0{i+1}T10:00:00Z",
                scheduled_arrival=f"2024-01-0{i+1}T18:00:00Z",
            )
            repo.create(flight)
        
        all_flights = repo.find_all(limit=10)
        assert len(all_flights) >= 3
    
    def test_delete_flight(self, session):
        """Test deleting a flight."""
        repo = FlightRepository(session)
        
        flight = Flight(
            flight_id="FL-DELETE",
            flight_number="TA999",
            aircraft_id="AC-999",
            operator="Test Airlines",
            origin="LAX",
            destination="JFK",
            scheduled_departure="2024-01-01T10:00:00Z",
            scheduled_arrival="2024-01-01T18:00:00Z",
        )
        repo.create(flight)
        
        deleted = repo.delete("FL-DELETE")
        assert deleted is True
        
        found = repo.find_by_id("FL-DELETE")
        assert found is None


class TestAirportRepository:
    """Tests for AirportRepository CRUD operations."""
    
    def test_create_airport(self, session):
        """Test creating a new airport."""
        repo = AirportRepository(session)
        airport = Airport(
            airport_id="AP-TEST-001",
            iata="TST",
            icao="KTST",
            name="Test Airport",
            city="Test City",
            country="Test Country",
            lat=34.05,
            lon=-118.25,
        )
        
        created = repo.create(airport)
        assert created.airport_id == "AP-TEST-001"
        assert created.iata == "TST"
        assert created.name == "Test Airport"
    
    def test_find_by_id(self, session):
        """Test finding an airport by ID."""
        repo = AirportRepository(session)
        
        airport = Airport(
            airport_id="AP-TEST-002",
            iata="TS2",
            icao="KTS2",
            name="Test Airport 2",
            city="Test City 2",
            country="Test Country 2",
            lat=40.64,
            lon=-73.78,
        )
        repo.create(airport)
        
        found = repo.find_by_id("AP-TEST-002")
        assert found is not None
        assert found.iata == "TS2"
    
    def test_find_by_iata(self, session):
        """Test finding an airport by IATA code."""
        repo = AirportRepository(session)
        
        airport = Airport(
            airport_id="AP-TEST-003",
            iata="TS3",
            icao="KTS3",
            name="Test Airport 3",
            city="Test City 3",
            country="Test Country 3",
            lat=37.77,
            lon=-122.42,
        )
        repo.create(airport)
        
        found = repo.find_by_iata("TS3")
        assert found is not None
        assert found.airport_id == "AP-TEST-003"
    
    def test_find_all(self, session):
        """Test finding all airports."""
        repo = AirportRepository(session)
        
        for i in range(3):
            airport = Airport(
                airport_id=f"AP-ALL-{i}",
                iata=f"TA{i}",
                icao=f"KTA{i}",
                name=f"Test Airport {i}",
                city=f"Test City {i}",
                country="Test Country",
                lat=float(30 + i),
                lon=float(-120 + i),
            )
            repo.create(airport)
        
        all_airports = repo.find_all(limit=10)
        assert len(all_airports) >= 3


class TestSystemRepository:
    """Tests for SystemRepository CRUD operations."""
    
    def test_create_system(self, session):
        """Test creating a new system."""
        repo = SystemRepository(session)
        system = System(
            system_id="SYS-TEST-001",
            aircraft_id="AC-TEST-001",
            name="Hydraulic System",
            type="Hydraulics",
        )
        
        created = repo.create(system)
        assert created.system_id == "SYS-TEST-001"
        assert created.name == "Hydraulic System"
        assert created.type == "Hydraulics"
    
    def test_find_by_id(self, session):
        """Test finding a system by ID."""
        repo = SystemRepository(session)
        
        system = System(
            system_id="SYS-TEST-002",
            aircraft_id="AC-TEST-002",
            name="Avionics System",
            type="Avionics",
        )
        repo.create(system)
        
        found = repo.find_by_id("SYS-TEST-002")
        assert found is not None
        assert found.name == "Avionics System"


class TestMaintenanceEventRepository:
    """Tests for MaintenanceEventRepository CRUD operations."""
    
    def test_create_maintenance_event(self, session):
        """Test creating a new maintenance event."""
        repo = MaintenanceEventRepository(session)
        event = MaintenanceEvent(
            event_id="ME-TEST-001",
            aircraft_id="AC-TEST-001",
            system_id="SYS-TEST-001",
            component_id="COMP-TEST-001",
            fault="Test fault description",
            severity="WARNING",
            reported_at="2024-01-01T12:00:00Z",
            corrective_action="Test corrective action",
        )
        
        created = repo.create(event)
        assert created.event_id == "ME-TEST-001"
        assert created.fault == "Test fault description"
        assert created.severity == "WARNING"
    
    def test_find_by_id(self, session):
        """Test finding a maintenance event by ID."""
        repo = MaintenanceEventRepository(session)
        
        event = MaintenanceEvent(
            event_id="ME-TEST-002",
            aircraft_id="AC-TEST-002",
            system_id="SYS-TEST-002",
            component_id="COMP-TEST-002",
            fault="Critical fault",
            severity="CRITICAL",
            reported_at="2024-01-02T14:00:00Z",
            corrective_action="Emergency repair",
        )
        repo.create(event)
        
        found = repo.find_by_id("ME-TEST-002")
        assert found is not None
        assert found.severity == "CRITICAL"
    
    def test_find_by_severity(self, session):
        """Test finding maintenance events by severity."""
        repo = MaintenanceEventRepository(session)
        
        # Create events with different severities
        for i, severity in enumerate(["CRITICAL", "CRITICAL", "WARNING"]):
            event = MaintenanceEvent(
                event_id=f"ME-SEV-{i}",
                aircraft_id=f"AC-SEV-{i}",
                system_id=f"SYS-SEV-{i}",
                component_id=f"COMP-SEV-{i}",
                fault=f"Fault {i}",
                severity=severity,
                reported_at=f"2024-01-0{i+1}T12:00:00Z",
                corrective_action=f"Action {i}",
            )
            repo.create(event)
        
        # Find critical events
        critical = repo.find_by_severity("CRITICAL", limit=10)
        assert len(critical) >= 2
        for event in critical:
            assert event.severity == "CRITICAL"
