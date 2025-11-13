#!/usr/bin/env python3
"""
Example usage of the Neo4j Aircraft Client library.

This script demonstrates how to use the client library to query aircraft data.
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    FlightRepository,
    MaintenanceEventRepository,
    AirportRepository,
    Aircraft
)


def main():
    # Get connection details from environment variables
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print("=" * 70)
    print("Neo4j Aircraft Data Client - Example Usage")
    print("=" * 70)
    
    # Use context manager for automatic connection handling
    with Neo4jConnection(uri, username, password, database) as connection:
        session = connection.get_session()
        
        # Example 1: Query Aircraft
        print("\n1. Querying Aircraft")
        print("-" * 70)
        aircraft_repo = AircraftRepository(session)
        
        aircraft_list = aircraft_repo.find_all(limit=5)
        print(f"Found {len(aircraft_list)} aircraft:")
        
        for aircraft in aircraft_list[:3]:
            print(f"\n  • {aircraft.tail_number} ({aircraft.model})")
            print(f"    Operator: {aircraft.operator}")
            print(f"    Manufacturer: {aircraft.manufacturer}")
        
        # Example 2: Query Flights for an Aircraft
        if aircraft_list:
            print("\n2. Querying Flights for Aircraft")
            print("-" * 70)
            
            first_aircraft = aircraft_list[0]
            flight_repo = FlightRepository(session)
            
            flights = flight_repo.find_by_aircraft(first_aircraft.aircraft_id, limit=5)
            print(f"Aircraft {first_aircraft.tail_number} has {len(flights)} recent flights:")
            
            for i, flight in enumerate(flights[:3], 1):
                print(f"  {i}. {flight.flight_number}: {flight.origin} → {flight.destination}")
                print(f"     Departure: {flight.scheduled_departure}")
        
        # Example 3: Query Flights by Route
        print("\n3. Querying Flights by Route")
        print("-" * 70)
        
        # Find a sample route from existing flights
        if flights:
            sample_origin = flights[0].origin
            sample_dest = flights[0].destination
            
            route_flights = flight_repo.find_by_route(sample_origin, sample_dest, limit=5)
            print(f"Flights from {sample_origin} to {sample_dest}: {len(route_flights)}")
        
        # Example 4: Query Airports
        print("\n4. Querying Airports")
        print("-" * 70)
        airport_repo = AirportRepository(session)
        
        airports = airport_repo.find_all(limit=5)
        print(f"Found {len(airports)} airports:")
        
        for airport in airports[:3]:
            print(f"\n  • {airport.iata} / {airport.icao}")
            print(f"    {airport.name}")
            print(f"    Location: {airport.city}, {airport.country}")
            print(f"    Coordinates: {airport.lat:.4f}, {airport.lon:.4f}")
        
        # Example 5: Query Maintenance Events
        print("\n5. Querying Maintenance Events")
        print("-" * 70)
        maintenance_repo = MaintenanceEventRepository(session)
        
        critical_events = maintenance_repo.find_critical_events(limit=5)
        print(f"Found {len(critical_events)} critical maintenance events:")
        
        for i, event in enumerate(critical_events[:3], 1):
            print(f"\n  {i}. Event ID: {event.event_id}")
            print(f"     Severity: {event.severity}")
            print(f"     Fault: {event.fault}")
            print(f"     Corrective Action: {event.corrective_action}")
        
        # Example 6: Create a New Aircraft (if you have write permissions)
        print("\n6. Creating a New Aircraft (Example)")
        print("-" * 70)
        
        new_aircraft = Aircraft(
            aircraft_id="DEMO001",
            tail_number="N99999",
            icao24="DEMO99",
            model="Boeing 787-9",
            operator="Demo Airlines",
            manufacturer="Boeing"
        )
        
        print("Creating aircraft:")
        print(f"  Tail: {new_aircraft.tail_number}")
        print(f"  Model: {new_aircraft.model}")
        print(f"  Operator: {new_aircraft.operator}")
        
        try:
            created = aircraft_repo.create(new_aircraft)
            print(f"✅ Successfully created aircraft: {created.aircraft_id}")
            
            # Clean up the demo aircraft
            aircraft_repo.delete(created.aircraft_id)
            print(f"✅ Cleaned up demo aircraft")
        except Exception as e:
            print(f"⚠️  Note: {e}")
            print("   (This is expected if you don't have write permissions)")
        
        session.close()
    
    print("\n" + "=" * 70)
    print("Example completed successfully!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
