"""Integration tests for repository operations."""

import pytest
from neo4j_client import (
    Aircraft,
    Flight,
    MaintenanceEvent,
    AircraftRepository,
    FlightRepository,
    MaintenanceEventRepository,
    NotFoundError,
)


class TestAircraftRepository:
    """Test suite for AircraftRepository."""
    
    def test_create_aircraft(self, neo4j_client):
        """Test creating a new aircraft."""
        with neo4j_client.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="AC001",
                tail_number="N12345",
                icao24="ABC123",
                model="Boeing 737-800",
                operator="Test Airlines",
                manufacturer="Boeing"
            )
            
            result = repo.create(aircraft)
            assert result.aircraft_id == "AC001"
            assert result.tail_number == "N12345"
    
    def test_find_by_id(self, neo4j_client):
        """Test finding an aircraft by ID."""
        with neo4j_client.get_session() as session:
            repo = AircraftRepository(session)
            
            # Create aircraft
            aircraft = Aircraft(
                aircraft_id="AC002",
                tail_number="N54321",
                icao24="XYZ789",
                model="Airbus A320",
                operator="Test Airlines",
                manufacturer="Airbus"
            )
            repo.create(aircraft)
            
            # Find aircraft
            found = repo.find_by_id("AC002")
            assert found is not None
            assert found.aircraft_id == "AC002"
            assert found.tail_number == "N54321"
    
    def test_find_by_id_not_found(self, neo4j_client):
        """Test finding a non-existent aircraft."""
        with neo4j_client.get_session() as session:
            repo = AircraftRepository(session)
            
            found = repo.find_by_id("NONEXISTENT")
            assert found is None
    
    def test_find_all(self, neo4j_client):
        """Test finding all aircraft."""
        with neo4j_client.get_session() as session:
            repo = AircraftRepository(session)
            
            # Create multiple aircraft
            aircraft1 = Aircraft(
                aircraft_id="AC003",
                tail_number="N11111",
                icao24="AAA111",
                model="Boeing 777",
                operator="Test Airlines",
                manufacturer="Boeing"
            )
            aircraft2 = Aircraft(
                aircraft_id="AC004",
                tail_number="N22222",
                icao24="BBB222",
                model="Airbus A350",
                operator="Test Airlines",
                manufacturer="Airbus"
            )
            
            repo.create(aircraft1)
            repo.create(aircraft2)
            
            # Find all
            all_aircraft = repo.find_all()
            assert len(all_aircraft) == 2
    
    def test_update_aircraft(self, neo4j_client):
        """Test updating an existing aircraft."""
        with neo4j_client.get_session() as session:
            repo = AircraftRepository(session)
            
            # Create aircraft
            aircraft = Aircraft(
                aircraft_id="AC005",
                tail_number="N33333",
                icao24="CCC333",
                model="Boeing 787",
                operator="Old Operator",
                manufacturer="Boeing"
            )
            repo.create(aircraft)
            
            # Update aircraft
            aircraft.operator = "New Operator"
            updated = repo.update(aircraft)
            assert updated.operator == "New Operator"
            
            # Verify update
            found = repo.find_by_id("AC005")
            assert found.operator == "New Operator"
    
    def test_update_nonexistent_aircraft(self, neo4j_client):
        """Test updating a non-existent aircraft raises NotFoundError."""
        with neo4j_client.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="NONEXISTENT",
                tail_number="N99999",
                icao24="ZZZ999",
                model="Boeing 737",
                operator="Test",
                manufacturer="Boeing"
            )
            
            with pytest.raises(NotFoundError):
                repo.update(aircraft)
    
    def test_delete_aircraft(self, neo4j_client):
        """Test deleting an aircraft."""
        with neo4j_client.get_session() as session:
            repo = AircraftRepository(session)
            
            # Create aircraft
            aircraft = Aircraft(
                aircraft_id="AC006",
                tail_number="N44444",
                icao24="DDD444",
                model="Boeing 737",
                operator="Test Airlines",
                manufacturer="Boeing"
            )
            repo.create(aircraft)
            
            # Delete aircraft
            deleted = repo.delete("AC006")
            assert deleted is True
            
            # Verify deletion
            found = repo.find_by_id("AC006")
            assert found is None
    
    def test_delete_nonexistent_aircraft(self, neo4j_client):
        """Test deleting a non-existent aircraft returns False."""
        with neo4j_client.get_session() as session:
            repo = AircraftRepository(session)
            
            deleted = repo.delete("NONEXISTENT")
            assert deleted is False


