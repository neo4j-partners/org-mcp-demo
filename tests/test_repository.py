"""Tests for Neo4j aircraft repository operations."""

import pytest
from neo4j_client import (
    Aircraft,
    Flight,
    MaintenanceEvent,
    System,
    Airport,
    AircraftRepository,
    FlightRepository,
    MaintenanceEventRepository,
    SystemRepository,
    AirportRepository,
    NotFoundError,
)


class TestAircraftRepository:
    """Tests for AircraftRepository."""
    
    def test_create_aircraft(self, session):
        """Test creating a new aircraft."""
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
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        found = repo.find_by_id("AC001")
        assert found is not None
        assert found.aircraft_id == "AC001"
        assert found.tail_number == "N12345"
    
    def test_find_by_id_not_found(self, session):
        """Test finding non-existent aircraft."""
        repo = AircraftRepository(session)
        found = repo.find_by_id("NONEXISTENT")
        assert found is None
    
    def test_find_by_tail_number(self, session):
        """Test finding aircraft by tail number."""
        repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        found = repo.find_by_tail_number("N12345")
        assert found is not None
        assert found.aircraft_id == "AC001"
    
    def test_find_by_operator(self, session):
        """Test finding aircraft by operator."""
        repo = AircraftRepository(session)
        
        aircraft1 = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        aircraft2 = Aircraft(
            aircraft_id="AC002",
            tail_number="N54321",
            icao24="A54321",
            model="Airbus A320",
            operator="Test Airlines",
            manufacturer="Airbus"
        )
        
        repo.create(aircraft1)
        repo.create(aircraft2)
        
        found = repo.find_by_operator("Test Airlines")
        assert len(found) == 2
    
    def test_find_all(self, session):
        """Test finding all aircraft."""
        repo = AircraftRepository(session)
        
        aircraft1 = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        aircraft2 = Aircraft(
            aircraft_id="AC002",
            tail_number="N54321",
            icao24="A54321",
            model="Airbus A320",
            operator="Other Airlines",
            manufacturer="Airbus"
        )
        
        repo.create(aircraft1)
        repo.create(aircraft2)
        
        all_aircraft = repo.find_all()
        assert len(all_aircraft) == 2
    
    def test_update_aircraft(self, session):
        """Test updating an aircraft."""
        repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        aircraft.operator = "Updated Airlines"
        updated = repo.update(aircraft)
        assert updated.operator == "Updated Airlines"
        
        found = repo.find_by_id("AC001")
        assert found.operator == "Updated Airlines"
    
    def test_update_nonexistent_aircraft(self, session):
        """Test updating non-existent aircraft raises error."""
        repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="NONEXISTENT",
            tail_number="N12345",
            icao24="A12345",
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
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        repo.create(aircraft)
        
        deleted = repo.delete("AC001")
        assert deleted is True
        
        found = repo.find_by_id("AC001")
        assert found is None
    
    def test_delete_nonexistent_aircraft(self, session):
        """Test deleting non-existent aircraft."""
        repo = AircraftRepository(session)
        deleted = repo.delete("NONEXISTENT")
        assert deleted is False


