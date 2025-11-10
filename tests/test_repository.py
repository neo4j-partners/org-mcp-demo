"""Tests for repository implementations."""

import pytest
from neo4j_client import (
    Aircraft,
    Flight,
    Airport,
    MaintenanceEvent,
    AircraftRepository,
    FlightRepository,
    AirportRepository,
    MaintenanceEventRepository,
    NotFoundError
)


class TestAircraftRepository:
    """Tests for AircraftRepository."""
    
    def test_create_aircraft(self, neo4j_connection):
        """Test creating a new aircraft."""
        with neo4j_connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="AC001",
                tail_number="N12345",
                manufacturer="Boeing",
                model="737-800",
                operator="United Airlines",
                icao24="ABC123"
            )
            
            created = repo.create(aircraft)
            assert created.aircraft_id == aircraft.aircraft_id
            assert created.tail_number == aircraft.tail_number
    
    def test_find_by_id(self, neo4j_connection):
        """Test finding an aircraft by ID."""
        with neo4j_connection.get_session() as session:
            repo = AircraftRepository(session)
            
            # Create an aircraft first
            aircraft = Aircraft(
                aircraft_id="AC002",
                tail_number="N54321",
                manufacturer="Airbus",
                model="A320",
                operator="Delta Airlines",
                icao24="DEF456"
            )
            repo.create(aircraft)
            
            # Find it
            found = repo.find_by_id("AC002")
            assert found is not None
            assert found.aircraft_id == "AC002"
            assert found.tail_number == "N54321"
            assert found.manufacturer == "Airbus"
    
    def test_find_by_id_not_found(self, neo4j_connection):
        """Test finding a non-existent aircraft."""
        with neo4j_connection.get_session() as session:
            repo = AircraftRepository(session)
            found = repo.find_by_id("NONEXISTENT")
            assert found is None
    
    def test_find_by_tail_number(self, neo4j_connection):
        """Test finding an aircraft by tail number."""
        with neo4j_connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="AC003",
                tail_number="N99999",
                manufacturer="Boeing",
                model="777-300",
                operator="American Airlines"
            )
            repo.create(aircraft)
            
            found = repo.find_by_tail_number("N99999")
            assert found is not None
            assert found.aircraft_id == "AC003"
    
    def test_find_all(self, neo4j_connection):
        """Test finding all aircraft."""
        with neo4j_connection.get_session() as session:
            repo = AircraftRepository(session)
            
            # Create multiple aircraft
            for i in range(3):
                aircraft = Aircraft(
                    aircraft_id=f"AC{i:03d}",
                    tail_number=f"N{i:05d}",
                    manufacturer="Boeing",
                    model="737",
                    operator="Test Airlines"
                )
                repo.create(aircraft)
            
            all_aircraft = repo.find_all()
            assert len(all_aircraft) == 3
    
    def test_find_by_operator(self, neo4j_connection):
        """Test finding aircraft by operator."""
        with neo4j_connection.get_session() as session:
            repo = AircraftRepository(session)
            
            # Create aircraft for different operators
            aircraft1 = Aircraft(
                aircraft_id="AC101",
                tail_number="N10001",
                manufacturer="Boeing",
                model="737",
                operator="Southwest Airlines"
            )
            aircraft2 = Aircraft(
                aircraft_id="AC102",
                tail_number="N10002",
                manufacturer="Boeing",
                model="737",
                operator="Southwest Airlines"
            )
            aircraft3 = Aircraft(
                aircraft_id="AC103",
                tail_number="N10003",
                manufacturer="Airbus",
                model="A320",
                operator="JetBlue"
            )
            
            repo.create(aircraft1)
            repo.create(aircraft2)
            repo.create(aircraft3)
            
            southwest_aircraft = repo.find_by_operator("Southwest Airlines")
            assert len(southwest_aircraft) == 2
            assert all(a.operator == "Southwest Airlines" for a in southwest_aircraft)
    
    def test_update_aircraft(self, neo4j_connection):
        """Test updating an aircraft."""
        with neo4j_connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="AC200",
                tail_number="N20000",
                manufacturer="Boeing",
                model="737",
                operator="OldOperator"
            )
            repo.create(aircraft)
            
            # Update the operator
            aircraft.operator = "NewOperator"
            updated = repo.update(aircraft)
            
            # Verify update
            found = repo.find_by_id("AC200")
            assert found.operator == "NewOperator"
    
    def test_update_nonexistent_aircraft(self, neo4j_connection):
        """Test updating a non-existent aircraft."""
        with neo4j_connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="NONEXISTENT",
                tail_number="N00000",
                manufacturer="Boeing",
                model="737",
                operator="Test"
            )
            
            with pytest.raises(NotFoundError):
                repo.update(aircraft)
    
    def test_delete_aircraft(self, neo4j_connection):
        """Test deleting an aircraft."""
        with neo4j_connection.get_session() as session:
            repo = AircraftRepository(session)
            
            aircraft = Aircraft(
                aircraft_id="AC300",
                tail_number="N30000",
                manufacturer="Boeing",
                model="737",
                operator="Test Airlines"
            )
            repo.create(aircraft)
            
            # Delete it
            deleted = repo.delete("AC300")
            assert deleted is True
            
            # Verify it's gone
            found = repo.find_by_id("AC300")
            assert found is None
    
    def test_delete_nonexistent_aircraft(self, neo4j_connection):
        """Test deleting a non-existent aircraft."""
        with neo4j_connection.get_session() as session:
            repo = AircraftRepository(session)
            deleted = repo.delete("NONEXISTENT")
            assert deleted is False


