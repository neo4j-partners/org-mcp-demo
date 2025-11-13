"""Integration tests for repository operations."""

import pytest
from neo4j_client.models import Aircraft, Airport, Flight, System, MaintenanceEvent


class TestAircraftRepository:
    """Test cases for AircraftRepository."""
    
    def test_create_aircraft(self, aircraft_repo):
        """Test creating a new aircraft."""
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        
        created = aircraft_repo.create(aircraft)
        assert created.aircraft_id == aircraft.aircraft_id
        assert created.tail_number == aircraft.tail_number
        assert created.model == aircraft.model
    
    def test_find_by_id(self, aircraft_repo):
        """Test finding aircraft by ID."""
        aircraft = Aircraft(
            aircraft_id="AC002",
            tail_number="N54321",
            icao24="A54321",
            model="Airbus A320",
            operator="Test Airways",
            manufacturer="Airbus"
        )
        aircraft_repo.create(aircraft)
        
        found = aircraft_repo.find_by_id("AC002")
        assert found is not None
        assert found.aircraft_id == "AC002"
        assert found.tail_number == "N54321"
    
    def test_find_by_id_not_found(self, aircraft_repo):
        """Test finding non-existent aircraft returns None."""
        found = aircraft_repo.find_by_id("NONEXISTENT")
        assert found is None
    
    def test_find_by_tail_number(self, aircraft_repo):
        """Test finding aircraft by tail number."""
        aircraft = Aircraft(
            aircraft_id="AC003",
            tail_number="N99999",
            icao24="A99999",
            model="Boeing 777",
            operator="Global Air",
            manufacturer="Boeing"
        )
        aircraft_repo.create(aircraft)
        
        found = aircraft_repo.find_by_tail_number("N99999")
        assert found is not None
        assert found.aircraft_id == "AC003"
    
    def test_find_all(self, aircraft_repo):
        """Test finding all aircraft."""
        aircraft1 = Aircraft(
            aircraft_id="AC004",
            tail_number="N11111",
            icao24="A11111",
            model="Boeing 737",
            operator="Air Test",
            manufacturer="Boeing"
        )
        aircraft2 = Aircraft(
            aircraft_id="AC005",
            tail_number="N22222",
            icao24="A22222",
            model="Airbus A320",
            operator="Air Test",
            manufacturer="Airbus"
        )
        aircraft_repo.create(aircraft1)
        aircraft_repo.create(aircraft2)
        
        all_aircraft = aircraft_repo.find_all()
        assert len(all_aircraft) == 2
    
    def test_find_by_operator(self, aircraft_repo):
        """Test finding aircraft by operator."""
        aircraft1 = Aircraft(
            aircraft_id="AC006",
            tail_number="N33333",
            icao24="A33333",
            model="Boeing 737",
            operator="Specific Airlines",
            manufacturer="Boeing"
        )
        aircraft2 = Aircraft(
            aircraft_id="AC007",
            tail_number="N44444",
            icao24="A44444",
            model="Airbus A320",
            operator="Other Airlines",
            manufacturer="Airbus"
        )
        aircraft_repo.create(aircraft1)
        aircraft_repo.create(aircraft2)
        
        specific_aircraft = aircraft_repo.find_by_operator("Specific Airlines")
        assert len(specific_aircraft) == 1
        assert specific_aircraft[0].aircraft_id == "AC006"
    
    def test_delete_aircraft(self, aircraft_repo):
        """Test deleting an aircraft."""
        aircraft = Aircraft(
            aircraft_id="AC008",
            tail_number="N55555",
            icao24="A55555",
            model="Boeing 787",
            operator="Delete Test",
            manufacturer="Boeing"
        )
        aircraft_repo.create(aircraft)
        
        deleted = aircraft_repo.delete("AC008")
        assert deleted is True
        
        found = aircraft_repo.find_by_id("AC008")
        assert found is None
    
    def test_delete_nonexistent(self, aircraft_repo):
        """Test deleting non-existent aircraft returns False."""
        deleted = aircraft_repo.delete("NONEXISTENT")
        assert deleted is False


