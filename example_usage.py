#!/usr/bin/env python3
"""Example usage of the Neo4j Aviation Client Library.

This script demonstrates how to use the client to interact with a Neo4j database.
"""

import os
from neo4j_client import (
    Neo4jConnection,
    Aircraft,
    Airport,
    Flight,
    MaintenanceEvent,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
)


def main():
    """Demonstrate the Neo4j client library functionality."""
    
    # Get connection details from environment or use defaults
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print("=" * 60)
    print("Neo4j Aviation Client - Example Usage")
    print("=" * 60)
    print()
    
    # Connect to Neo4j
    try:
        with Neo4jConnection(uri, username, password, database) as conn:
            print(f"✓ Connected to Neo4j at {uri}")
            print()
            
            # Get a session
            session = conn.get_session()
            
            # Example 1: Working with Aircraft
            print("Example 1: Working with Aircraft")
            print("-" * 60)
            
            aircraft_repo = AircraftRepository(session)
            
            # Create aircraft
            aircraft = Aircraft(
                aircraft_id="AC_DEMO_001",
                tail_number="N12345",
                icao24="A12345",
                model="Boeing 737-800",
                operator="Example Airlines",
                manufacturer="Boeing"
            )
            aircraft_repo.create(aircraft)
            print(f"Created aircraft: {aircraft.tail_number} - {aircraft.model}")
            
            # Find aircraft by ID
            found = aircraft_repo.find_by_id("AC_DEMO_001")
            if found:
                print(f"Found aircraft: {found.tail_number} operated by {found.operator}")
            
            print()
            
            # Example 2: Working with Airports
            print("Example 2: Working with Airports")
            print("-" * 60)
            
            airport_repo = AirportRepository(session)
            
            # Create airports
            lax = Airport(
                airport_id="AP_LAX",
                iata="LAX",
                icao="KLAX",
                name="Los Angeles International",
                city="Los Angeles",
                country="USA",
                lat=33.9425,
                lon=-118.408
            )
            airport_repo.create(lax)
            print(f"Created airport: {lax.iata} - {lax.name}")
            
            jfk = Airport(
                airport_id="AP_JFK",
                iata="JFK",
                icao="KJFK",
                name="John F Kennedy International",
                city="New York",
                country="USA",
                lat=40.6413,
                lon=-73.7781
            )
            airport_repo.create(jfk)
            print(f"Created airport: {jfk.iata} - {jfk.name}")
            
            # Find airport by IATA
            found_airport = airport_repo.find_by_iata("LAX")
            if found_airport:
                print(f"Found airport: {found_airport.name} at ({found_airport.lat}, {found_airport.lon})")
            
            print()
            
            # Example 3: Working with Flights
            print("Example 3: Working with Flights")
            print("-" * 60)
            
            flight_repo = FlightRepository(session)
            
            # Create a flight
            flight = Flight(
                flight_id="FL_DEMO_001",
                flight_number="EX100",
                aircraft_id="AC_DEMO_001",
                operator="Example Airlines",
                origin="LAX",
                destination="JFK",
                scheduled_departure="2024-01-15T10:00:00Z",
                scheduled_arrival="2024-01-15T18:00:00Z"
            )
            flight_repo.create(flight)
            print(f"Created flight: {flight.flight_number} from {flight.origin} to {flight.destination}")
            
            # Find all flights
            all_flights = flight_repo.find_all(limit=10)
            print(f"Total flights in database: {len(all_flights)}")
            
            print()
            
            # Example 4: Working with Maintenance Events
            print("Example 4: Working with Maintenance Events")
            print("-" * 60)
            
            maint_repo = MaintenanceEventRepository(session)
            
            # Create a maintenance event
            event = MaintenanceEvent(
                event_id="ME_DEMO_001",
                aircraft_id="AC_DEMO_001",
                system_id="SYS_001",
                component_id="COMP_001",
                fault="Hydraulic pressure low",
                severity="WARNING",
                reported_at="2024-01-14T15:30:00Z",
                corrective_action="Replaced hydraulic pump"
            )
            maint_repo.create(event)
            print(f"Created maintenance event: {event.event_id} - {event.severity}")
            print(f"Fault: {event.fault}")
            print(f"Action: {event.corrective_action}")
            
            # Create a critical event
            critical_event = MaintenanceEvent(
                event_id="ME_DEMO_002",
                aircraft_id="AC_DEMO_001",
                system_id="SYS_002",
                component_id="COMP_002",
                fault="Engine failure",
                severity="CRITICAL",
                reported_at="2024-01-14T16:00:00Z",
                corrective_action="Emergency engine replacement"
            )
            maint_repo.create(critical_event)
            print(f"Created critical event: {critical_event.fault}")
            
            # Find critical events
            critical_events = maint_repo.find_by_severity("CRITICAL")
            print(f"Total CRITICAL events: {len(critical_events)}")
            
            print()
            
            # Clean up demo data
            print("Cleaning up demo data...")
            aircraft_repo.delete("AC_DEMO_001")
            flight_repo.delete("FL_DEMO_001")
            print("✓ Demo data cleaned up")
            
            print()
            print("=" * 60)
            print("Examples completed successfully!")
            print("=" * 60)
            
            session.close()
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
