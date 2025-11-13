#!/usr/bin/env python
"""Example usage of the Neo4j Aircraft Client library.

This script demonstrates how to use the client to query aircraft data
from a Neo4j database.
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    FlightRepository,
    SystemRepository,
    MaintenanceEventRepository,
    AirportRepository,
)


def main():
    """Main example function."""
    # Get connection details from environment variables
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print(f"Connecting to Neo4j at {uri}...")
    
    # Use context manager for automatic connection handling
    with Neo4jConnection(uri, username, password, database) as conn:
        session = conn.get_session()
        
        # Example 1: Get all aircraft
        print("\n=== Example 1: List All Aircraft ===")
        aircraft_repo = AircraftRepository(session)
        aircraft_list = aircraft_repo.find_all(limit=5)
        print(f"Found {len(aircraft_list)} aircraft:")
        for aircraft in aircraft_list:
            print(f"  - {aircraft.tail_number}: {aircraft.manufacturer} {aircraft.model}")
        
        # Example 2: Get flights for first aircraft
        if aircraft_list:
            print(f"\n=== Example 2: Flights for {aircraft_list[0].tail_number} ===")
            flights = aircraft_repo.get_flights(aircraft_list[0].aircraft_id, limit=5)
            print(f"Found {len(flights)} flights:")
            for flight in flights:
                print(f"  - {flight.flight_number}: {flight.origin} → {flight.destination}")
                print(f"    Departure: {flight.scheduled_departure}")
        
        # Example 3: Get systems for first aircraft
        if aircraft_list:
            print(f"\n=== Example 3: Systems for {aircraft_list[0].tail_number} ===")
            systems = aircraft_repo.get_systems(aircraft_list[0].aircraft_id)
            print(f"Found {len(systems)} systems:")
            for system in systems:
                print(f"  - {system.name} ({system.type})")
        
        # Example 4: Get airports
        print("\n=== Example 4: List Airports ===")
        airport_repo = AirportRepository(session)
        airports = airport_repo.find_all(limit=5)
        print(f"Found {len(airports)} airports:")
        for airport in airports:
            print(f"  - {airport.iata}: {airport.name} ({airport.city}, {airport.country})")
        
        # Example 5: Find critical maintenance events
        print("\n=== Example 5: Critical Maintenance Events ===")
        maint_repo = MaintenanceEventRepository(session)
        critical_events = maint_repo.find_by_severity("CRITICAL", limit=5)
        print(f"Found {len(critical_events)} critical events:")
        for event in critical_events:
            print(f"  - {event.event_id}: {event.fault}")
            print(f"    Severity: {event.severity}, Reported: {event.reported_at}")
            print(f"    Action: {event.corrective_action}")
        
        # Example 6: Find delayed flights
        print("\n=== Example 6: Delayed Flights (>30 min) ===")
        flight_repo = FlightRepository(session)
        delayed_flights = flight_repo.find_with_delays(min_minutes=30, limit=5)
        print(f"Found {len(delayed_flights)} delayed flights:")
        for flight in delayed_flights:
            print(f"  - {flight.flight_number}: {flight.origin} → {flight.destination}")
        
        # Example 7: Get components for a system
        if aircraft_list:
            systems = aircraft_repo.get_systems(aircraft_list[0].aircraft_id)
            if systems:
                print(f"\n=== Example 7: Components for {systems[0].name} ===")
                system_repo = SystemRepository(session)
                components = system_repo.get_components(systems[0].system_id)
                print(f"Found {len(components)} components:")
                for component in components[:5]:  # Show first 5
                    print(f"  - {component.name} ({component.type})")
        
        session.close()
    
    print("\n✅ Examples completed successfully!")


if __name__ == "__main__":
    main()
