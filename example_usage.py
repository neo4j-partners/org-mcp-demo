"""Example script demonstrating the Neo4j Aircraft Client usage.

This script shows how to use the client library to query aircraft data
from a live Neo4j database.
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    FlightRepository,
    MaintenanceEventRepository,
)


def main():
    """Main example function."""
    # Get connection details from environment variables
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print(f"Connecting to Neo4j at {uri}...")
    
    # Use context manager for automatic connection cleanup
    with Neo4jConnection(uri, username, password, database) as conn:
        print("✓ Connected successfully!\n")
        
        # Create repositories
        aircraft_repo = AircraftRepository(conn)
        flight_repo = FlightRepository(conn)
        maintenance_repo = MaintenanceEventRepository(conn)
        
        # Example 1: Find all aircraft (limited to 5)
        print("=" * 60)
        print("Example 1: Finding aircraft in the fleet")
        print("=" * 60)
        aircraft_list = aircraft_repo.find_all(limit=5)
        print(f"Found {len(aircraft_list)} aircraft (showing first 5):\n")
        for aircraft in aircraft_list:
            print(f"  • {aircraft.tail_number}")
            print(f"    Model: {aircraft.model}")
            print(f"    Operator: {aircraft.operator}")
            print(f"    Manufacturer: {aircraft.manufacturer}")
            print()
        
        if not aircraft_list:
            print("No aircraft found in database.")
            return
        
        # Example 2: Get flights for the first aircraft
        print("=" * 60)
        print("Example 2: Finding flights for an aircraft")
        print("=" * 60)
        first_aircraft = aircraft_list[0]
        print(f"Aircraft: {first_aircraft.tail_number} ({first_aircraft.model})\n")
        
        flights = aircraft_repo.get_flights(first_aircraft.aircraft_id, limit=5)
        print(f"Found {len(flights)} flights (showing first 5):\n")
        for flight in flights:
            print(f"  • Flight {flight.flight_number}")
            print(f"    Route: {flight.origin} → {flight.destination}")
            print(f"    Departure: {flight.scheduled_departure}")
            print(f"    Arrival: {flight.scheduled_arrival}")
            print()
        
        # Example 3: Get maintenance events for the aircraft
        print("=" * 60)
        print("Example 3: Finding maintenance events")
        print("=" * 60)
        print(f"Aircraft: {first_aircraft.tail_number}\n")
        
        events = aircraft_repo.get_maintenance_events(first_aircraft.aircraft_id, limit=5)
        print(f"Found {len(events)} maintenance events (showing first 5):\n")
        for event in events:
            print(f"  • [{event.severity}] {event.fault}")
            print(f"    Reported: {event.reported_at}")
            print(f"    Action: {event.corrective_action}")
            print()
        
        # Example 4: Find critical maintenance events across all aircraft
        print("=" * 60)
        print("Example 4: Finding critical maintenance events")
        print("=" * 60)
        critical_events = maintenance_repo.find_by_severity("CRITICAL", limit=5)
        print(f"Found {len(critical_events)} critical events (showing first 5):\n")
        for event in critical_events:
            # Find the aircraft for this event
            affected_aircraft = aircraft_repo.find_by_id(event.aircraft_id)
            aircraft_name = affected_aircraft.tail_number if affected_aircraft else event.aircraft_id
            
            print(f"  • Aircraft: {aircraft_name}")
            print(f"    Fault: {event.fault}")
            print(f"    Reported: {event.reported_at}")
            print(f"    Action: {event.corrective_action}")
            print()
        
        # Example 5: Get systems for an aircraft
        print("=" * 60)
        print("Example 5: Finding aircraft systems")
        print("=" * 60)
        print(f"Aircraft: {first_aircraft.tail_number}\n")
        
        systems = aircraft_repo.get_systems(first_aircraft.aircraft_id)
        print(f"Found {len(systems)} systems:\n")
        for system in systems:
            print(f"  • {system.name} ({system.type})")
        print()
        
        print("=" * 60)
        print("Examples completed successfully!")
        print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
