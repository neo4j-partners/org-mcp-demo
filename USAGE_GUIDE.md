# Aviation Client Usage Guide

This guide shows how to use the Neo4j Aviation Client to address the aviation forum requirements.

## Quick Start

### Installation

```bash
pip install neo4j pydantic
```

### Configuration

Set your Neo4j connection details:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your_password"
export NEO4J_DATABASE="neo4j"
```

## Aviation Forum Requirements

The issue requested: _"Tool to Read the aircraft components and airports and latest destinations include missing components the aviation forum need to get"_

### 1. Reading Aircraft Components

```python
from neo4j_client import Neo4jConnection, AircraftRepository

with Neo4jConnection(uri, username, password) as conn:
    repo = AircraftRepository(conn)
    
    # Get all aircraft
    aircraft_list = repo.find_all(limit=10)
    
    for aircraft in aircraft_list:
        print(f"Aircraft: {aircraft.tail_number} ({aircraft.model})")
        
        # Get all components for this aircraft
        components = repo.get_components(aircraft.aircraft_id)
        print(f"Total components: {len(components)}")
        
        for component in components:
            print(f"  - {component.name} ({component.type})")
```

**Key Methods:**
- `AircraftRepository.find_all()` - Get all aircraft
- `AircraftRepository.find_by_tail_number()` - Find specific aircraft
- `AircraftRepository.get_components()` - Get all components for an aircraft
- `AircraftRepository.get_systems()` - Get all systems for an aircraft

### 2. Reading Airports

```python
from neo4j_client import Neo4jConnection, AirportRepository

with Neo4jConnection(uri, username, password) as conn:
    repo = AirportRepository(conn)
    
    # Get all airports
    airports = repo.find_all()
    
    for airport in airports:
        print(f"{airport.iata} - {airport.name}")
        print(f"  Location: {airport.city}, {airport.country}")
        print(f"  Coordinates: ({airport.lat}, {airport.lon})")
```

**Key Methods:**
- `AirportRepository.find_all()` - Get all airports
- `AirportRepository.find_by_iata()` - Find by IATA code (e.g., "LAX")
- `AirportRepository.find_by_icao()` - Find by ICAO code (e.g., "KLAX")

### 3. Finding Latest Destinations

```python
from neo4j_client import Neo4jConnection, FlightRepository

with Neo4jConnection(uri, username, password) as conn:
    repo = FlightRepository(conn)
    
    # Get latest flight destinations
    destinations = repo.find_latest_destinations(limit=20)
    
    for dest in destinations:
        flight = dest['flight']
        airport = dest['destination']
        
        print(f"Flight {flight.flight_number}")
        print(f"  Route: {flight.origin} → {airport.iata}")
        print(f"  Destination: {airport.name} ({airport.city})")
        print(f"  Arrival: {flight.scheduled_arrival}")
```

**Key Methods:**
- `FlightRepository.find_latest_destinations()` - Get recent flights with destination info
- `FlightRepository.find_all()` - Get all flights
- `FlightRepository.find_by_aircraft()` - Get flights for a specific aircraft

### 4. Finding Missing/Faulty Components

This identifies components with critical maintenance issues that need attention:

```python
from neo4j_client import Neo4jConnection, MaintenanceEventRepository

with Neo4jConnection(uri, username, password) as conn:
    repo = MaintenanceEventRepository(conn)
    
    # Get components with critical issues
    missing = repo.find_missing_components(limit=50)
    
    for item in missing:
        component = item['component']
        event = item['maintenance_event']
        
        print(f"Component: {component.name}")
        print(f"  Fault: {event.fault}")
        print(f"  Severity: {event.severity}")
        print(f"  Reported: {event.reported_at}")
        print(f"  Aircraft: {event.aircraft_id}")
        print(f"  Action: {event.corrective_action}")
```

**Key Methods:**
- `MaintenanceEventRepository.find_missing_components()` - Get critical component issues
- `MaintenanceEventRepository.find_by_aircraft()` - Get events for specific aircraft
- `MaintenanceEventRepository.find_by_severity()` - Filter by severity level

## Complete Example

Run the demo script to see all features in action:

```bash
python demo_aviation_tool.py
```

Or run the specific examples:

```bash
python examples/aviation_forum_queries.py
```

## Data Models

The client provides Pydantic models with full type safety:

- **Aircraft** - Fleet aircraft with tail numbers and models
- **Airport** - Airports with IATA/ICAO codes and locations
- **Flight** - Flight operations with origin/destination
- **Component** - Aircraft components (parts of systems)
- **System** - Major aircraft systems (hydraulics, avionics, etc.)
- **MaintenanceEvent** - Maintenance records and faults

## Repository Classes

Each entity has a repository for data access:

- `AircraftRepository` - Query aircraft and their components
- `AirportRepository` - Query airports
- `FlightRepository` - Query flights and destinations
- `ComponentRepository` - Query components
- `MaintenanceEventRepository` - Query maintenance events
- `SystemRepository` - Query aircraft systems

## Security Features

✅ **Parameterized queries** - All Cypher queries use parameters to prevent SQL injection  
✅ **Type validation** - Pydantic models validate all data  
✅ **Connection management** - Context managers ensure proper cleanup  
✅ **Error handling** - Custom exceptions for better error messages

## Testing

Run the integration tests (requires running Neo4j instance):

```bash
pytest tests/
```

## Next Steps

For production use, consider adding:

- Caching for frequently accessed data
- Batch query operations
- Async/await support for concurrent queries
- Custom filtering and sorting options
- Data export utilities

## Support

For detailed API documentation, see [CLIENT_README.md](CLIENT_README.md)

For schema details, see [DATA_MODEL.md](DATA_MODEL.md)
