#!/usr/bin/env python3
"""
Aviation Forum Query Examples

This script demonstrates specific queries for the aviation forum use case:
1. Reading aircraft components
2. Listing airports
3. Finding latest destinations
4. Identifying missing/faulty components
"""

import os
import sys

# Add parent directory to path to import neo4j_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository
)


def get_connection_params():
    """Get Neo4j connection parameters from environment."""
    return {
        'uri': os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
        'username': os.getenv('NEO4J_USERNAME', 'neo4j'),
        'password': os.getenv('NEO4J_PASSWORD', ''),
        'database': os.getenv('NEO4J_DATABASE', 'neo4j')
    }


def query_aircraft_components():
    """Example: Query aircraft and their components."""
    print("\n=== Aircraft Components Query ===\n")
    
    params = get_connection_params()
    with Neo4jConnection(**params) as conn:
        repo = AircraftRepository(conn)
        
        # Get all aircraft
        aircraft_list = repo.find_all(limit=5)
        print(f"Found {len(aircraft_list)} aircraft\n")
        
        for aircraft in aircraft_list:
            print(f"Aircraft: {aircraft.tail_number} ({aircraft.model})")
            
            # Get components for this aircraft
            components = repo.get_components(aircraft.aircraft_id)
            print(f"  Total components: {len(components)}")
            
            # Show sample components
            if components:
                print("  Sample components:")
                for comp in components[:5]:
                    print(f"    - {comp.name} (Type: {comp.type})")
            print()


def query_airports():
    """Example: Query all airports."""
    print("\n=== Airports Query ===\n")
    
    params = get_connection_params()
    with Neo4jConnection(**params) as conn:
        repo = AirportRepository(conn)
        
        # Get all airports
        airports = repo.find_all(limit=20)
        print(f"Found {len(airports)} airports\n")
        
        for airport in airports:
            print(f"{airport.iata:4} | {airport.name:40} | {airport.city}, {airport.country}")


def query_latest_destinations():
    """Example: Query latest flight destinations."""
    print("\n=== Latest Destinations Query ===\n")
    
    params = get_connection_params()
    with Neo4jConnection(**params) as conn:
        repo = FlightRepository(conn)
        
        # Get latest destinations
        destinations = repo.find_latest_destinations(limit=15)
        print(f"Found {len(destinations)} recent flights\n")
        
        for dest in destinations:
            flight = dest['flight']
            airport = dest['destination']
            print(f"Flight {flight.flight_number:8} | {flight.origin} → {airport.iata} | {airport.name}")
            print(f"           Arrival: {flight.scheduled_arrival}")
            print()


def query_missing_components():
    """Example: Query missing/faulty components (critical maintenance issues)."""
    print("\n=== Missing/Faulty Components Query ===\n")
    
    params = get_connection_params()
    with Neo4jConnection(**params) as conn:
        repo = MaintenanceEventRepository(conn)
        
        # Get critical component issues
        missing = repo.find_missing_components(limit=20)
        
        if missing:
            print(f"Found {len(missing)} critical component issues\n")
            
            for item in missing:
                component = item['component']
                event = item['maintenance_event']
                
                print(f"Component: {component.name} (ID: {component.component_id})")
                print(f"  Type: {component.type}")
                print(f"  Fault: {event.fault}")
                print(f"  Severity: {event.severity}")
                print(f"  Reported: {event.reported_at}")
                print(f"  Aircraft: {event.aircraft_id}")
                print(f"  Action: {event.corrective_action}")
                print()
        else:
            print("No critical component issues found.")


def main():
    """Run all example queries."""
    try:
        print("=" * 80)
        print("AVIATION FORUM QUERY EXAMPLES")
        print("=" * 80)
        
        # Run each query example
        query_aircraft_components()
        query_airports()
        query_latest_destinations()
        query_missing_components()
        
        print("=" * 80)
        print("All queries completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nMake sure to set environment variables:")
        print("  export NEO4J_URI='bolt://localhost:7687'")
        print("  export NEO4J_USERNAME='neo4j'")
        print("  export NEO4J_PASSWORD='your_password'")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