class TestFlightRepository:
    """Tests for FlightRepository."""
    
    def test_create_flight(self, neo4j_connection):
        """Test creating a new flight."""
        with neo4j_connection.get_session() as session:
            repo = FlightRepository(session)
            
            flight = Flight(
                flight_id="FL001",
                flight_number="UA123",
                aircraft_id="AC001",
                operator="United Airlines",
                origin="SFO",
                destination="LAX",
                scheduled_departure="2024-01-15T10:00:00Z",
                scheduled_arrival="2024-01-15T12:00:00Z"
            )
            
            created = repo.create(flight)
            assert created.flight_id == flight.flight_id
            assert created.flight_number == flight.flight_number
    
    def test_find_by_id(self, neo4j_connection):
        """Test finding a flight by ID."""
        with neo4j_connection.get_session() as session:
            repo = FlightRepository(session)
            
            flight = Flight(
                flight_id="FL002",
                flight_number="DL456",
                aircraft_id="AC002",
                operator="Delta Airlines",
                origin="JFK",
                destination="ATL",
                scheduled_departure="2024-01-15T14:00:00Z",
                scheduled_arrival="2024-01-15T16:00:00Z"
            )
            repo.create(flight)
            
            found = repo.find_by_id("FL002")
            assert found is not None
            assert found.flight_number == "DL456"
            assert found.origin == "JFK"
    
    def test_find_by_flight_number(self, neo4j_connection):
        """Test finding flights by flight number."""
        with neo4j_connection.get_session() as session:
            repo = FlightRepository(session)
            
            # Create multiple flights with same number
            for i in range(2):
                flight = Flight(
                    flight_id=f"FL10{i}",
                    flight_number="AA789",
                    aircraft_id=f"AC{i}",
                    operator="American Airlines",
                    origin="DFW",
                    destination="MIA",
                    scheduled_departure=f"2024-01-{15+i}T10:00:00Z",
                    scheduled_arrival=f"2024-01-{15+i}T12:00:00Z"
                )
                repo.create(flight)
            
            flights = repo.find_by_flight_number("AA789")
            assert len(flights) == 2
            assert all(f.flight_number == "AA789" for f in flights)
    
    def test_find_by_aircraft(self, neo4j_connection):
        """Test finding flights by aircraft."""
        with neo4j_connection.get_session() as session:
            repo = FlightRepository(session)
            
            # Create flights for specific aircraft
            for i in range(3):
                flight = Flight(
                    flight_id=f"FL20{i}",
                    flight_number=f"SW{i}",
                    aircraft_id="AC999",
                    operator="Southwest Airlines",
                    origin="LAX",
                    destination="SFO",
                    scheduled_departure=f"2024-01-15T{10+i}:00:00Z",
                    scheduled_arrival=f"2024-01-15T{12+i}:00:00Z"
                )
                repo.create(flight)
            
            flights = repo.find_by_aircraft("AC999")
            assert len(flights) == 3
            assert all(f.aircraft_id == "AC999" for f in flights)
    
    def test_delete_flight(self, neo4j_connection):
        """Test deleting a flight."""
        with neo4j_connection.get_session() as session:
            repo = FlightRepository(session)
            
            flight = Flight(
                flight_id="FL300",
                flight_number="TEST123",
                aircraft_id="AC001",
                operator="Test Airlines",
                origin="SFO",
                destination="LAX",
                scheduled_departure="2024-01-15T10:00:00Z",
                scheduled_arrival="2024-01-15T12:00:00Z"
            )
            repo.create(flight)
            
            deleted = repo.delete("FL300")
            assert deleted is True
            
            found = repo.find_by_id("FL300")
            assert found is None


