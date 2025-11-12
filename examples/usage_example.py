"""Example usage of the Neo4j Aircraft Data Python Client.

This script demonstrates how to use the client library to query aircraft data
from a Neo4j database. It includes examples of:
- Connecting to Neo4j
- Querying aircraft
- Finding flights for an aircraft
- Retrieving maintenance events
- Working with airports and systems
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    FlightRepository,
    AirportRepository,
    SystemRepository,
    MaintenanceEventRepository,
)


def main():
    """Run example queries against the Neo4j database."""
    
    # Get connection details from environment variables
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print("=" * 80)
    print("Neo4j Aircraft Data Client - Example Usage")
    print("=" * 80)
    print(f"\nConnecting to Neo4j at {uri}...\n")
    
    try:
        # Create connection using context manager (auto cleanup)
        with Neo4jConnection(uri, username, password, database) as conn:
            print("✅ Connected successfully!\n")
            
            # Example 1: List all aircraft
            print("-" * 80)
            print("Example 1: List Aircraft")
            print("-" * 80)
            aircraft_repo = AircraftRepository(conn)
            aircraft_list = aircraft_repo.find_all(limit=5)
            print(f"Found {len(aircraft_list)} aircraft:\n")
            for ac in aircraft_list:
                print(f"  {ac.tail_number}")
                print(f"    Model: {ac.model}")
                print(f"    Operator: {ac.operator}")
                print(f"    Manufacturer: {ac.manufacturer}")
                print()
            
            if not aircraft_list:
                print("No aircraft found in database. Exiting.\n")
                return
            
            # Example 2: Find aircraft by operator
            print("-" * 80)
            print("Example 2: Find Aircraft by Operator")
            print("-" * 80)
            first_operator = aircraft_list[0].operator
            operator_aircraft = aircraft_repo.find_by_operator(first_operator, limit=3)
            print(f"Aircraft operated by {first_operator}:\n")
            for ac in operator_aircraft:
                print(f"  - {ac.tail_number} ({ac.model})")
            print()
            
            # Example 3: Get flights for specific aircraft
            print("-" * 80)
            print("Example 3: Flights for Specific Aircraft")
            print("-" * 80)
            first_aircraft = aircraft_list[0]
            flight_repo = FlightRepository(conn)
            flights = flight_repo.find_by_aircraft_id(first_aircraft.aircraft_id, limit=5)
            print(f"Recent flights for {first_aircraft.tail_number}:\n")
            for flight in flights:
                print(f"  {flight.flight_number}")
                print(f"    Route: {flight.origin} → {flight.destination}")
                print(f"    Departure: {flight.scheduled_departure}")
                print(f"    Arrival: {flight.scheduled_arrival}")
                print()
            
            # Example 4: Get aircraft systems
            print("-" * 80)
            print("Example 4: Aircraft Systems")
            print("-" * 80)
            system_repo = SystemRepository(conn)
            systems = system_repo.find_by_aircraft_id(first_aircraft.aircraft_id)
            print(f"Systems for {first_aircraft.tail_number}:\n")
            for system in systems:
                print(f"  - {system.name} ({system.type})")
            print()
            
            # Example 5: Get maintenance events
            print("-" * 80)
            print("Example 5: Maintenance Events")
            print("-" * 80)
            maint_repo = MaintenanceEventRepository(conn)
            events = maint_repo.find_by_aircraft_id(first_aircraft.aircraft_id, limit=5)
            print(f"Recent maintenance events for {first_aircraft.tail_number}:\n")
            for event in events:
                print(f"  [{event.severity}] {event.reported_at}")
                print(f"    Fault: {event.fault}")
                print(f"    Action: {event.corrective_action}")
                print()
            
            # Example 6: Find critical maintenance events
            print("-" * 80)
            print("Example 6: Critical Maintenance Events")
            print("-" * 80)
            critical_events = maint_repo.find_by_severity("CRITICAL", limit=5)
            print(f"Critical maintenance events across all aircraft:\n")
            for event in critical_events:
                aircraft = aircraft_repo.find_by_id(event.aircraft_id)
                tail = aircraft.tail_number if aircraft else "Unknown"
                print(f"  Aircraft: {tail}")
                print(f"    Reported: {event.reported_at}")
                print(f"    Fault: {event.fault[:60]}...")
                print()
            
            # Example 7: Airport information
            print("-" * 80)
            print("Example 7: Airport Information")
            print("-" * 80)
            airport_repo = AirportRepository(conn)
            airports = airport_repo.find_all(limit=5)
            print(f"Sample airports in the network:\n")
            for airport in airports:
                print(f"  {airport.iata} - {airport.name}")
                print(f"    Location: {airport.city}, {airport.country}")
                print(f"    Coordinates: {airport.lat}, {airport.lon}")
                print()
            
            print("=" * 80)
            print("✅ All examples completed successfully!")
            print("=" * 80)
            
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
