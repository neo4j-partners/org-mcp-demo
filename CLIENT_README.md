# Neo4j Aviation Client

A Python client library for querying the Aviation Neo4j database. This library provides a clean, type-safe interface for accessing aircraft, airports, flights, components, and maintenance data.

## Features

✅ **Type-safe models** - Pydantic models for all entities  
✅ **Repository pattern** - Clean separation of data access logic  
✅ **Parameterized queries** - All Cypher queries use parameters to prevent injection attacks  
✅ **Connection management** - Context manager support for automatic cleanup  
✅ **Comprehensive coverage** - Access to aircraft, airports, flights, systems, components, and maintenance events  
✅ **Integration tested** - Tests using pytest with the actual database

## Installation

### Prerequisites

- Python 3.9 or higher
- Access to a Neo4j database with the aviation schema

### Install Dependencies

```bash
pip install neo4j pydantic
```

For development and testing:

```bash
pip install neo4j pydantic pytest testcontainers
```

## Quick Start

### Basic Usage

```python
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    ComponentRepository,
    MaintenanceEventRepository
)

# Create connection
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password",
    database="neo4j"
) as conn:
    # Use repositories to query data
    aircraft_repo = AircraftRepository(conn)
    
    # Get all aircraft
    aircraft = aircraft_repo.find_all(limit=10)
    for a in aircraft:
        print(f"{a.tail_number}: {a.model} ({a.manufacturer})")
```

### Find Aircraft Components

```python
from neo4j_client import Neo4jConnection, AircraftRepository

with Neo4jConnection(uri, username, password) as conn:
    repo = AircraftRepository(conn)
    
    # Get an aircraft
    aircraft = repo.find_by_tail_number("N12345")
    
    if aircraft:
        # Get all components for this aircraft
        components = repo.get_components(aircraft.aircraft_id)
        
        print(f"Components for {aircraft.tail_number}:")
        for component in components:
            print(f"  - {component.name} ({component.type})")
```

### Find Airports

```python
from neo4j_client import Neo4jConnection, AirportRepository

with Neo4jConnection(uri, username, password) as conn:
    repo = AirportRepository(conn)
    
    # Get all airports
    airports = repo.find_all()
    
    for airport in airports:
        print(f"{airport.iata} - {airport.name} ({airport.city}, {airport.country})")
    
    # Find specific airport
    lax = repo.find_by_iata("LAX")
    if lax:
        print(f"Found: {lax.name} at ({lax.lat}, {lax.lon})")
```

### Find Latest Destinations

```python
from neo4j_client import Neo4jConnection, FlightRepository

with Neo4jConnection(uri, username, password) as conn:
    repo = FlightRepository(conn)
    
    # Get latest flight destinations
    destinations = repo.find_latest_destinations(limit=20)
    
    print("Latest Destinations:")
    for dest in destinations:
        flight = dest['flight']
        airport = dest['destination']
        print(f"Flight {flight.flight_number}: {flight.origin} → {airport.iata} ({airport.name})")
        print(f"  Scheduled arrival: {flight.scheduled_arrival}")
```

### Find Missing/Faulty Components

```python
from neo4j_client import Neo4jConnection, MaintenanceEventRepository

with Neo4jConnection(uri, username, password) as conn:
    repo = MaintenanceEventRepository(conn)
    
    # Get components with critical maintenance events
    missing = repo.find_missing_components(limit=50)
    
    print("Critical Component Issues:")
    for item in missing:
        component = item['component']
        event = item['maintenance_event']
        
        print(f"\nComponent: {component.name} ({component.component_id})")
        print(f"  Fault: {event.fault}")
        print(f"  Severity: {event.severity}")
        print(f"  Reported: {event.reported_at}")
        print(f"  Action: {event.corrective_action}")
```

## Repository Overview

### AircraftRepository

Query aircraft information and related data.

**Methods:**
- `find_all(limit)` - Get all aircraft
- `find_by_id(aircraft_id)` - Find by ID
- `find_by_tail_number(tail_number)` - Find by tail number
- `get_systems(aircraft_id)` - Get all systems for an aircraft
- `get_components(aircraft_id)` - Get all components for an aircraft

### AirportRepository

Query airport information.

**Methods:**
- `find_all(limit)` - Get all airports
- `find_by_iata(iata)` - Find by IATA code
- `find_by_icao(icao)` - Find by ICAO code

### FlightRepository

Query flight operations and destinations.

**Methods:**
- `find_all(limit)` - Get all flights
- `find_by_id(flight_id)` - Find by ID
- `find_by_aircraft(aircraft_id, limit)` - Get flights for specific aircraft
- `find_latest_destinations(limit)` - Get latest flight destinations with airport details

### ComponentRepository

Query aircraft components.

**Methods:**
- `find_all(limit)` - Get all components
- `find_by_id(component_id)` - Find by ID
- `find_by_system(system_id)` - Get components for a specific system

### MaintenanceEventRepository

Query maintenance events and identify faulty components.

**Methods:**
- `find_all(limit)` - Get all maintenance events
- `find_by_aircraft(aircraft_id, limit)` - Get events for specific aircraft
- `find_by_severity(severity, limit)` - Get events by severity level
- `find_missing_components(limit)` - Get critical component issues

### SystemRepository

Query aircraft systems.

