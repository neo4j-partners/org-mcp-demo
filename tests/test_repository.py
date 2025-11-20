"""
Integration tests for Neo4j aviation client repositories.

These tests verify that the repository classes work correctly with
the actual Neo4j database schema.
"""

import pytest
from neo4j_client import (
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    ComponentRepository,
    MaintenanceEventRepository,
    SystemRepository,
)


class TestAircraftRepository:
    """Tests for AircraftRepository."""
    
    def test_find_all_aircraft(self, connection):
        """Test retrieving all aircraft."""
        repo = AircraftRepository(connection)
        aircraft = repo.find_all(limit=10)
        
        assert isinstance(aircraft, list)
        assert len(aircraft) > 0
        assert all(hasattr(a, 'aircraft_id') for a in aircraft)
        assert all(hasattr(a, 'tail_number') for a in aircraft)
        assert all(hasattr(a, 'model') for a in aircraft)
    
    def test_find_aircraft_by_id(self, connection):
        """Test finding aircraft by ID."""
        repo = AircraftRepository(connection)
        
        # First get an aircraft to test with
        all_aircraft = repo.find_all(limit=1)
        if len(all_aircraft) == 0:
            pytest.skip("No aircraft in database")
        
        test_aircraft = all_aircraft[0]
        found = repo.find_by_id(test_aircraft.aircraft_id)
        
        assert found is not None
        assert found.aircraft_id == test_aircraft.aircraft_id
        assert found.tail_number == test_aircraft.tail_number
    
    def test_find_aircraft_by_nonexistent_id(self, connection):
        """Test finding aircraft with nonexistent ID returns None."""
        repo = AircraftRepository(connection)
        found = repo.find_by_id("NONEXISTENT_ID_12345")
        
        assert found is None
    
    def test_get_aircraft_systems(self, connection):
        """Test retrieving systems for an aircraft."""
        repo = AircraftRepository(connection)
        
        # Get first aircraft
        all_aircraft = repo.find_all(limit=1)
        if len(all_aircraft) == 0:
            pytest.skip("No aircraft in database")
        
        test_aircraft = all_aircraft[0]
        systems = repo.get_systems(test_aircraft.aircraft_id)
        
        assert isinstance(systems, list)
        # Systems should exist for aircraft
        if len(systems) > 0:
            assert all(hasattr(s, 'system_id') for s in systems)
            assert all(hasattr(s, 'name') for s in systems)
    
    def test_get_aircraft_components(self, connection):
        """Test retrieving components for an aircraft."""
        repo = AircraftRepository(connection)
        
        # Get first aircraft
        all_aircraft = repo.find_all(limit=1)
        if len(all_aircraft) == 0:
            pytest.skip("No aircraft in database")
        
        test_aircraft = all_aircraft[0]
        components = repo.get_components(test_aircraft.aircraft_id)
        
        assert isinstance(components, list)
        # Components should exist for aircraft
        if len(components) > 0:
            assert all(hasattr(c, 'component_id') for c in components)
            assert all(hasattr(c, 'name') for c in components)


class TestAirportRepository:
    """Tests for AirportRepository."""
    
    def test_find_all_airports(self, connection):
        """Test retrieving all airports."""
        repo = AirportRepository(connection)
        airports = repo.find_all(limit=10)
        
        assert isinstance(airports, list)
        assert len(airports) > 0
        assert all(hasattr(a, 'airport_id') for a in airports)
        assert all(hasattr(a, 'iata') for a in airports)
        assert all(hasattr(a, 'name') for a in airports)
    
    def test_find_airport_by_iata(self, connection):
        """Test finding airport by IATA code."""
        repo = AirportRepository(connection)
        
        # Get first airport
        all_airports = repo.find_all(limit=1)
        if len(all_airports) == 0:
            pytest.skip("No airports in database")
        
        test_airport = all_airports[0]
        found = repo.find_by_iata(test_airport.iata)
        
        assert found is not None
        assert found.iata == test_airport.iata
        assert found.airport_id == test_airport.airport_id
    
    def test_find_airport_by_icao(self, connection):
        """Test finding airport by ICAO code."""
        repo = AirportRepository(connection)
        
        # Get first airport
        all_airports = repo.find_all(limit=1)
        if len(all_airports) == 0:
            pytest.skip("No airports in database")
        
        test_airport = all_airports[0]
        found = repo.find_by_icao(test_airport.icao)
        
        assert found is not None
        assert found.icao == test_airport.icao
        assert found.airport_id == test_airport.airport_id


