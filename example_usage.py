#!/usr/bin/env python
"""Example script demonstrating the Neo4j Aircraft Client library.

This script shows how to use the client library to manage aircraft information.
"""

import os
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft


def main():
    """Demonstrate basic usage of the aircraft client."""
    
    # Get connection details from environment variables
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print(f"Connecting to Neo4j at {uri}...")
    
    # Connect to Neo4j using context manager
    with Neo4jConnection(uri, username, password, database) as conn:
        # Create repository
        aircraft_repo = AircraftRepository(conn)
        
        print("\n1. Creating a new aircraft...")
        new_aircraft = Aircraft(
            aircraft_id="AC9001",
            tail_number="N12345X",
            icao24="abc123",
            model="B787-9",
            operator="DemoAir",
            manufacturer="Boeing"
        )
        
        created = aircraft_repo.create(new_aircraft)
        print(f"   Created: {created.tail_number} - {created.model}")
        
        print("\n2. Finding aircraft by ID...")
        found = aircraft_repo.find_by_id("AC9001")
        if found:
            print(f"   Found: {found.tail_number} operated by {found.operator}")
        
        print("\n3. Finding all aircraft (first 5)...")
        all_aircraft = aircraft_repo.find_all(limit=5)
        print(f"   Found {len(all_aircraft)} aircraft:")
        for aircraft in all_aircraft:
            print(f"   - {aircraft.tail_number}: {aircraft.manufacturer} {aircraft.model}")
        
        print("\n4. Finding Boeing aircraft...")
        boeing_aircraft = aircraft_repo.find_by_manufacturer("Boeing")
        print(f"   Found {len(boeing_aircraft)} Boeing aircraft")
        
        print("\n5. Updating aircraft operator...")
        new_aircraft.operator = "UpdatedAir"
        updated = aircraft_repo.update(new_aircraft)
        print(f"   Updated operator to: {updated.operator}")
        
        print("\n6. Deleting the test aircraft...")
        deleted = aircraft_repo.delete("AC9001")
        print(f"   Deleted: {deleted}")
        
        print("\n✅ Example completed successfully!")


if __name__ == "__main__":
    main()