**Methods:**
- `find_all(limit)` - Get all systems
- `find_by_id(system_id)` - Find by ID

## Environment Variables

The library uses the following environment variables for configuration:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your_password"
export NEO4J_DATABASE="neo4j"
```

## Testing

Run the integration tests:

```bash
# Ensure Neo4j is running and environment variables are set
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your_password"

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=neo4j_client --cov-report=html
```

## Data Models

The library provides Pydantic models for the following entities:

- **Aircraft** - Commercial aircraft in the fleet
- **Airport** - Airports with location and identification codes
- **Flight** - Scheduled flight operations
- **System** - Major aircraft systems (hydraulics, avionics, engines)
- **Component** - Components within aircraft systems
- **Sensor** - Sensors that monitor systems
- **Reading** - Time-series sensor readings
- **MaintenanceEvent** - Maintenance events and fault reports
- **Delay** - Flight delay incidents

## Architecture

The library follows the Repository pattern:

```
neo4j_client/
├── models.py         # Pydantic data models
├── connection.py     # Connection management
├── repository.py     # Repository classes for queries
└── exceptions.py     # Custom exceptions
```

## Security

✅ All Cypher queries use **parameterized queries** to prevent injection attacks  
✅ Connection credentials are managed securely  
✅ Context managers ensure proper resource cleanup  
✅ Type validation with Pydantic models

## Next Steps

This is a foundational client library. Consider extending it with:

- [ ] Async/await support for concurrent queries
- [ ] Caching layer for frequently accessed data
- [ ] Batch operations for bulk data loading
- [ ] Custom query builders for complex filtering
- [ ] Relationship traversal helpers
- [ ] Data export utilities
- [ ] CLI tools for common operations
- [ ] Monitoring and logging integration

## License

MIT License

## Contributing

Contributions are welcome! Please ensure:

1. All queries use parameters (no string interpolation)
2. Type hints on all functions
3. Tests for new functionality
4. Documentation updates

## Support

For issues or questions:

1. Check the [DATA_MODEL.md](DATA_MODEL.md) for schema details
2. Review the test files for usage examples
3. Open an issue on GitHub

## Example: Complete Aviation Forum Tool

Here's a complete example that addresses the aviation forum requirements:

```python
#!/usr/bin/env python3
"""
Aviation Forum Tool - Read aircraft components, airports, and latest destinations
"""

import os
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    AirportRepository,
    FlightRepository,
    MaintenanceEventRepository
)


def main():
    # Get connection details from environment
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    if not password:
        print("Error: NEO4J_PASSWORD environment variable not set")
        return
    
    # Connect to database
    with Neo4jConnection(uri, username, password, database) as conn:
        print("=" * 80)
        print("AVIATION FORUM REPORT")
        print("=" * 80)
        
        # 1. Aircraft Components
        print("\n1. AIRCRAFT COMPONENTS")
        print("-" * 80)
        aircraft_repo = AircraftRepository(conn)
        aircraft_list = aircraft_repo.find_all(limit=5)
        
        for aircraft in aircraft_list:
            print(f"\nAircraft: {aircraft.tail_number} ({aircraft.model})")
            components = aircraft_repo.get_components(aircraft.aircraft_id)
            print(f"  Total Components: {len(components)}")
            if components:
                print(f"  Sample Components:")
                for comp in components[:3]:
                    print(f"    - {comp.name} ({comp.type})")
        
        # 2. Airports
        print("\n\n2. AIRPORTS")
        print("-" * 80)
        airport_repo = AirportRepository(conn)
        airports = airport_repo.find_all(limit=10)
        
        for airport in airports:
            print(f"{airport.iata} ({airport.icao}) - {airport.name}")
            print(f"  Location: {airport.city}, {airport.country}")
            print(f"  Coordinates: {airport.lat}, {airport.lon}")
        
        # 3. Latest Destinations
        print("\n\n3. LATEST DESTINATIONS")
        print("-" * 80)
        flight_repo = FlightRepository(conn)
        destinations = flight_repo.find_latest_destinations(limit=10)
        
        for dest in destinations:
            flight = dest['flight']
            airport = dest['destination']
            print(f"Flight {flight.flight_number}: {flight.origin} → {airport.iata}")
            print(f"  Destination: {airport.name} ({airport.city})")
            print(f"  Arrival: {flight.scheduled_arrival}")
        
        # 4. Missing Components (Critical Maintenance Issues)
        print("\n\n4. MISSING/FAULTY COMPONENTS")
        print("-" * 80)
        maint_repo = MaintenanceEventRepository(conn)
        missing = maint_repo.find_missing_components(limit=10)
        
        if missing:
            for item in missing:
                component = item['component']
                event = item['maintenance_event']
                print(f"\nComponent: {component.name} (ID: {component.component_id})")
                print(f"  Type: {component.type}")
                print(f"  Fault: {event.fault}")
                print(f"  Severity: {event.severity}")
                print(f"  Reported: {event.reported_at}")
                print(f"  Action Taken: {event.corrective_action}")
        else:
            print("No critical component issues found.")
        
        print("\n" + "=" * 80)
        print("Report Complete")
        print("=" * 80)


if __name__ == "__main__":
    main()
```

Save this as `aviation_forum_tool.py` and run:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your_password"

python aviation_forum_tool.py
```

This tool provides all the information requested for the aviation forum.