class TestAirportRepository:
    """Test cases for AirportRepository."""
    
    def test_find_by_iata(self, airport_repo, session):
        """Test finding airport by IATA code."""
        # Create a test airport
        session.run("""
            CREATE (a:Airport {
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
        
        airport = airport_repo.find_by_iata("LAX")
        assert airport is not None
        assert airport.iata == "LAX"
        assert airport.name == "Los Angeles International"
    
    def test_find_by_icao(self, airport_repo, session):
        """Test finding airport by ICAO code."""
        session.run("""
            CREATE (a:Airport {
                airport_id: 'APT002',
                iata: 'JFK',
                icao: 'KJFK',
                name: 'John F. Kennedy International',
                city: 'New York',
                country: 'USA',
                lat: 40.6413,
                lon: -73.7781
            })
        """)
        
        airport = airport_repo.find_by_icao("KJFK")
        assert airport is not None
        assert airport.icao == "KJFK"
        assert airport.city == "New York"


class TestFlightRepository:
    """Test cases for FlightRepository."""
    
    def test_find_by_aircraft(self, flight_repo, session):
        """Test finding flights by aircraft."""
        # Create aircraft and flights
        session.run("""
            CREATE (a:Aircraft {aircraft_id: 'AC009'})
            CREATE (f1:Flight {
                flight_id: 'FL001',
                flight_number: 'AA100',
                aircraft_id: 'AC009',
                operator: 'American',
                origin: 'LAX',
                destination: 'JFK',
                scheduled_departure: '2024-01-01T10:00:00Z',
                scheduled_arrival: '2024-01-01T18:00:00Z'
            })
            CREATE (f2:Flight {
                flight_id: 'FL002',
                flight_number: 'AA101',
                aircraft_id: 'AC009',
                operator: 'American',
                origin: 'JFK',
                destination: 'LAX',
                scheduled_departure: '2024-01-02T10:00:00Z',
                scheduled_arrival: '2024-01-02T13:00:00Z'
            })
            CREATE (a)-[:OPERATES_FLIGHT]->(f1)
            CREATE (a)-[:OPERATES_FLIGHT]->(f2)
        """)
        
        flights = flight_repo.find_by_aircraft("AC009")
        assert len(flights) == 2
    
    def test_find_by_route(self, flight_repo, session):
        """Test finding flights by route."""
        session.run("""
            CREATE (f:Flight {
                flight_id: 'FL003',
                flight_number: 'AA200',
                aircraft_id: 'AC010',
                operator: 'American',
                origin: 'LAX',
                destination: 'ORD',
                scheduled_departure: '2024-01-01T10:00:00Z',
                scheduled_arrival: '2024-01-01T16:00:00Z'
            })
        """)
        
        flights = flight_repo.find_by_route("LAX", "ORD")
        assert len(flights) == 1
        assert flights[0].flight_number == "AA200"


class TestMaintenanceEventRepository:
    """Test cases for MaintenanceEventRepository."""
    
    def test_find_by_aircraft(self, maintenance_repo, session):
        """Test finding maintenance events by aircraft."""
        session.run("""
            CREATE (a:Aircraft {aircraft_id: 'AC011'})
            CREATE (m:MaintenanceEvent {
                event_id: 'ME001',
                aircraft_id: 'AC011',
                system_id: 'SYS001',
                component_id: 'COMP001',
                fault: 'Test fault',
                severity: 'WARNING',
                reported_at: '2024-01-01T10:00:00Z',
                corrective_action: 'Test action'
            })
            CREATE (m)-[:AFFECTS_AIRCRAFT]->(a)
        """)
        
        events = maintenance_repo.find_by_aircraft("AC011")
        assert len(events) == 1
        assert events[0].event_id == "ME001"
        assert events[0].severity == "WARNING"
    
    def test_find_critical_events(self, maintenance_repo, session):
        """Test finding critical maintenance events."""
        session.run("""
            CREATE (m:MaintenanceEvent {
                event_id: 'ME002',
                aircraft_id: 'AC012',
                system_id: 'SYS002',
                component_id: 'COMP002',
                fault: 'Critical fault',
                severity: 'CRITICAL',
                reported_at: '2024-01-01T10:00:00Z',
                corrective_action: 'Emergency repair'
            })
        """)
        
        events = maintenance_repo.find_critical_events()
        assert len(events) == 1
        assert events[0].severity == "CRITICAL"


class TestSystemRepository:
    """Test cases for SystemRepository."""
    
    def test_find_by_aircraft(self, system_repo, session):
        """Test finding systems by aircraft."""
        session.run("""
            CREATE (a:Aircraft {aircraft_id: 'AC013'})
            CREATE (s1:System {
                system_id: 'SYS001',
                aircraft_id: 'AC013',
                name: 'Hydraulics',
                type: 'Primary'
            })
            CREATE (s2:System {
                system_id: 'SYS002',
                aircraft_id: 'AC013',
                name: 'Avionics',
                type: 'Navigation'
            })
            CREATE (a)-[:HAS_SYSTEM]->(s1)
            CREATE (a)-[:HAS_SYSTEM]->(s2)
        """)
        
        systems = system_repo.find_by_aircraft("AC013")
        assert len(systems) == 2
        system_names = [s.name for s in systems]
        assert "Hydraulics" in system_names
        assert "Avionics" in system_names