class TestFlightRepository:
    """Test suite for FlightRepository."""
    
    def test_create_flight(self, neo4j_client):
        """Test creating a new flight."""
        with neo4j_client.get_session() as session:
            repo = FlightRepository(session)
            
            flight = Flight(
                flight_id="FL001",
                flight_number="TA123",
                aircraft_id="AC001",
                operator="Test Airlines",
                origin="JFK",
                destination="LAX",
                scheduled_departure="2024-01-01T10:00:00Z",
                scheduled_arrival="2024-01-01T14:00:00Z"
            )
            
            result = repo.create(flight)
            assert result.flight_id == "FL001"
            assert result.flight_number == "TA123"
    
    def test_find_by_aircraft(self, neo4j_client):
        """Test finding flights by aircraft ID."""
        with neo4j_client.get_session() as session:
            repo = FlightRepository(session)
            
            # Create flights for same aircraft
            flight1 = Flight(
                flight_id="FL002",
                flight_number="TA124",
                aircraft_id="AC001",
                operator="Test Airlines",
                origin="LAX",
                destination="SFO",
                scheduled_departure="2024-01-02T10:00:00Z",
                scheduled_arrival="2024-01-02T11:00:00Z"
            )
            flight2 = Flight(
                flight_id="FL003",
                flight_number="TA125",
                aircraft_id="AC001",
                operator="Test Airlines",
                origin="SFO",
                destination="SEA",
                scheduled_departure="2024-01-02T12:00:00Z",
                scheduled_arrival="2024-01-02T14:00:00Z"
            )
            
            repo.create(flight1)
            repo.create(flight2)
            
            # Find flights by aircraft
            flights = repo.find_by_aircraft("AC001")
            assert len(flights) == 2


class TestMaintenanceEventRepository:
    """Test suite for MaintenanceEventRepository."""
    
    def test_create_maintenance_event(self, neo4j_client):
        """Test creating a new maintenance event."""
        with neo4j_client.get_session() as session:
            repo = MaintenanceEventRepository(session)
            
            event = MaintenanceEvent(
                event_id="ME001",
                aircraft_id="AC001",
                system_id="SYS001",
                component_id="COMP001",
                fault="Engine vibration",
                severity="HIGH",
                corrective_action="Replace bearing",
                reported_at="2024-01-01T08:00:00Z"
            )
            
            result = repo.create(event)
            assert result.event_id == "ME001"
            assert result.severity == "HIGH"
    
    def test_find_by_aircraft(self, neo4j_client):
        """Test finding maintenance events by aircraft ID."""
        with neo4j_client.get_session() as session:
            repo = MaintenanceEventRepository(session)
            
            # Create events for same aircraft
            event1 = MaintenanceEvent(
                event_id="ME002",
                aircraft_id="AC001",
                system_id="SYS001",
                component_id="COMP001",
                fault="Fault 1",
                severity="LOW",
                corrective_action="Action 1",
                reported_at="2024-01-01T08:00:00Z"
            )
            event2 = MaintenanceEvent(
                event_id="ME003",
                aircraft_id="AC001",
                system_id="SYS002",
                component_id="COMP002",
                fault="Fault 2",
                severity="MEDIUM",
                corrective_action="Action 2",
                reported_at="2024-01-02T08:00:00Z"
            )
            
            repo.create(event1)
            repo.create(event2)
            
            # Find events by aircraft
            events = repo.find_by_aircraft("AC001")
            assert len(events) == 2
    
    def test_find_by_severity(self, neo4j_client):
        """Test finding maintenance events by severity."""
        with neo4j_client.get_session() as session:
            repo = MaintenanceEventRepository(session)
            
            # Create events with different severities
            event1 = MaintenanceEvent(
                event_id="ME004",
                aircraft_id="AC001",
                system_id="SYS001",
                component_id="COMP001",
                fault="Critical fault",
                severity="CRITICAL",
                corrective_action="Emergency repair",
                reported_at="2024-01-01T08:00:00Z"
            )
            event2 = MaintenanceEvent(
                event_id="ME005",
                aircraft_id="AC002",
                system_id="SYS002",
                component_id="COMP002",
                fault="Minor fault",
                severity="LOW",
                corrective_action="Routine maintenance",
                reported_at="2024-01-02T08:00:00Z"
            )
            
            repo.create(event1)
            repo.create(event2)
            
            # Find critical events
            critical_events = repo.find_by_severity("CRITICAL")
            assert len(critical_events) == 1
            assert critical_events[0].severity == "CRITICAL"
