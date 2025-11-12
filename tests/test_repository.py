"""Tests for repository operations."""

import pytest
from neo4j_client.repository import (
    AircraftRepository,
    FlightRepository,
    AirportRepository,
    SystemRepository,
    MaintenanceEventRepository,
)
from neo4j_client.models import Aircraft, Flight, Airport, System, MaintenanceEvent
from neo4j_client.exceptions import NotFoundError, QueryError


class TestAircraftRepository:
    """Tests for AircraftRepository."""
    
    def test_create_aircraft(self, connection):
        """Test creating a new aircraft."""
        repo = AircraftRepository(connection)
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="ABC123",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        
        result = repo.create(aircraft)
        
        assert result.aircraft_id == aircraft.aircraft_id
        assert result.tail_number == aircraft.tail_number
    
    def test_find_by_id_exists(self, connection):
        """Test finding an aircraft that exists."""
        repo = AircraftRepository(connection)
        aircraft = Aircraft(
            aircraft_id="AC002",
            tail_number="N54321",
            icao24="DEF456",
            model="Airbus A320",
            operator="Test Airlines",
            manufacturer="Airbus"
        )
        repo.create(aircraft)
        
        result = repo.find_by_id("AC002")
        
        assert result is not None
        assert result.aircraft_id == "AC002"
        assert result.model == "Airbus A320"
    
    def test_find_by_id_not_exists(self, connection):
        """Test finding an aircraft that doesn't exist."""
        repo = AircraftRepository(connection)
        
        result = repo.find_by_id("NONEXISTENT")
        
        assert result is None
    
    def test_find_by_tail_number(self, connection):
        """Test finding an aircraft by tail number."""
        repo = AircraftRepository(connection)
        aircraft = Aircraft(
            aircraft_id="AC003",
            tail_number="N99999",
            icao24="GHI789",
            model="Boeing 777",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        result = repo.find_by_tail_number("N99999")
        
        assert result is not None
        assert result.aircraft_id == "AC003"
    
    def test_find_all(self, connection):
        """Test finding all aircraft."""
        repo = AircraftRepository(connection)
        
        # Create multiple aircraft
        for i in range(3):
            aircraft = Aircraft(
                aircraft_id=f"AC{i:03d}",
                tail_number=f"N{i:05d}",
                icao24=f"TEST{i:03d}",
                model=f"Test Model {i}",
                operator="Test Airlines",
                manufacturer="Test Manufacturer"
            )
            repo.create(aircraft)
        
        results = repo.find_all()
        
        assert len(results) == 3
    
    def test_find_by_operator(self, connection):
        """Test finding aircraft by operator."""
        repo = AircraftRepository(connection)
        
        # Create aircraft for different operators
        aircraft1 = Aircraft(
            aircraft_id="AC010",
            tail_number="N10000",
            icao24="OPR001",
            model="Boeing 737",
            operator="Operator A",
            manufacturer="Boeing"
        )
        aircraft2 = Aircraft(
            aircraft_id="AC011",
            tail_number="N10001",
            icao24="OPR002",
            model="Airbus A320",
            operator="Operator B",
            manufacturer="Airbus"
        )
        repo.create(aircraft1)
        repo.create(aircraft2)
        
        results = repo.find_by_operator("Operator A")
        
        assert len(results) == 1
        assert results[0].operator == "Operator A"
    
    def test_update_aircraft(self, connection):
        """Test updating an existing aircraft."""
        repo = AircraftRepository(connection)
        
        # Create aircraft
        aircraft = Aircraft(
            aircraft_id="AC020",
            tail_number="N20000",
            icao24="UPD001",
            model="Boeing 737",
            operator="Old Operator",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        # Update aircraft
        aircraft.operator = "New Operator"
        result = repo.update(aircraft)
        
        assert result.operator == "New Operator"
        
        # Verify update persisted
        found = repo.find_by_id("AC020")
        assert found.operator == "New Operator"
    
    def test_update_nonexistent_aircraft(self, connection):
        """Test updating an aircraft that doesn't exist."""
        repo = AircraftRepository(connection)
        
        aircraft = Aircraft(
            aircraft_id="NONEXISTENT",
            tail_number="N00000",
            icao24="NONE",
            model="Test",
            operator="Test",
            manufacturer="Test"
        )
        
        with pytest.raises(NotFoundError):
            repo.update(aircraft)
    
    def test_delete_aircraft(self, connection):
        """Test deleting an aircraft."""
        repo = AircraftRepository(connection)
        
        # Create aircraft
        aircraft = Aircraft(
            aircraft_id="AC030",
            tail_number="N30000",
            icao24="DEL001",
            model="Boeing 737",
            operator="Test",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        # Delete aircraft
        result = repo.delete("AC030")
        
        assert result is True
        
        # Verify deletion
        found = repo.find_by_id("AC030")
        assert found is None
    
    def test_delete_nonexistent_aircraft(self, connection):
        """Test deleting an aircraft that doesn't exist."""
        repo = AircraftRepository(connection)
        
        result = repo.delete("NONEXISTENT")
        
        assert result is False


class TestFlightRepository:
    """Tests for FlightRepository."""
    
    def test_find_flights_by_aircraft_id(self, connection):
        """Test finding flights for a specific aircraft."""
        # Create aircraft and flight in database
        with connection.session() as session:
            session.run("""
                CREATE (a:Aircraft {aircraft_id: 'AC100'})
                CREATE (f:Flight {
                    flight_id: 'FL001',
                    flight_number: 'AA100',
                    aircraft_id: 'AC100',
                    operator: 'Test Airlines',
                    origin: 'LAX',
                    destination: 'JFK',
                    scheduled_departure: '2024-01-01T10:00:00',
                    scheduled_arrival: '2024-01-01T18:00:00'
                })
                CREATE (a)-[:OPERATES_FLIGHT]->(f)
            """)
        
        repo = FlightRepository(connection)
        results = repo.find_by_aircraft_id("AC100")
        
        assert len(results) == 1
        assert results[0].flight_id == "FL001"
        assert results[0].aircraft_id == "AC100"
    
    def test_find_flight_by_id(self, connection):
        """Test finding a specific flight by ID."""
        # Create flight in database
        with connection.session() as session:
            session.run("""
                CREATE (f:Flight {
                    flight_id: 'FL002',
                    flight_number: 'AA200',
                    aircraft_id: 'AC200',
                    operator: 'Test Airlines',
                    origin: 'SFO',
                    destination: 'ORD',
                    scheduled_departure: '2024-01-02T10:00:00',
                    scheduled_arrival: '2024-01-02T16:00:00'
                })
            """)
        
        repo = FlightRepository(connection)
        result = repo.find_by_id("FL002")
        
        assert result is not None
        assert result.flight_id == "FL002"
        assert result.origin == "SFO"


class TestAirportRepository:
    """Tests for AirportRepository."""
    
    def test_find_airport_by_iata(self, connection):
        """Test finding an airport by IATA code."""
        # Create airport in database
        with connection.session() as session:
            session.run("""
                CREATE (a:Airport {
                    airport_id: 'AP001',
                    iata: 'LAX',
                    icao: 'KLAX',
                    name: 'Los Angeles International',
                    city: 'Los Angeles',
                    country: 'USA',
                    lat: 33.9425,
                    lon: -118.408
                })
            """)
        
        repo = AirportRepository(connection)
        result = repo.find_by_iata("LAX")
        
        assert result is not None
        assert result.iata == "LAX"
        assert result.name == "Los Angeles International"
    
    def test_find_all_airports(self, connection):
        """Test finding all airports."""
        # Create multiple airports
        with connection.session() as session:
            session.run("""
                CREATE (a1:Airport {
                    airport_id: 'AP010',
                    iata: 'SFO',
                    icao: 'KSFO',
                    name: 'San Francisco',
                    city: 'San Francisco',
                    country: 'USA',
                    lat: 37.6213,
                    lon: -122.3790
                })
                CREATE (a2:Airport {
                    airport_id: 'AP011',
                    iata: 'JFK',
                    icao: 'KJFK',
                    name: 'John F Kennedy',
                    city: 'New York',
                    country: 'USA',
                    lat: 40.6413,
                    lon: -73.7781
                })
            """)
        
        repo = AirportRepository(connection)
        results = repo.find_all()
        
        assert len(results) == 2


class TestSystemRepository:
    """Tests for SystemRepository."""
    
    def test_find_systems_by_aircraft_id(self, connection):
        """Test finding systems for a specific aircraft."""
        # Create aircraft and system in database
        with connection.session() as session:
            session.run("""
                CREATE (a:Aircraft {aircraft_id: 'AC300'})
                CREATE (s:System {
                    system_id: 'SYS001',
                    aircraft_id: 'AC300',
                    name: 'Hydraulics',
                    type: 'Primary'
                })
                CREATE (a)-[:HAS_SYSTEM]->(s)
            """)
        
        repo = SystemRepository(connection)
        results = repo.find_by_aircraft_id("AC300")
        
        assert len(results) == 1
        assert results[0].system_id == "SYS001"
        assert results[0].name == "Hydraulics"


class TestMaintenanceEventRepository:
    """Tests for MaintenanceEventRepository."""
    
    def test_find_maintenance_events_by_aircraft_id(self, connection):
        """Test finding maintenance events for a specific aircraft."""
        # Create aircraft and maintenance event in database
        with connection.session() as session:
            session.run("""
                CREATE (a:Aircraft {aircraft_id: 'AC400'})
                CREATE (m:MaintenanceEvent {
                    event_id: 'ME001',
                    aircraft_id: 'AC400',
                    system_id: 'SYS100',
                    component_id: 'COMP100',
                    fault: 'Test fault',
                    severity: 'WARNING',
                    reported_at: '2024-01-01T12:00:00',
                    corrective_action: 'Test action'
                })
                CREATE (m)-[:AFFECTS_AIRCRAFT]->(a)
            """)
        
        repo = MaintenanceEventRepository(connection)
        results = repo.find_by_aircraft_id("AC400")
        
        assert len(results) == 1
        assert results[0].event_id == "ME001"
        assert results[0].severity == "WARNING"
    
    def test_find_maintenance_events_by_severity(self, connection):
        """Test finding maintenance events by severity."""
        # Create maintenance events with different severities
        with connection.session() as session:
            session.run("""
                CREATE (m1:MaintenanceEvent {
                    event_id: 'ME010',
                    aircraft_id: 'AC410',
                    system_id: 'SYS110',
                    component_id: 'COMP110',
                    fault: 'Critical fault',
                    severity: 'CRITICAL',
                    reported_at: '2024-01-01T12:00:00',
                    corrective_action: 'Immediate action'
                })
                CREATE (m2:MaintenanceEvent {
                    event_id: 'ME011',
                    aircraft_id: 'AC411',
                    system_id: 'SYS111',
                    component_id: 'COMP111',
                    fault: 'Minor fault',
                    severity: 'WARNING',
                    reported_at: '2024-01-01T13:00:00',
                    corrective_action: 'Monitor'
                })
            """)
        
        repo = MaintenanceEventRepository(connection)
        results = repo.find_by_severity("CRITICAL")
        
        assert len(results) == 1
        assert results[0].severity == "CRITICAL"
