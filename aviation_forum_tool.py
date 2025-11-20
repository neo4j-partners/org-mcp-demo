#!/usr/bin/env python3
"""
Aviation Forum Tool

Simple tool to read:
1. Aircraft components
2. Airports
3. Latest destinations
4. Missing components

This tool directly addresses the aviation forum requirements.
"""

import os
import sys
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository
)


def main():
    """Main function - Aviation Forum Tool."""
    
    # Get connection from environment
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    username = os.getenv('NEO4J_USERNAME', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD')
    database = os.getenv('NEO4J_DATABASE', 'neo4j')
    
    if not password:
        print("Error: Set NEO4J_PASSWORD environment variable")
        return 1
    
    try:
        with Neo4jConnection(uri, username, password, database) as conn:
            print("=" * 80)
            print("AVIATION FORUM TOOL - DATA RETRIEVAL")
            print("=" * 80)
            
            # 1. AIRCRAFT COMPONENTS
            print("\n[1] AIRCRAFT COMPONENTS")
            print("-" * 80)
            aircraft_repo = AircraftRepository(conn)
            aircraft_list = aircraft_repo.find_all(limit=5)
            
            for aircraft in aircraft_list:
                components = aircraft_repo.get_components(aircraft.aircraft_id)
                print(f"{aircraft.tail_number} ({aircraft.model}): {len(components)} components")
            
            # 2. AIRPORTS
            print("\n[2] AIRPORTS")
            print("-" * 80)
            airport_repo = AirportRepository(conn)
            airports = airport_repo.find_all(limit=10)
            
            for airport in airports:
                print(f"{airport.iata} - {airport.name} ({airport.city}, {airport.country})")
            
            # 3. LATEST DESTINATIONS
            print("\n[3] LATEST DESTINATIONS")
            print("-" * 80)
            flight_repo = FlightRepository(conn)
            destinations = flight_repo.find_latest_destinations(limit=10)
            
            for dest in destinations:
                flight = dest['flight']
                airport = dest['destination']
                print(f"Flight {flight.flight_number}: {flight.origin} → {airport.iata} ({airport.name})")
            
            # 4. MISSING COMPONENTS
            print("\n[4] MISSING COMPONENTS")
            print("-" * 80)
            maint_repo = MaintenanceEventRepository(conn)
            missing = maint_repo.find_missing_components(limit=10)
            
            if missing:
                for item in missing:
                    component = item['component']
                    event = item['maintenance_event']
                    print(f"{component.name} - {event.fault} [{event.severity}]")
            else:
                print("No critical component issues found.")
            
            print("\n" + "=" * 80)
            print("DATA RETRIEVAL COMPLETE")
            print("=" * 80)
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
