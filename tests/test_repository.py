"""Integration tests for Neo4j aircraft repositories."""

import pytest
from neo4j_client.models import Aircraft, Flight, System, MaintenanceEvent, Airport
from neo4j_client.repository import (
    AircraftRepository,
    FlightRepository,
    SystemRepository,
    MaintenanceEventRepository,
    AirportRepository,
)


class TestAircraftRepository:
    """Tests for AircraftRepository."""
    
    def test_create_aircraft(self, neo4j_session):
        """Test creating an aircraft."""
        repo = AircraftRepository(neo4j_session)
        
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
    
    def test_find_by_id(self, neo4j_session):
        """Test finding aircraft by ID."""
        repo = AircraftRepository(neo4j_session)
        
        # Create test aircraft
        aircraft = Aircraft(
            aircraft_id="AC002",
            tail_number="N67890",
            icao24="DEF456",
            model="Airbus A320",
            operator="Test Airlines",
            manufacturer="Airbus"
        )
        repo.create(aircraft)
        
        # Find it
        found = repo.find_by_id("AC002")
        assert found is not None
        assert found.aircraft_id == "AC002"
        assert found.model == "Airbus A320"
    
    def test_find_by_id_not_found(self, neo4j_session):
        """Test finding non-existent aircraft."""
        repo = AircraftRepository(neo4j_session)
        found = repo.find_by_id("NONEXISTENT")
        assert found is None
    
    def test_find_by_tail_number(self, neo4j_session):
        """Test finding aircraft by tail number."""
        repo = AircraftRepository(neo4j_session)
        
        aircraft = Aircraft(
            aircraft_id="AC003",
            tail_number="N11111",
            icao24="GHI789",
            model="Boeing 777",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        found = repo.find_by_tail_number("N11111")
        assert found is not None
        assert found.aircraft_id == "AC003"
    
    def test_find_all(self, neo4j_session):
        """Test finding all aircraft."""
        repo = AircraftRepository(neo4j_session)
        
        # Create multiple aircraft
        for i in range(3):
            aircraft = Aircraft(
                aircraft_id=f"AC{i:03d}",
                tail_number=f"N{i:05d}",
                icao24=f"TEST{i:03d}",
                model="Boeing 737",
                operator="Test Airlines",
                manufacturer="Boeing"
            )
            repo.create(aircraft)
        
        all_aircraft = repo.find_all(limit=10)
        assert len(all_aircraft) == 3
    
    def test_get_flights(self, neo4j_session):
        """Test getting flights for an aircraft."""
        aircraft_repo = AircraftRepository(neo4j_session)
        
        # Create aircraft
        aircraft = Aircraft(
            aircraft_id="AC004",
            tail_number="N22222",
            icao24="JKL012",
            model="Boeing 737",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        aircraft_repo.create(aircraft)
        
        # Create flight and relationship
        neo4j_session.run("""
            MERGE (f:Flight {
                flight_id: 'FL001',
                flight_number: 'TA100',
                aircraft_id: 'AC004',
                operator: 'Test Airlines',
                origin: 'LAX',
                destination: 'JFK',
                scheduled_departure: '2024-01-01T10:00:00',
                scheduled_arrival: '2024-01-01T18:00:00'
            })
            WITH f
            MATCH (a:Aircraft {aircraft_id: 'AC004'})
            MERGE (a)-[:OPERATES_FLIGHT]->(f)
        """)
        
        flights = aircraft_repo.get_flights("AC004")
        assert len(flights) == 1
        assert flights[0].flight_id == "FL001"
    
    def test_get_systems(self, neo4j_session):
        """Test getting systems for an aircraft."""
        aircraft_repo = AircraftRepository(neo4j_session)
        
        # Create aircraft
        aircraft = Aircraft(
            aircraft_id="AC005",
            tail_number="N33333",
            icao24="MNO345",
            model="Boeing 737",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        aircraft_repo.create(aircraft)
        
        # Create system and relationship
        neo4j_session.run("""
            MERGE (s:System {
                system_id: 'SYS001',
                aircraft_id: 'AC005',
                name: 'Hydraulic System',
                type: 'Hydraulics'
            })
            WITH s
            MATCH (a:Aircraft {aircraft_id: 'AC005'})
            MERGE (a)-[:HAS_SYSTEM]->(s)
        """)
        
        systems = aircraft_repo.get_systems("AC005")
        assert len(systems) == 1
        assert systems[0].system_id == "SYS001"


class TestFlightRepository:
    """Tests for FlightRepository."""
    
    def test_find_by_id(self, neo4j_session):
        """Test finding flight by ID."""
        repo = FlightRepository(neo4j_session)
        
        # Create test flight
        neo4j_session.run("""
            MERGE (f:Flight {
                flight_id: 'FL002',
                flight_number: 'TA200',
                aircraft_id: 'AC001',
                operator: 'Test Airlines',
                origin: 'SFO',
                destination: 'ORD',
                scheduled_departure: '2024-01-02T09:00:00',
                scheduled_arrival: '2024-01-02T15:00:00'
            })
        """)
        
        found = repo.find_by_id("FL002")
        assert found is not None
        assert found.flight_number == "TA200"
    
    def test_find_by_flight_number(self, neo4j_session):
        """Test finding flights by flight number."""
        repo = FlightRepository(neo4j_session)
        
        # Create multiple flights with same number
        for i in range(2):
            neo4j_session.run("""
                MERGE (f:Flight {
                    flight_id: $flight_id,
                    flight_number: 'TA300',
                    aircraft_id: $aircraft_id,
                    operator: 'Test Airlines',
                    origin: 'LAX',
                    destination: 'JFK',
                    scheduled_departure: $departure,
                    scheduled_arrival: '2024-01-03T18:00:00'
                })
            """, flight_id=f"FL{i:03d}", aircraft_id=f"AC{i:03d}", 
                 departure=f"2024-01-0{i+1}T10:00:00")
        
        flights = repo.find_by_flight_number("TA300")
        assert len(flights) == 2


class TestSystemRepository:
    """Tests for SystemRepository."""
    
    def test_find_by_id(self, neo4j_session):
        """Test finding system by ID."""
        repo = SystemRepository(neo4j_session)
        
        # Create test system
        neo4j_session.run("""
            MERGE (s:System {
                system_id: 'SYS002',
                aircraft_id: 'AC001',
                name: 'Avionics System',
                type: 'Avionics'
            })
        """)
        
        found = repo.find_by_id("SYS002")
        assert found is not None
        assert found.name == "Avionics System"
    
    def test_get_components(self, neo4j_session):
        """Test getting components for a system."""
        repo = SystemRepository(neo4j_session)
        
        # Create system and component
        neo4j_session.run("""
            MERGE (s:System {
                system_id: 'SYS003',
                aircraft_id: 'AC001',
                name: 'Engine System',
                type: 'Propulsion'
            })
            MERGE (c:Component {
                component_id: 'COMP001',
                system_id: 'SYS003',
                name: 'Fuel Pump',
                type: 'Pump'
            })
            MERGE (s)-[:HAS_COMPONENT]->(c)
        """)
        
        components = repo.get_components("SYS003")
        assert len(components) == 1
        assert components[0].component_id == "COMP001"


class TestAirportRepository:
    """Tests for AirportRepository."""
    
    def test_find_by_iata(self, neo4j_session):
        """Test finding airport by IATA code."""
        repo = AirportRepository(neo4j_session)
        
        # Create test airport
        neo4j_session.run("""
            MERGE (a:Airport {
                airport_id: 'APT001',
                iata: 'LAX',
                icao: 'KLAX',
                name: 'Los Angeles International',
                city: 'Los Angeles',
                country: 'USA',
                lat: 33.9425,
                lon: -118.408
            })
        """)
        
        found = repo.find_by_iata("LAX")
        assert found is not None
        assert found.name == "Los Angeles International"
        assert found.lat == 33.9425
    
    def test_find_all_airports(self, neo4j_session):
        """Test finding all airports."""
        repo = AirportRepository(neo4j_session)
        
        # Create multiple airports
        for i, iata in enumerate(["JFK", "ORD", "SFO"]):
            neo4j_session.run("""
                MERGE (a:Airport {
                    airport_id: $id,
                    iata: $iata,
                    icao: $icao,
                    name: $name,
                    city: 'Test City',
                    country: 'USA',
                    lat: 40.0,
                    lon: -74.0
                })
            """, id=f"APT{i:03d}", iata=iata, icao=f"K{iata}", 
                 name=f"{iata} Airport")
        
        airports = repo.find_all()
        assert len(airports) == 3


class TestMaintenanceEventRepository:
    """Tests for MaintenanceEventRepository."""
    
    def test_find_by_severity(self, neo4j_session):
        """Test finding maintenance events by severity."""
        repo = MaintenanceEventRepository(neo4j_session)
        
        # Create test events
        neo4j_session.run("""
            MERGE (m:MaintenanceEvent {
                event_id: 'EVT001',
                aircraft_id: 'AC001',
                system_id: 'SYS001',
                component_id: 'COMP001',
                fault: 'Test fault',
                severity: 'CRITICAL',
                reported_at: '2024-01-01T12:00:00',
                corrective_action: 'Replaced component'
            })
        """)
        
        events = repo.find_by_severity("CRITICAL")
        assert len(events) == 1
        assert events[0].event_id == "EVT001"
