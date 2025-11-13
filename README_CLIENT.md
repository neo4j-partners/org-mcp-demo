# Neo4j Aircraft Client

A Python client library for working with aircraft data in Neo4j. This library provides a clean, type-safe interface for querying and managing aviation data including aircraft, flights, maintenance events, and more.

## Features

✅ **Type-Safe Models** - Pydantic models for all entities with full type hints  
✅ **Repository Pattern** - Clean separation of data access logic  
✅ **Parameterized Queries** - All Cypher queries use parameters to prevent injection  
✅ **Connection Management** - Context manager support for safe resource cleanup  
✅ **Comprehensive Testing** - Integration tests with testcontainers  
✅ **Modern Python** - Built for Python 3.9+ with PEP 621 packaging  

## Installation

```bash
pip install -e .
```

For development with testing dependencies:

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from neo4j_client import Neo4jConnection, AircraftRepository

# Connect to Neo4j
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="password"
) as conn:
    # Get a session
    session = conn.get_session()
    
    # Use a repository
    aircraft_repo = AircraftRepository(session)
    
    # Find an aircraft by tail number
    aircraft = aircraft_repo.find_by_tail_number("N12345")
    if aircraft:
        print(f"Found: {aircraft.model} operated by {aircraft.operator}")
    
    # Find all aircraft for an operator
    fleet = aircraft_repo.find_by_operator("United Airlines")
    print(f"Fleet size: {len(fleet)}")
    
    session.close()
```

### Working with Flights

```python
from neo4j_client import FlightRepository

session = conn.get_session()
flight_repo = FlightRepository(session)

# Find all flights for an aircraft
flights = flight_repo.find_by_aircraft("AC001")

# Find flights by route
lax_to_jfk = flight_repo.find_by_route("LAX", "JFK")

# Find flights with significant delays
delayed_flights = flight_repo.find_with_delays(min_delay_minutes=60)
for item in delayed_flights:
    flight = item["flight"]
    delay = item["delay"]
    print(f"Flight {flight.flight_number}: {delay.minutes} min delay - {delay.cause}")

session.close()
```

### Maintenance Events

```python
from neo4j_client import MaintenanceEventRepository

session = conn.get_session()
maint_repo = MaintenanceEventRepository(session)

# Find all critical maintenance events for an aircraft
critical_events = maint_repo.find_by_aircraft(
    aircraft_id="AC001",
    severity="CRITICAL"
)

# Find all critical events across the fleet
all_critical = maint_repo.find_by_severity("CRITICAL")

for event in all_critical:
    print(f"{event.reported_at}: {event.fault} - {event.corrective_action}")

session.close()
```

### Creating and Updating Data

```python
from neo4j_client import Aircraft, AircraftRepository

session = conn.get_session()
aircraft_repo = AircraftRepository(session)

# Create a new aircraft
new_aircraft = Aircraft(
    aircraft_id="AC999",
    tail_number="N99999",
    icao24="A99999",
    model="Boeing 787-9",
    operator="Test Airlines",
    manufacturer="Boeing"
)
created = aircraft_repo.create(new_aircraft)

# Update the aircraft
created.operator = "Updated Airlines"
updated = aircraft_repo.update(created)

# Delete the aircraft
deleted = aircraft_repo.delete("AC999")

session.close()
```

### Systems and Components

```python
from neo4j_client import SystemRepository

session = conn.get_session()
system_repo = SystemRepository(session)

# Find all systems for an aircraft
systems = system_repo.find_by_aircraft("AC001")
for system in systems:
    print(f"System: {system.name} ({system.type})")

session.close()
```

### Airports

```python
from neo4j_client import AirportRepository

session = conn.get_session()
airport_repo = AirportRepository(session)

# Find airport by IATA code
lax = airport_repo.find_by_iata("LAX")
print(f"{lax.name} in {lax.city}, {lax.country}")

# Find all airports in a country
us_airports = airport_repo.find_by_country("United States")
print(f"Found {len(us_airports)} airports in the US")

session.close()
```

## Available Models

All models are Pydantic classes with full type hints:

- **Aircraft** - Commercial aircraft in the fleet
- **Airport** - Airports with location and codes
- **Flight** - Scheduled flight operations
- **System** - Aircraft systems (hydraulics, avionics, etc.)
- **Component** - System components
- **Sensor** - Monitoring sensors
- **Reading** - Time-series sensor readings
- **MaintenanceEvent** - Maintenance events and faults
- **Delay** - Flight delay incidents

## Available Repositories

Each repository provides query operations for its entity type:

- **AircraftRepository** - CRUD operations for aircraft
- **FlightRepository** - Flight queries and relationships
- **MaintenanceEventRepository** - Maintenance event queries
- **SystemRepository** - System queries
- **AirportRepository** - Airport queries

## Environment Variables

You can use environment variables for connection configuration:

```python
import os
from neo4j_client import Neo4jConnection

conn = Neo4jConnection(
    uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    username=os.getenv("NEO4J_USERNAME", "neo4j"),
    password=os.getenv("NEO4J_PASSWORD"),
    database=os.getenv("NEO4J_DATABASE", "neo4j")
)
```

## Testing

Run tests using pytest with testcontainers:

```bash
pytest
```

The tests use Docker to spin up a temporary Neo4j instance, so Docker must be running.

To run specific tests:

```bash
pytest tests/test_repository.py::TestAircraftRepository::test_create_aircraft
```

## What's Included

This library provides:

- ✅ Type-safe Pydantic models for all entities
- ✅ Repository pattern for clean data access
- ✅ Parameterized Cypher queries (no SQL injection risk)
- ✅ Connection management with context managers
- ✅ Comprehensive error handling
- ✅ Integration tests with testcontainers
- ✅ Modern Python packaging (PEP 621)

## What's NOT Included (Next Steps)

This is a starting point. Consider adding:

- **Async support** - AsyncIO-based operations
- **Batch operations** - Bulk inserts and updates
- **Advanced querying** - Complex graph traversals
- **Caching** - Query result caching
- **Migrations** - Schema version management
- **Monitoring** - Logging and metrics
- **CLI tools** - Command-line utilities

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation with diagrams.

## Data Model

The Neo4j database contains the following entities:

- 60 Aircraft nodes
- 36 Airport nodes
- 2,400 Flight nodes
- 240 System nodes
- 960 Component nodes
- 480 Sensor nodes
- 1,036,800 Reading nodes (time-series data)
- 900 MaintenanceEvent nodes
- 1,542 Delay nodes

For detailed data model documentation, see [DATA_MODEL.md](DATA_MODEL.md).

## Contributing

This is a starting-point library designed to be extended. Feel free to:

1. Add new repository methods for specific queries
2. Extend models with computed properties
3. Add new entity types as needed
4. Improve error handling and validation
5. Add async support

## License

MIT License

## Support

For issues or questions:
- Review the [DATA_MODEL.md](DATA_MODEL.md) for database schema details
- Check the [ARCHITECTURE.md](ARCHITECTURE.md) for design patterns
- See the test files for usage examples
