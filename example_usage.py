"""Example script demonstrating Neo4j Aircraft Client usage with the live database."""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    FlightRepository,
    MaintenanceEventRepository,
    SystemRepository,
    AirportRepository,
)


def main():
    """Demonstrate the Neo4j Aircraft Client with live data."""
    
    # Get connection parameters from environment
    # Support both NEO4J_* and COPILOT_MCP_NEO4J_* naming conventions
    uri = os.getenv("NEO4J_URI") or os.getenv("COPILOT_MCP_NEO4J_URI") or "bolt://localhost:7687"
    username = os.getenv("NEO4J_USERNAME") or os.getenv("COPILOT_MCP_NEO4J_USERNAME") or "neo4j"
    password = os.getenv("NEO4J_PASSWORD") or os.getenv("COPILOT_MCP_NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE") or os.getenv("COPILOT_MCP_NEO4J_DATABASE") or "neo4j"
    
    if not password:
        print("Error: NEO4J_PASSWORD environment variable not set")
        return
    
    # Connect to Neo4j
    print(f"Connecting to Neo4j at {uri}...")
    with Neo4jConnection(uri, username, password, database) as conn:
        session = conn.get_session()
        
        # Test 1: Query aircraft
        print("\n=== Aircraft Query ===")
        aircraft_repo = AircraftRepository(session)
        all_aircraft = aircraft_repo.find_all(limit=5)
        print(f"Found {len(all_aircraft)} aircraft (showing first 5):")
        for aircraft in all_aircraft:
            print(f"  - {aircraft.tail_number}: {aircraft.model} ({aircraft.operator})")
        
        if all_aircraft:
            # Test 2: Query flights for first aircraft
            print(f"\n=== Flights for {all_aircraft[0].tail_number} ===")
            flight_repo = FlightRepository(session)
            flights = flight_repo.find_by_aircraft(all_aircraft[0].aircraft_id, limit=3)
            print(f"Found {len(flights)} flights (showing first 3):")
            for flight in flights:
                print(f"  - {flight.flight_number}: {flight.origin} → {flight.destination}")
            
            # Test 3: Query systems for first aircraft
            print(f"\n=== Systems for {all_aircraft[0].tail_number} ===")
            system_repo = SystemRepository(session)
            systems = system_repo.find_by_aircraft(all_aircraft[0].aircraft_id)
            print(f"Found {len(systems)} systems:")
            for system in systems[:5]:
                print(f"  - {system.name} ({system.type})")
            
            # Test 4: Query maintenance events
            print(f"\n=== Maintenance Events for {all_aircraft[0].tail_number} ===")
            maint_repo = MaintenanceEventRepository(session)
            events = maint_repo.find_by_aircraft(all_aircraft[0].aircraft_id, limit=3)
            print(f"Found {len(events)} maintenance events (showing first 3):")
            for event in events:
                print(f"  - [{event.severity}] {event.fault}")
        
        # Test 5: Query airports
        print("\n=== Airports ===")
        airport_repo = AirportRepository(session)
        airports = airport_repo.find_all(limit=5)
        print(f"Found {len(airports)} airports (showing first 5):")
        for airport in airports:
            print(f"  - {airport.iata}: {airport.name} ({airport.city}, {airport.country})")
        
        # Test 6: Find delayed flights
        print("\n=== Delayed Flights (>30 min) ===")
        delayed = flight_repo.find_with_delays(min_delay_minutes=30, limit=5)
        print(f"Found {len(delayed)} delayed flights (showing first 5):")
        for item in delayed:
            flight = item["flight"]
            delay = item["delay"]
            print(f"  - {flight.flight_number}: {delay.minutes} min delay - {delay.cause}")
        
        session.close()
        print("\n✅ All queries completed successfully!")


if __name__ == "__main__":
    main()
