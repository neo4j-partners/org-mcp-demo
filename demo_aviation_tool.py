#!/usr/bin/env python3
"""
Aviation Forum Tool - Demonstration

This script demonstrates the Neo4j aviation client library by reading:
1. Aircraft components
2. Airports
3. Latest destinations
4. Missing/faulty components (critical maintenance events)
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository,
    SystemRepository
)


def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_subheader(title):
    """Print a formatted subsection header."""
    print(f"\n{title}")
    print("-" * 80)


def main():
    """Main function to demonstrate the aviation client library."""
    
    # Get connection details from environment
    # The MCP server provides these through COPILOT_MCP_* variables
    uri = os.getenv("NEO4J_URI") or os.getenv("COPILOT_MCP_NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME") or os.getenv("COPILOT_MCP_NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD") or os.getenv("COPILOT_MCP_NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE") or os.getenv("COPILOT_MCP_NEO4J_DATABASE", "neo4j")
    
    if not password:
        print("Error: NEO4J_PASSWORD or COPILOT_MCP_NEO4J_PASSWORD environment variable not set")
        return 1
    
    try:
        # Connect to database
        print_header("AVIATION FORUM REPORT")
        print(f"Connecting to Neo4j at {uri}...")
        
        with Neo4jConnection(uri, username, password, database) as conn:
            print("✓ Connected successfully!\n")
            
            # 1. AIRCRAFT COMPONENTS
            print_subheader("1. AIRCRAFT COMPONENTS")
            aircraft_repo = AircraftRepository(conn)
            aircraft_list = aircraft_repo.find_all(limit=3)
            
            print(f"Found {len(aircraft_list)} aircraft (showing first 3):\n")
            for aircraft in aircraft_list:
                print(f"Aircraft: {aircraft.tail_number}")
                print(f"  Model: {aircraft.model}")
                print(f"  Manufacturer: {aircraft.manufacturer}")
                print(f"  Operator: {aircraft.operator}")
                
                # Get systems for this aircraft
                systems = aircraft_repo.get_systems(aircraft.aircraft_id)
                print(f"  Systems: {len(systems)}")
                
                # Get components for this aircraft
                components = aircraft_repo.get_components(aircraft.aircraft_id)
                print(f"  Total Components: {len(components)}")
                
                if components:
                    print(f"  Sample Components (first 3):")
                    for comp in components[:3]:
                        print(f"    • {comp.name} ({comp.type})")
                print()
            
            # 2. AIRPORTS
            print_subheader("2. AIRPORTS")
            airport_repo = AirportRepository(conn)
            airports = airport_repo.find_all(limit=10)
            
            print(f"Found {len(airports)} airports (showing first 10):\n")
            for airport in airports:
                print(f"{airport.iata} ({airport.icao}) - {airport.name}")
                print(f"  Location: {airport.city}, {airport.country}")
                print(f"  Coordinates: ({airport.lat:.4f}, {airport.lon:.4f})")
            
            # 3. LATEST DESTINATIONS
            print_subheader("3. LATEST FLIGHT DESTINATIONS")
            flight_repo = FlightRepository(conn)
            destinations = flight_repo.find_latest_destinations(limit=10)
            
            print(f"Found {len(destinations)} recent flights (showing first 10):\n")
            for dest in destinations:
                flight = dest['flight']
                airport = dest['destination']
                print(f"Flight {flight.flight_number}")
                print(f"  Route: {flight.origin} → {airport.iata}")
                print(f"  Destination: {airport.name} ({airport.city})")
                print(f"  Aircraft: {flight.aircraft_id}")
                print(f"  Scheduled Arrival: {flight.scheduled_arrival}")
                print()
            
            # 4. MISSING/FAULTY COMPONENTS (Critical Maintenance)
            print_subheader("4. CRITICAL COMPONENT ISSUES (Missing/Faulty)")
            maint_repo = MaintenanceEventRepository(conn)
            missing = maint_repo.find_missing_components(limit=10)
            
            if missing:
                print(f"Found {len(missing)} critical component issues:\n")
                for item in missing:
                    component = item['component']
                    event = item['maintenance_event']
                    print(f"Component: {component.name}")
                    print(f"  ID: {component.component_id}")
                    print(f"  Type: {component.type}")
                    print(f"  System: {component.system_id}")
                    print(f"  Fault: {event.fault}")
                    print(f"  Severity: {event.severity}")
                    print(f"  Reported: {event.reported_at}")
                    print(f"  Aircraft: {event.aircraft_id}")
                    print(f"  Corrective Action: {event.corrective_action}")
                    print()
            else:
                print("✓ No critical component issues found.\n")
            
            # 5. SYSTEM OVERVIEW
            print_subheader("5. SYSTEM OVERVIEW")
            system_repo = SystemRepository(conn)
            systems = system_repo.find_all(limit=10)
            
            print(f"Found {len(systems)} systems (showing first 10):\n")
            system_types = {}
            for system in systems:
                system_types[system.type] = system_types.get(system.type, 0) + 1
            
            print("System Types Distribution:")
            for sys_type, count in sorted(system_types.items()):
                print(f"  • {sys_type}: {count}")
            
            print_header("REPORT COMPLETE")
            print("✓ All data retrieved successfully")
            print("=" * 80 + "\n")
            
            return 0
            
    except Exception as e:
        print(f"\n✗ Error: {str(e)}\n")
        return 1


if __name__ == "__main__":
    exit(main())