class TestFlightRepository:
    """Tests for FlightRepository."""
    
    def test_find_by_aircraft(self, session):
        """Test finding flights by aircraft."""
        # Create aircraft
        aircraft_repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        aircraft_repo.create(aircraft)
        
        # Create flight and relationship
        session.run("""
            MATCH (a:Aircraft {aircraft_id: $aircraft_id})
            CREATE (f:Flight {
                flight_id: $flight_id,
                flight_number: $flight_number,
                aircraft_id: $aircraft_id,
                operator: $operator,
                origin: $origin,
                destination: $destination,
                scheduled_departure: $scheduled_departure,
                scheduled_arrival: $scheduled_arrival
            })
            CREATE (a)-[:OPERATES_FLIGHT]->(f)
        """, {
            "aircraft_id": "AC001",
            "flight_id": "FL001",
            "flight_number": "TA100",
            "operator": "Test Airlines",
            "origin": "LAX",
            "destination": "JFK",
            "scheduled_departure": "2024-01-01T08:00:00Z",
            "scheduled_arrival": "2024-01-01T16:00:00Z"
        })
        
        flight_repo = FlightRepository(session)
        flights = flight_repo.find_by_aircraft("AC001")
        assert len(flights) == 1
        assert flights[0].flight_id == "FL001"
    
    def test_find_by_flight_number(self, session):
        """Test finding flights by flight number."""
        session.run("""
            CREATE (f:Flight {
                flight_id: $flight_id,
                flight_number: $flight_number,
                aircraft_id: $aircraft_id,
                operator: $operator,
                origin: $origin,
                destination: $destination,
                scheduled_departure: $scheduled_departure,
                scheduled_arrival: $scheduled_arrival
            })
        """, {
            "flight_id": "FL001",
            "flight_number": "TA100",
            "aircraft_id": "AC001",
            "operator": "Test Airlines",
            "origin": "LAX",
            "destination": "JFK",
            "scheduled_departure": "2024-01-01T08:00:00Z",
            "scheduled_arrival": "2024-01-01T16:00:00Z"
        })
        
        flight_repo = FlightRepository(session)
        flights = flight_repo.find_by_flight_number("TA100")
        assert len(flights) == 1
        assert flights[0].flight_id == "FL001"


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
            fault="Hydraulic leak detected",
            severity="CRITICAL",
            reported_at="2024-01-01T12:00:00Z",
            corrective_action="Replaced hydraulic seal"
        )
        
        created = repo.create(event)
        assert created.event_id == "ME001"
        assert created.severity == "CRITICAL"
    
    def test_find_by_aircraft(self, session):
        """Test finding maintenance events by aircraft."""
        # Create aircraft
        aircraft_repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        aircraft_repo.create(aircraft)
        
        # Create maintenance event and relationship
        event_repo = MaintenanceEventRepository(session)
        event = MaintenanceEvent(
            event_id="ME001",
            aircraft_id="AC001",
            system_id="SYS001",
            component_id="COMP001",
            fault="Hydraulic leak detected",
            severity="CRITICAL",
            reported_at="2024-01-01T12:00:00Z",
            corrective_action="Replaced hydraulic seal"
        )
        event_repo.create(event)
        
        # Create relationship
        session.run("""
            MATCH (a:Aircraft {aircraft_id: $aircraft_id})
            MATCH (m:MaintenanceEvent {event_id: $event_id})
            CREATE (m)-[:AFFECTS_AIRCRAFT]->(a)
        """, {"aircraft_id": "AC001", "event_id": "ME001"})
        
        events = event_repo.find_by_aircraft("AC001")
        assert len(events) == 1
        assert events[0].event_id == "ME001"
    
    def test_find_by_severity(self, session):
        """Test finding maintenance events by severity."""
        event_repo = MaintenanceEventRepository(session)
        
        event1 = MaintenanceEvent(
            event_id="ME001",
            aircraft_id="AC001",
            system_id="SYS001",
            component_id="COMP001",
            fault="Hydraulic leak detected",
            severity="CRITICAL",
            reported_at="2024-01-01T12:00:00Z",
            corrective_action="Replaced hydraulic seal"
        )
        event2 = MaintenanceEvent(
            event_id="ME002",
            aircraft_id="AC001",
            system_id="SYS002",
            component_id="COMP002",
            fault="Warning light",
            severity="WARNING",
            reported_at="2024-01-02T12:00:00Z",
            corrective_action="Bulb replaced"
        )
        
        event_repo.create(event1)
        event_repo.create(event2)
        
        critical_events = event_repo.find_by_severity("CRITICAL")
        assert len(critical_events) == 1
        assert critical_events[0].event_id == "ME001"


class TestAirportRepository:
    """Tests for AirportRepository."""
    
    def test_find_by_iata(self, session):
        """Test finding airport by IATA code."""
        session.run("""
            CREATE (a:Airport {
                airport_id: $airport_id,
                iata: $iata,
                icao: $icao,
                name: $name,
                city: $city,
                country: $country,
                lat: $lat,
                lon: $lon
            })
        """, {
            "airport_id": "AP001",
            "iata": "LAX",
            "icao": "KLAX",
            "name": "Los Angeles International Airport",
            "city": "Los Angeles",
            "country": "United States",
            "lat": 33.9425,
            "lon": -118.408
        })
        
        airport_repo = AirportRepository(session)
        airport = airport_repo.find_by_iata("LAX")
        assert airport is not None
        assert airport.name == "Los Angeles International Airport"
    
    def test_find_by_country(self, session):
        """Test finding airports by country."""
        session.run("""
            CREATE (a1:Airport {
                airport_id: 'AP001',
                iata: 'LAX',
                icao: 'KLAX',
                name: 'Los Angeles International Airport',
                city: 'Los Angeles',
                country: 'United States',
                lat: 33.9425,
                lon: -118.408
            })
            CREATE (a2:Airport {
                airport_id: 'AP002',
                iata: 'JFK',
                icao: 'KJFK',
                name: 'John F. Kennedy International Airport',
                city: 'New York',
                country: 'United States',
                lat: 40.6413,
                lon: -73.7781
            })
        """)
        
        airport_repo = AirportRepository(session)
        airports = airport_repo.find_by_country("United States")
        assert len(airports) == 2


class TestSystemRepository:
    """Tests for SystemRepository."""
    
    def test_find_by_aircraft(self, session):
        """Test finding systems by aircraft."""
        # Create aircraft
        aircraft_repo = AircraftRepository(session)
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        aircraft_repo.create(aircraft)
        
        # Create system and relationship
        session.run("""
            MATCH (a:Aircraft {aircraft_id: $aircraft_id})
            CREATE (s:System {
                system_id: $system_id,
                aircraft_id: $aircraft_id,
                name: $name,
                type: $type
            })
            CREATE (a)-[:HAS_SYSTEM]->(s)
        """, {
            "aircraft_id": "AC001",
            "system_id": "SYS001",
            "name": "Hydraulic System",
            "type": "Hydraulics"
        })
        
        system_repo = SystemRepository(session)
        systems = system_repo.find_by_aircraft("AC001")
        assert len(systems) == 1
        assert systems[0].name == "Hydraulic System"