class TestAirportRepository:
    """Tests for AirportRepository."""
    
    def test_create_airport(self, neo4j_connection):
        """Test creating a new airport."""
        with neo4j_connection.get_session() as session:
            repo = AirportRepository(session)
            
            airport = Airport(
                airport_id="AP001",
                name="Los Angeles International Airport",
                iata="LAX",
                icao="KLAX",
                city="Los Angeles",
                country="USA",
                lat=33.9425,
                lon=-118.4081
            )
            
            created = repo.create(airport)
            assert created.airport_id == airport.airport_id
            assert created.iata == "LAX"
    
    def test_find_by_id(self, neo4j_connection):
        """Test finding an airport by ID."""
        with neo4j_connection.get_session() as session:
            repo = AirportRepository(session)
            
            airport = Airport(
                airport_id="AP002",
                name="San Francisco International Airport",
                iata="SFO",
                icao="KSFO",
                city="San Francisco",
                country="USA",
                lat=37.6213,
                lon=-122.3790
            )
            repo.create(airport)
            
            found = repo.find_by_id("AP002")
            assert found is not None
            assert found.iata == "SFO"
            assert found.city == "San Francisco"
    
    def test_find_by_iata(self, neo4j_connection):
        """Test finding an airport by IATA code."""
        with neo4j_connection.get_session() as session:
            repo = AirportRepository(session)
            
            airport = Airport(
                airport_id="AP003",
                name="John F. Kennedy International Airport",
                iata="JFK",
                icao="KJFK",
                city="New York",
                country="USA",
                lat=40.6413,
                lon=-73.7781
            )
            repo.create(airport)
            
            found = repo.find_by_iata("JFK")
            assert found is not None
            assert found.airport_id == "AP003"
            assert found.name == "John F. Kennedy International Airport"
    
    def test_find_all(self, neo4j_connection):
        """Test finding all airports."""
        with neo4j_connection.get_session() as session:
            repo = AirportRepository(session)
            
            # Create multiple airports
            airports = [
                Airport(
                    airport_id=f"AP{i:03d}",
                    name=f"Airport {i}",
                    iata=f"A{i:02d}",
                    icao=f"KA{i:02d}",
                    city=f"City {i}",
                    country="USA",
                    lat=float(i),
                    lon=float(i)
                )
                for i in range(5)
            ]
            
            for airport in airports:
                repo.create(airport)
            
            all_airports = repo.find_all()
            assert len(all_airports) == 5
    
    def test_delete_airport(self, neo4j_connection):
        """Test deleting an airport."""
        with neo4j_connection.get_session() as session:
            repo = AirportRepository(session)
            
            airport = Airport(
                airport_id="AP100",
                name="Test Airport",
                iata="TST",
                icao="KTST",
                city="Test City",
                country="USA",
                lat=0.0,
                lon=0.0
            )
            repo.create(airport)
            
            deleted = repo.delete("AP100")
            assert deleted is True
            
            found = repo.find_by_id("AP100")
            assert found is None


class TestMaintenanceEventRepository:
    """Tests for MaintenanceEventRepository."""
    
    def test_create_maintenance_event(self, neo4j_connection):
        """Test creating a new maintenance event."""
        with neo4j_connection.get_session() as session:
            repo = MaintenanceEventRepository(session)
            
            event = MaintenanceEvent(
                event_id="ME001",
                aircraft_id="AC001",
                system_id="SYS001",
                component_id="COMP001",
                fault="Hydraulic leak detected",
                severity="HIGH",
                corrective_action="Replaced hydraulic line",
                reported_at="2024-01-15T08:30:00Z"
            )
            
            created = repo.create(event)
            assert created.event_id == event.event_id
            assert created.fault == event.fault
    
    def test_find_by_id(self, neo4j_connection):
        """Test finding a maintenance event by ID."""
        with neo4j_connection.get_session() as session:
            repo = MaintenanceEventRepository(session)
            
            event = MaintenanceEvent(
                event_id="ME002",
                aircraft_id="AC002",
                fault="Engine performance degradation",
                severity="MEDIUM",
                corrective_action="Engine inspection completed",
                reported_at="2024-01-16T10:00:00Z"
            )
            repo.create(event)
            
            found = repo.find_by_id("ME002")
            assert found is not None
            assert found.severity == "MEDIUM"
            assert found.aircraft_id == "AC002"
    
    def test_find_by_aircraft(self, neo4j_connection):
        """Test finding maintenance events by aircraft."""
        with neo4j_connection.get_session() as session:
            repo = MaintenanceEventRepository(session)
            
            # Create multiple events for same aircraft
            for i in range(3):
                event = MaintenanceEvent(
                    event_id=f"ME10{i}",
                    aircraft_id="AC999",
                    fault=f"Fault {i}",
                    severity="LOW",
                    corrective_action=f"Action {i}",
                    reported_at=f"2024-01-{15+i}T10:00:00Z"
                )
                repo.create(event)
            
            events = repo.find_by_aircraft("AC999")
            assert len(events) == 3
            assert all(e.aircraft_id == "AC999" for e in events)