class TestFlightRepository:
    """Tests for FlightRepository."""
    
    def test_find_all_flights(self, connection):
        """Test retrieving all flights."""
        repo = FlightRepository(connection)
        flights = repo.find_all(limit=10)
        
        assert isinstance(flights, list)
        assert len(flights) > 0
        assert all(hasattr(f, 'flight_id') for f in flights)
        assert all(hasattr(f, 'flight_number') for f in flights)
        assert all(hasattr(f, 'origin') for f in flights)
        assert all(hasattr(f, 'destination') for f in flights)
    
    def test_find_flight_by_id(self, connection):
        """Test finding flight by ID."""
        repo = FlightRepository(connection)
        
        # Get first flight
        all_flights = repo.find_all(limit=1)
        if len(all_flights) == 0:
            pytest.skip("No flights in database")
        
        test_flight = all_flights[0]
        found = repo.find_by_id(test_flight.flight_id)
        
        assert found is not None
        assert found.flight_id == test_flight.flight_id
        assert found.flight_number == test_flight.flight_number
    
    def test_find_flights_by_aircraft(self, connection):
        """Test finding flights by aircraft."""
        repo = FlightRepository(connection)
        
        # Get first flight to get an aircraft_id
        all_flights = repo.find_all(limit=1)
        if len(all_flights) == 0:
            pytest.skip("No flights in database")
        
        test_flight = all_flights[0]
        flights = repo.find_by_aircraft(test_flight.aircraft_id, limit=10)
        
        assert isinstance(flights, list)
        assert len(flights) > 0
        # All flights should be for the same aircraft
        assert all(f.aircraft_id == test_flight.aircraft_id for f in flights)
    
    def test_find_latest_destinations(self, connection):
        """Test finding latest destinations."""
        repo = FlightRepository(connection)
        destinations = repo.find_latest_destinations(limit=10)
        
        assert isinstance(destinations, list)
        assert len(destinations) > 0
        
        # Each result should have flight and destination
        for dest in destinations:
            assert 'flight' in dest
            assert 'destination' in dest
            assert hasattr(dest['flight'], 'destination')
            assert hasattr(dest['destination'], 'iata')


class TestComponentRepository:
    """Tests for ComponentRepository."""
    
    def test_find_all_components(self, connection):
        """Test retrieving all components."""
        repo = ComponentRepository(connection)
        components = repo.find_all(limit=10)
        
        assert isinstance(components, list)
        assert len(components) > 0
        assert all(hasattr(c, 'component_id') for c in components)
        assert all(hasattr(c, 'name') for c in components)
    
    def test_find_component_by_id(self, connection):
        """Test finding component by ID."""
        repo = ComponentRepository(connection)
        
        # Get first component
        all_components = repo.find_all(limit=1)
        if len(all_components) == 0:
            pytest.skip("No components in database")
        
        test_component = all_components[0]
        found = repo.find_by_id(test_component.component_id)
        
        assert found is not None
        assert found.component_id == test_component.component_id
        assert found.name == test_component.name
    
    def test_find_components_by_system(self, connection):
        """Test finding components by system."""
        repo = ComponentRepository(connection)
        
        # Get first component to get a system_id
        all_components = repo.find_all(limit=1)
        if len(all_components) == 0:
            pytest.skip("No components in database")
        
        test_component = all_components[0]
        components = repo.find_by_system(test_component.system_id)
        
        assert isinstance(components, list)
        assert len(components) > 0
        # All components should be for the same system
        assert all(c.system_id == test_component.system_id for c in components)


class TestMaintenanceEventRepository:
    """Tests for MaintenanceEventRepository."""
    
    def test_find_all_maintenance_events(self, connection):
        """Test retrieving all maintenance events."""
        repo = MaintenanceEventRepository(connection)
        events = repo.find_all(limit=10)
        
        assert isinstance(events, list)
        assert len(events) > 0
        assert all(hasattr(e, 'event_id') for e in events)
        assert all(hasattr(e, 'severity') for e in events)
        assert all(hasattr(e, 'fault') for e in events)
    
    def test_find_maintenance_events_by_aircraft(self, connection):
        """Test finding maintenance events by aircraft."""
        repo = MaintenanceEventRepository(connection)
        
        # Get first event to get an aircraft_id
        all_events = repo.find_all(limit=1)
        if len(all_events) == 0:
            pytest.skip("No maintenance events in database")
        
        test_event = all_events[0]
        events = repo.find_by_aircraft(test_event.aircraft_id, limit=10)
        
        assert isinstance(events, list)
        assert len(events) > 0
        # All events should be for the same aircraft
        assert all(e.aircraft_id == test_event.aircraft_id for e in events)
    
    def test_find_maintenance_events_by_severity(self, connection):
        """Test finding maintenance events by severity."""
        repo = MaintenanceEventRepository(connection)
        events = repo.find_by_severity("CRITICAL", limit=10)
        
        assert isinstance(events, list)
        # If there are critical events, verify they have the right severity
        if len(events) > 0:
            assert all(e.severity == "CRITICAL" for e in events)
    
    def test_find_missing_components(self, connection):
        """Test finding missing/faulty components."""
        repo = MaintenanceEventRepository(connection)
        missing = repo.find_missing_components(limit=10)
        
        assert isinstance(missing, list)
        # Each result should have component and maintenance_event
        if len(missing) > 0:
            for item in missing:
                assert 'component' in item
                assert 'maintenance_event' in item
                assert item['maintenance_event'].severity == "CRITICAL"


class TestSystemRepository:
    """Tests for SystemRepository."""
    
    def test_find_all_systems(self, connection):
        """Test retrieving all systems."""
        repo = SystemRepository(connection)
        systems = repo.find_all(limit=10)
        
        assert isinstance(systems, list)
        assert len(systems) > 0
        assert all(hasattr(s, 'system_id') for s in systems)
        assert all(hasattr(s, 'name') for s in systems)
    
    def test_find_system_by_id(self, connection):
        """Test finding system by ID."""
        repo = SystemRepository(connection)
        
        # Get first system
        all_systems = repo.find_all(limit=1)
        if len(all_systems) == 0:
            pytest.skip("No systems in database")
        
        test_system = all_systems[0]
        found = repo.find_by_id(test_system.system_id)
        
        assert found is not None
        assert found.system_id == test_system.system_id
        assert found.name == test_system.name
