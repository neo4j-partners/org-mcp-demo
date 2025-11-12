#!/usr/bin/env python3
"""
Example script demonstrating the Neo4j Aircraft Client library.

This script shows how to use the client to query aircraft data from Neo4j.
Set NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, and NEO4J_DATABASE environment
variables to connect to your Neo4j instance.
"""

import os
import sys
from neo4j_aircraft_client import (
    Neo4jConnection,
    AircraftRepository,
    FlightRepository,
    AirportRepository,
    SystemRepository,
    MaintenanceEventRepository,
)


def main():
    """Main entry point for the example script."""
    
    # Get connection details from environment variables
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    if not password:
        print("Error: NEO4J_PASSWORD environment variable is required", file=sys.stderr)
        sys.exit(1)
    
    print(f"Connecting to Neo4j at {uri}...")
    print()
    
    # Use context manager for automatic connection cleanup
    with Neo4jConnection(uri, username, password, database) as conn:
        with conn.session() as session:
            # Example 1: List all aircraft
            print("=" * 60)
            print("Example 1: List All Aircraft")
            print("=" * 60)
            aircraft_repo = AircraftRepository(session)
            aircraft_list = aircraft_repo.find_all(limit=5)
            
            if aircraft_list:
                for aircraft in aircraft_list:
                    print(f"✈️  {aircraft.tail_number} - {aircraft.model}")
                    print(f"   Operator: {aircraft.operator}")
                    print(f"   Manufacturer: {aircraft.manufacturer}")
                    print()
            else:
                print("No aircraft found in database")
                print()
            
            # Example 2: Get flights for the first aircraft
            if aircraft_list:
                print("=" * 60)
                print("Example 2: Flights for Aircraft")
                print("=" * 60)
                first_aircraft = aircraft_list[0]
                print(f"Aircraft: {first_aircraft.tail_number} ({first_aircraft.model})")
                print()
                
                flight_repo = FlightRepository(session)
                flights = flight_repo.find_by_aircraft(first_aircraft.aircraft_id, limit=5)
                
                if flights:
                    for flight in flights:
                        print(f"🛫 Flight {flight.flight_number}")
                        print(f"   Route: {flight.origin} → {flight.destination}")
                        print(f"   Departure: {flight.scheduled_departure}")
                        print(f"   Arrival: {flight.scheduled_arrival}")
                        print()
                else:
                    print("No flights found for this aircraft")
                    print()
            
            # Example 3: List airports
            print("=" * 60)
            print("Example 3: List Airports")
            print("=" * 60)
            airport_repo = AirportRepository(session)
            airports = airport_repo.find_all(limit=5)
            
            if airports:
                for airport in airports:
                    print(f"🏢 {airport.name} ({airport.iata}/{airport.icao})")
                    print(f"   Location: {airport.city}, {airport.country}")
                    print(f"   Coordinates: {airport.lat}, {airport.lon}")
                    print()
            else:
                print("No airports found in database")
                print()
            
            # Example 4: Find critical maintenance events
            print("=" * 60)
            print("Example 4: Critical Maintenance Events")
            print("=" * 60)
            maintenance_repo = MaintenanceEventRepository(session)
            critical_events = maintenance_repo.find_by_severity("CRITICAL", limit=5)
            
            if critical_events:
                for event in critical_events:
                    print(f"⚠️  Event {event.event_id}")
                    print(f"   Aircraft: {event.aircraft_id}")
                    print(f"   System: {event.system_id}")
                    print(f"   Fault: {event.fault}")
                    print(f"   Reported: {event.reported_at}")
                    print(f"   Action: {event.corrective_action}")
                    print()
            else:
                print("No critical maintenance events found")
                print()
            
            # Example 5: Get aircraft systems
            if aircraft_list:
                print("=" * 60)
                print("Example 5: Aircraft Systems")
                print("=" * 60)
                first_aircraft = aircraft_list[0]
                print(f"Aircraft: {first_aircraft.tail_number}")
                print()
                
                system_repo = SystemRepository(session)
                systems = system_repo.find_by_aircraft(first_aircraft.aircraft_id)
                
                if systems:
                    for system in systems:
                        print(f"🔧 {system.name} ({system.type})")
                    print()
                else:
                    print("No systems found for this aircraft")
                    print()
            
            # Example 6: Query a specific airport by IATA code
            print("=" * 60)
            print("Example 6: Query Airport by IATA Code")
            print("=" * 60)
            
            # Try to find LAX
            lax = airport_repo.find_by_iata("LAX")
            if lax:
                print(f"Found airport: {lax.name}")
                print(f"IATA: {lax.iata}")
                print(f"ICAO: {lax.icao}")
                print(f"Location: {lax.city}, {lax.country}")
                print(f"Coordinates: ({lax.lat}, {lax.lon})")
            else:
                print("LAX airport not found in database")
            print()
    
    print("=" * 60)
    print("Examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
