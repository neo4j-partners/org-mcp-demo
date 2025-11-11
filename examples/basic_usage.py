#!/usr/bin/env python3
"""
Example script demonstrating the Neo4j Aviation Client.

This script connects to a Neo4j database and demonstrates basic operations
for querying aircraft, flights, and maintenance events.

Environment variables required:
- NEO4J_URI: Database URI (e.g., bolt://localhost:7687)
- NEO4J_USERNAME: Database username
- NEO4J_PASSWORD: Database password
- NEO4J_DATABASE: Database name (default: neo4j)
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
)


def main():
    """Demonstrate basic client usage."""
    
    # Get connection details from environment
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    if not password:
        print("Error: NEO4J_PASSWORD environment variable is required")
        return 1
    
    print("=" * 70)
    print("Neo4j Aviation Client - Example Usage")
    print("=" * 70)
    print()
    
    # Connect to database using context manager
    with Neo4jConnection(uri, username, password, database) as conn:
        session = conn.get_session()
        
        # Create repositories
        aircraft_repo = AircraftRepository(session)
        airport_repo = AirportRepository(session)
        flight_repo = FlightRepository(session)
        event_repo = MaintenanceEventRepository(session)
        
        # Example 1: List some aircraft
        print("1. Sample Aircraft in Fleet:")
        print("-" * 70)
        aircraft_list = aircraft_repo.find_all(limit=5)
        for aircraft in aircraft_list:
            print(f"  • {aircraft.tail_number} - {aircraft.manufacturer} {aircraft.model}")
            print(f"    Operator: {aircraft.operator}")
        print()
        
        # Example 2: List airports
        print("2. Sample Airports:")
        print("-" * 70)
        airports = airport_repo.find_all(limit=5)
        for airport in airports:
            print(f"  • {airport.iata}/{airport.icao} - {airport.name}")
            print(f"    Location: {airport.city}, {airport.country} ({airport.lat:.4f}, {airport.lon:.4f})")
        print()
        
        # Example 3: Find flights for the first aircraft
        if aircraft_list:
            first_aircraft = aircraft_list[0]
            print(f"3. Recent Flights for {first_aircraft.tail_number}:")
            print("-" * 70)
            flights = flight_repo.find_by_aircraft(first_aircraft.aircraft_id, limit=5)
            if flights:
                for flight in flights:
                    print(f"  • {flight.flight_number}: {flight.origin} → {flight.destination}")
                    print(f"    Departure: {flight.scheduled_departure}")
            else:
                print("  No flights found")
            print()
        
        # Example 4: Find critical maintenance events
        print("4. Critical Maintenance Events:")
        print("-" * 70)
        critical_events = event_repo.find_by_severity("CRITICAL", limit=5)
        if critical_events:
            for event in critical_events:
                print(f"  • Event {event.event_id}")
                print(f"    Fault: {event.fault}")
                print(f"    Aircraft: {event.aircraft_id}")
                print(f"    Reported: {event.reported_at}")
                print(f"    Action: {event.corrective_action}")
                print()
        else:
            print("  No critical events found")
        
        # Example 5: Get a specific aircraft by tail number
        if aircraft_list:
            tail_number = aircraft_list[0].tail_number
            print(f"5. Lookup Aircraft by Tail Number ({tail_number}):")
            print("-" * 70)
            aircraft = aircraft_repo.find_by_tail_number(tail_number)
            if aircraft:
                print(f"  Found: {aircraft.manufacturer} {aircraft.model}")
                print(f"  ICAO24: {aircraft.icao24}")
                print(f"  Operator: {aircraft.operator}")
            print()
        
        # Example 6: Get maintenance events for an aircraft
        if aircraft_list:
            aircraft_id = aircraft_list[0].aircraft_id
            print(f"6. Maintenance History for {aircraft_list[0].tail_number}:")
            print("-" * 70)
            events = event_repo.find_by_aircraft(aircraft_id, limit=5)
            if events:
                for event in events:
                    print(f"  • [{event.severity}] {event.fault}")
                    print(f"    Reported: {event.reported_at}")
            else:
                print("  No maintenance events found")
            print()
        
        session.close()
    
    print("=" * 70)
    print("Example completed successfully!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    exit(main())
