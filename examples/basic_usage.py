"""Basic usage examples for the Neo4j Aviation Client Library."""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    DelayRepository,
    Aircraft,
)

# Connection configuration
# These should come from environment variables or configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def example_basic_connection():
    """Example: Basic connection and query."""
    print("Example 1: Basic Connection")
    print("-" * 40)
    
    with Neo4jConnection(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE) as conn:
        with conn.session() as session:
            # Execute a simple count query
            result = session.run("MATCH (a:Aircraft) RETURN count(a) as count")
            count = result.single()["count"]
            print(f"Total aircraft in database: {count}")
    
    print()


def example_find_aircraft():
    """Example: Find and list aircraft."""
    print("Example 2: Find Aircraft")
    print("-" * 40)
    
    with Neo4jConnection(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE) as conn:
        with conn.session() as session:
            aircraft_repo = AircraftRepository(session)
            
            # Find all aircraft (limited to 10)
            aircraft_list = aircraft_repo.find_all(limit=10)
            print(f"Found {len(aircraft_list)} aircraft:")
            
            for aircraft in aircraft_list:
                print(f"  • {aircraft.tail_number}: {aircraft.model} ({aircraft.operator})")
    
    print()


def example_create_aircraft():
    """Example: Create a new aircraft."""
    print("Example 3: Create New Aircraft")
    print("-" * 40)
    
    with Neo4jConnection(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE) as conn:
        with conn.session() as session:
            aircraft_repo = AircraftRepository(session)
            
            # Create a new aircraft
            new_aircraft = Aircraft(
                aircraft_id="TEST001",
                tail_number="N-TEST-001",
                icao24="TEST01",
                model="Boeing 787-9 Dreamliner",
                operator="Test Airlines",
                manufacturer="Boeing",
            )
            
            created = aircraft_repo.create(new_aircraft)
            print(f"Created aircraft: {created.tail_number}")
            
            # Find it back
            found = aircraft_repo.find_by_tail_number("N-TEST-001")
            if found:
                print(f"Verified: Found aircraft {found.tail_number}")
            
            # Clean up
            aircraft_repo.delete(created.aircraft_id)
            print("Cleaned up test aircraft")
    
    print()


def example_find_flights():
    """Example: Find flights for an aircraft."""
    print("Example 4: Find Flights")
    print("-" * 40)
    
    with Neo4jConnection(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE) as conn:
        with conn.session() as session:
            aircraft_repo = AircraftRepository(session)
            flight_repo = FlightRepository(session)
            
            # Get first aircraft
            aircraft_list = aircraft_repo.find_all(limit=1)
            if aircraft_list:
                aircraft = aircraft_list[0]
                print(f"Aircraft: {aircraft.tail_number} ({aircraft.model})")
                
                # Find flights
                flights = flight_repo.find_by_aircraft(aircraft.aircraft_id, limit=5)
                print(f"Found {len(flights)} flights:")
                
                for flight in flights:
                    print(f"  • {flight.flight_number}: {flight.origin} → {flight.destination}")
                    print(f"    Departure: {flight.scheduled_departure}")
    
    print()


def example_maintenance_events():
    """Example: Find critical maintenance events."""
    print("Example 5: Maintenance Events")
    print("-" * 40)
    
    with Neo4jConnection(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE) as conn:
        with conn.session() as session:
            maint_repo = MaintenanceEventRepository(session)
            
            # Find critical maintenance events
            critical_events = maint_repo.find_by_severity("CRITICAL", limit=5)
            print(f"Found {len(critical_events)} critical maintenance events:")
            
            for event in critical_events:
                print(f"  • Fault: {event.fault[:60]}...")
                print(f"    Severity: {event.severity}")
                print(f"    Reported: {event.reported_at}")
                print(f"    Action: {event.corrective_action[:60]}...")
                print()
    
    print()


def example_delays():
    """Example: Find significant flight delays."""
    print("Example 6: Flight Delays")
    print("-" * 40)
    
    with Neo4jConnection(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE) as conn:
        with conn.session() as session:
            delay_repo = DelayRepository(session)
            
            # Find delays over 60 minutes
            significant_delays = delay_repo.find_significant_delays(min_minutes=60, limit=10)
            print(f"Found {len(significant_delays)} delays over 60 minutes:")
            
            for delay in significant_delays:
                print(f"  • Cause: {delay.cause}")
                print(f"    Duration: {delay.minutes} minutes")
    
    print()


def example_airports():
    """Example: Find airports."""
    print("Example 7: Airports")
    print("-" * 40)
    
    with Neo4jConnection(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE) as conn:
        with conn.session() as session:
            airport_repo = AirportRepository(session)
            
            # Find all airports
            airports = airport_repo.find_all(limit=10)
            print(f"Found {len(airports)} airports:")
            
            for airport in airports:
                print(f"  • {airport.iata} - {airport.name}")
                print(f"    Location: {airport.city}, {airport.country}")
                print(f"    Coordinates: ({airport.lat:.4f}, {airport.lon:.4f})")
    
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Neo4j Aviation Client Library - Usage Examples")
    print("=" * 60)
    print()
    
    try:
        # Run all examples
        example_basic_connection()
        example_find_aircraft()
        example_create_aircraft()
        example_find_flights()
        example_maintenance_events()
        example_delays()
        example_airports()
        
        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("\nMake sure Neo4j is running and environment variables are set:")
        print("  - NEO4J_URI")
        print("  - NEO4J_USERNAME")
        print("  - NEO4J_PASSWORD")
        print("  - NEO4J_DATABASE (optional, defaults to 'neo4j')")
