#!/usr/bin/env python
"""
Example usage of the Neo4j Airplane Client.

This script demonstrates how to use the client to query aviation data.
Make sure you have Neo4j running and accessible before running this.

Usage:
    # Set environment variables
    export NEO4J_URI="bolt://localhost:7687"
    export NEO4J_USERNAME="neo4j"
    export NEO4J_PASSWORD="your_password"
    export NEO4J_DATABASE="neo4j"
    
    # Run the example
    python examples/basic_usage.py
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    FlightRepository,
    AirportRepository,
    MaintenanceEventRepository,
    DelayRepository,
)


def main():
    """Main example function."""
    # Get credentials from environment
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print(f"Connecting to Neo4j at {uri}...")
    
    # Create connection using context manager
    with Neo4jConnection(uri, username, password, database) as connection:
        session = connection.get_session()
        
        print("✅ Connected successfully!\n")
        
        # Example 1: Query Aircraft
        print("=== Example 1: Query Aircraft ===")
        aircraft_repo = AircraftRepository(session)
        aircraft_list = aircraft_repo.find_all(limit=5)
        
        print(f"Found {len(aircraft_list)} aircraft:")
        for aircraft in aircraft_list:
            print(f"  {aircraft.tail_number}: {aircraft.model} ({aircraft.operator})")
        
        # Example 2: Find specific aircraft by tail number
        if aircraft_list:
            print("\n=== Example 2: Find Aircraft by Tail Number ===")
            tail_number = aircraft_list[0].tail_number
            aircraft = aircraft_repo.find_by_tail_number(tail_number)
            if aircraft:
                print(f"Aircraft {tail_number}:")
                print(f"  Model: {aircraft.model}")
                print(f"  Manufacturer: {aircraft.manufacturer}")
                print(f"  Operator: {aircraft.operator}")
        
        # Example 3: Query Airports
        print("\n=== Example 3: Query Airports ===")
        airport_repo = AirportRepository(session)
        airports = airport_repo.find_all(limit=5)
        
        for airport in airports:
            print(f"  {airport.iata}: {airport.name}, {airport.city}")
        
        # Example 4: Find Flights for an Aircraft
        if aircraft_list:
            print("\n=== Example 4: Find Flights for Aircraft ===")
            flight_repo = FlightRepository(session)
            aircraft_id = aircraft_list[0].aircraft_id
            flights = flight_repo.find_by_aircraft(aircraft_id, limit=5)
            
            print(f"Flights for aircraft {aircraft_list[0].tail_number}:")
            for flight in flights:
                print(f"  {flight.flight_number}: {flight.origin} → {flight.destination}")
                print(f"    Departure: {flight.scheduled_departure}")
        
        # Example 5: Find Critical Maintenance Events
        print("\n=== Example 5: Critical Maintenance Events ===")
        event_repo = MaintenanceEventRepository(session)
        critical_events = event_repo.find_by_severity("CRITICAL", limit=5)
        
        print(f"Found {len(critical_events)} critical maintenance events:")
        for event in critical_events:
            print(f"  {event.severity}: {event.fault}")
            print(f"    Reported: {event.reported_at}")
            print(f"    Action: {event.corrective_action}")
        
        # Example 6: Find Significant Delays
        print("\n=== Example 6: Significant Flight Delays ===")
        delay_repo = DelayRepository(session)
        delays = delay_repo.find_significant_delays(min_minutes=60, limit=5)
        
        print(f"Found {len(delays)} significant delays (>60 minutes):")
        for delay in delays:
            print(f"  {delay.minutes} minutes - Cause: {delay.cause}")
        
        session.close()
        print("\n✅ All examples completed successfully!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
