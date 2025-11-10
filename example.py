#!/usr/bin/env python3
"""
Example script demonstrating the Neo4j airplane client.

This script connects to the Neo4j database and queries existing airplane data.
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    FlightRepository,
    AirportRepository,
    MaintenanceEventRepository
)


def main():
    # Get connection details from environment variables
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print(f"Connecting to Neo4j at {uri}...")
    
    # Create connection using context manager
    with Neo4jConnection(uri, username, password, database) as connection:
        print("✓ Connected successfully!\n")
        
        # Example 1: Query Aircraft
        print("=" * 60)
        print("AIRCRAFT EXAMPLES")
        print("=" * 60)
        
        with connection.get_session() as session:
            aircraft_repo = AircraftRepository(session)
            
            # Find all aircraft (limit to 5 for display)
            all_aircraft = aircraft_repo.find_all(limit=5)
            print(f"\nFound {len(all_aircraft)} aircraft (showing first 5):")
            for aircraft in all_aircraft:
                print(f"  • {aircraft.tail_number} - {aircraft.manufacturer} {aircraft.model}")
                print(f"    Operator: {aircraft.operator}")
            
            # Find aircraft by operator (if any exist)
            if all_aircraft:
                operator = all_aircraft[0].operator
                operator_aircraft = aircraft_repo.find_by_operator(operator)
                print(f"\n{operator} operates {len(operator_aircraft)} aircraft")
        
        # Example 2: Query Airports
        print("\n" + "=" * 60)
        print("AIRPORT EXAMPLES")
        print("=" * 60)
        
        with connection.get_session() as session:
            airport_repo = AirportRepository(session)
            
            # Find all airports (limit to 5)
            all_airports = airport_repo.find_all(limit=5)
            print(f"\nFound {len(all_airports)} airports (showing first 5):")
            for airport in all_airports:
                print(f"  • {airport.iata}/{airport.icao} - {airport.name}")
                print(f"    Location: {airport.city}, {airport.country} ({airport.lat:.4f}, {airport.lon:.4f})")
            
            # Find specific airport by IATA (if any exist)
            if all_airports:
                iata = all_airports[0].iata
                specific_airport = airport_repo.find_by_iata(iata)
                if specific_airport:
                    print(f"\nDetails for {iata}:")
                    print(f"  Name: {specific_airport.name}")
                    print(f"  City: {specific_airport.city}, {specific_airport.country}")
        
        # Example 3: Query Flights
        print("\n" + "=" * 60)
        print("FLIGHT EXAMPLES")
        print("=" * 60)
        
        with connection.get_session() as session:
            flight_repo = FlightRepository(session)
            aircraft_repo = AircraftRepository(session)
            
            # Get first aircraft and find its flights
            all_aircraft = aircraft_repo.find_all(limit=1)
            if all_aircraft:
                aircraft = all_aircraft[0]
                flights = flight_repo.find_by_aircraft(aircraft.aircraft_id)
                print(f"\nAircraft {aircraft.tail_number} has operated {len(flights)} flights")
                
                # Show first 3 flights
                for flight in flights[:3]:
                    print(f"  • {flight.flight_number}: {flight.origin} → {flight.destination}")
                    print(f"    Departure: {flight.scheduled_departure}")
                    print(f"    Arrival: {flight.scheduled_arrival}")
        
        # Example 4: Query Maintenance Events
        print("\n" + "=" * 60)
        print("MAINTENANCE EVENT EXAMPLES")
        print("=" * 60)
        
        with connection.get_session() as session:
            maintenance_repo = MaintenanceEventRepository(session)
            aircraft_repo = AircraftRepository(session)
            
            # Get first aircraft and find maintenance events
            all_aircraft = aircraft_repo.find_all(limit=1)
            if all_aircraft:
                aircraft = all_aircraft[0]
                events = maintenance_repo.find_by_aircraft(aircraft.aircraft_id)
                print(f"\nAircraft {aircraft.tail_number} has {len(events)} maintenance events")
                
                # Show first 3 events
                for event in events[:3]:
                    print(f"  • {event.reported_at}")
                    print(f"    Fault: {event.fault}")
                    print(f"    Severity: {event.severity}")
                    print(f"    Action: {event.corrective_action}")
        
        print("\n" + "=" * 60)
        print("Example completed successfully!")
        print("=" * 60)


if __name__ == "__main__":
    main()
