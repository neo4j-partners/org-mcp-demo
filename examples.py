#!/usr/bin/env python3
"""
Example usage of the Neo4j Aviation Client Library.

This script demonstrates how to use the Python client to interact
with the Neo4j aviation database.
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    Aircraft,
    Airport,
    Flight,
    MaintenanceEvent,
)


def main():
    """Main example demonstrating client usage."""
    
    # Get connection details from environment
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print(f"Connecting to Neo4j at {uri}...")
    
    # Use context manager for automatic cleanup
    with Neo4jConnection(
        uri=uri,
        username=username,
        password=password,
        database=database
    ) as conn:
        session = conn.get_session()
        
        # Example 1: Query Aircraft
        print("\n=== Aircraft ===")
        aircraft_repo = AircraftRepository(session)
        aircraft_list = aircraft_repo.find_all(limit=5)
        print(f"Found {len(aircraft_list)} aircraft:")
        for aircraft in aircraft_list:
            print(f"  • {aircraft.tail_number}: {aircraft.model} ({aircraft.operator})")
        
        # Example 2: Query Airports
        print("\n=== Airports ===")
        airport_repo = AirportRepository(session)
        airports = airport_repo.find_all(limit=5)
        print(f"Found {len(airports)} airports:")
        for airport in airports:
            print(f"  • {airport.iata}: {airport.name} ({airport.city}, {airport.country})")
        
        # Example 3: Query Flights
        print("\n=== Flights ===")
        flight_repo = FlightRepository(session)
        flights = flight_repo.find_all(limit=5)
        print(f"Found {len(flights)} flights:")
        for flight in flights:
            print(f"  • {flight.flight_number}: {flight.origin} → {flight.destination}")
        
        # Example 4: Query Maintenance Events
        print("\n=== Critical Maintenance Events ===")
        event_repo = MaintenanceEventRepository(session)
        critical_events = event_repo.find_by_severity("CRITICAL", limit=5)
        print(f"Found {len(critical_events)} critical events:")
        for event in critical_events:
            print(f"  • {event.reported_at}: {event.fault} (Aircraft: {event.aircraft_id})")
        
        session.close()
        print("\n✅ Examples completed successfully!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure to set environment variables:")
        print("  NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE")
