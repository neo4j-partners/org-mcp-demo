#!/usr/bin/env python3
"""
Example script demonstrating the Neo4j Python client library.

This script connects to a Neo4j database and demonstrates basic operations
using the generated client library.
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    FlightRepository,
    MaintenanceEventRepository,
)


def main():
    """Main function demonstrating client library usage."""
    # Get connection parameters from environment variables
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print("=" * 80)
    print("Neo4j Python Client Library - Example Usage")
    print("=" * 80)
    print(f"\nConnecting to: {uri}")
    print(f"Database: {database}\n")
    
    # Create connection using context manager
    try:
        with Neo4jConnection(uri, username, password, database) as connection:
            # Example 1: Query Aircraft
            print("-" * 80)
            print("Example 1: Querying Aircraft")
            print("-" * 80)
            with connection.get_session() as session:
                aircraft_repo = AircraftRepository(session)
                
                # Find all aircraft (limit to 5)
                aircraft_list = aircraft_repo.find_all(limit=5)
                print(f"\nFound {len(aircraft_list)} aircraft:")
                for aircraft in aircraft_list:
                    print(f"  • {aircraft.tail_number} - {aircraft.model} ({aircraft.manufacturer})")
                    print(f"    Operator: {aircraft.operator}")
                    print(f"    ICAO24: {aircraft.icao24}")
                
                # Find a specific aircraft if any exist
                if aircraft_list:
                    first_aircraft = aircraft_list[0]
                    print(f"\nLooking up aircraft by ID: {first_aircraft.aircraft_id}")
                    found = aircraft_repo.find_by_id(first_aircraft.aircraft_id)
                    if found:
                        print(f"  ✓ Found: {found.tail_number} - {found.model}")
            
            # Example 2: Query Flights
            print("\n" + "-" * 80)
            print("Example 2: Querying Flights")
            print("-" * 80)
            with connection.get_session() as session:
                flight_repo = FlightRepository(session)
                
                # Find all flights (limit to 5)
                flights = flight_repo.find_all(limit=5)
                print(f"\nFound {len(flights)} flights:")
                for flight in flights:
                    print(f"  • {flight.flight_number}: {flight.origin} → {flight.destination}")
                    print(f"    Departure: {flight.scheduled_departure}")
                    print(f"    Aircraft: {flight.aircraft_id}")
                
                # Find flights for a specific aircraft
                if aircraft_list:
                    aircraft_id = aircraft_list[0].aircraft_id
                    print(f"\nFinding flights for aircraft: {aircraft_id}")
                    aircraft_flights = flight_repo.find_by_aircraft(aircraft_id, limit=3)
                    print(f"  Found {len(aircraft_flights)} flights for this aircraft")
                    for flt in aircraft_flights[:3]:
                        print(f"    - {flt.flight_number}: {flt.origin} → {flt.destination}")
            
            # Example 3: Query Maintenance Events
            print("\n" + "-" * 80)
            print("Example 3: Querying Maintenance Events")
            print("-" * 80)
            with connection.get_session() as session:
                maintenance_repo = MaintenanceEventRepository(session)
                
                # Find critical maintenance events
                critical_events = maintenance_repo.find_by_severity("CRITICAL", limit=3)
                print(f"\nFound {len(critical_events)} critical maintenance events:")
                for event in critical_events:
                    print(f"  • Event {event.event_id}")
                    print(f"    Aircraft: {event.aircraft_id}")
                    print(f"    Fault: {event.fault}")
                    print(f"    Action: {event.corrective_action}")
                    print(f"    Reported: {event.reported_at}")
                
                # Find maintenance events for a specific aircraft
                if aircraft_list:
                    aircraft_id = aircraft_list[0].aircraft_id
                    print(f"\nFinding maintenance events for aircraft: {aircraft_id}")
                    aircraft_events = maintenance_repo.find_by_aircraft(aircraft_id, limit=3)
                    print(f"  Found {len(aircraft_events)} events for this aircraft")
                    for evt in aircraft_events[:3]:
                        print(f"    - {evt.severity}: {evt.fault}")
            
            print("\n" + "=" * 80)
            print("Demo completed successfully!")
            print("=" * 80)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. Neo4j is running and accessible")
        print("  2. Environment variables are set correctly:")
        print("     - NEO4J_URI (default: bolt://localhost:7687)")
        print("     - NEO4J_USERNAME (default: neo4j)")
        print("     - NEO4J_PASSWORD (required)")
        print("     - NEO4J_DATABASE (default: neo4j)")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
