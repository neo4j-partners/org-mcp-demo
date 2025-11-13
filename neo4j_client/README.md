# Neo4j Aircraft Data Client

A simple, well-structured Python client library for working with aircraft data in Neo4j databases. This library provides a clean starting point with Python best practices, Pydantic models for type safety, and a repository pattern for organized query access.

## Features

✅ **Pydantic Models** - Type-safe data models for all aircraft entities  
✅ **Repository Pattern** - Clean, organized query access  
✅ **Parameterized Queries** - All Cypher queries use parameters to prevent injection  
✅ **Connection Management** - Context manager support for easy resource handling  
✅ **Comprehensive Coverage** - Models for Aircraft, Flights, Systems, Sensors, Maintenance Events, and more  
✅ **Tested** - Integration tests using testcontainers  

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
    password="your-password",
    database="neo4j"
) as conn:
    # Get a session
    session = conn.get_session()
    
    # Create a repository
    aircraft_repo = AircraftRepository(session)
    
    # Find an aircraft by ID
    aircraft = aircraft_repo.find_by_id("AC001")
    if aircraft:
        print(f"Found: {aircraft.model} - {aircraft.tail_number}")
    
    # Get all flights for an aircraft
    flights = aircraft_repo.get_flights("AC001", limit=10)
    for flight in flights:
        print(f"Flight {flight.flight_number}: {flight.origin} → {flight.destination}")
    
    session.close()
```

### Working with Different Entities

#### Aircraft Operations

```python
from neo4j_client import AircraftRepository, Aircraft

with Neo4jConnection(...) as conn:
    session = conn.get_session()
    repo = AircraftRepository(session)
    
    # Create a new aircraft
    new_aircraft = Aircraft(
        aircraft_id="AC100",
        tail_number="N12345",
        icao24="ABC123",
        model="Boeing 737-800",
        operator="Example Airlines",
        manufacturer="Boeing"
    )
    repo.create(new_aircraft)
    
    # Find by tail number
    aircraft = repo.find_by_tail_number("N12345")
    
    # Get all systems for an aircraft
    systems = repo.get_systems("AC100")
    
    # Get maintenance history
    events = repo.get_maintenance_events("AC100", limit=50)
    
    session.close()
```

#### Flight Operations

```python
from neo4j_client import FlightRepository

with Neo4jConnection(...) as conn:
    session = conn.get_session()
    repo = FlightRepository(session)
    
    # Find a specific flight
    flight = repo.find_by_id("FL001")
    
    # Find all flights with a flight number
    flights = repo.find_by_flight_number("AA100", limit=20)
    
    # Find delayed flights
    delayed = repo.find_with_delays(min_minutes=30, limit=100)
    
    # Get delays for a specific flight
    delays = repo.get_delays("FL001")
    
    session.close()
```

#### System and Maintenance Operations

```python
from neo4j_client import SystemRepository, MaintenanceEventRepository

with Neo4jConnection(...) as conn:
    session = conn.get_session()
    
    # System operations
    system_repo = SystemRepository(session)
    system = system_repo.find_by_id("SYS001")
    components = system_repo.get_components("SYS001")
    sensors = system_repo.get_sensors("SYS001")
    
    # Maintenance operations
    maint_repo = MaintenanceEventRepository(session)
    critical_events = maint_repo.find_by_severity("CRITICAL", limit=100)
    
    session.close()
```

#### Sensor and Reading Operations

```python
from neo4j_client import SensorRepository

with Neo4jConnection(...) as conn:
    session = conn.get_session()
    repo = SensorRepository(session)
    
    # Find sensor
    sensor = repo.find_by_id("SENS001")
    
    # Get recent readings
    readings = repo.get_readings("SENS001", limit=1000)
    for reading in readings:
        print(f"{reading.timestamp}: {reading.value} {sensor.unit}")
    
    session.close()
```

#### Airport Operations

```python
from neo4j_client import AirportRepository

with Neo4jConnection(...) as conn:
    session = conn.get_session()
    repo = AirportRepository(session)
    
    # Find airport by IATA code
    airport = repo.find_by_iata("LAX")
    print(f"{airport.name} - {airport.city}, {airport.country}")
    
    # Get all airports
    airports = repo.find_all(limit=100)
    
    session.close()
```

## Data Models

The library includes Pydantic models for the following entities:

- **Aircraft** - Commercial aircraft with tail numbers, models, operators
- **Airport** - Airports with IATA/ICAO codes and coordinates
- **Flight** - Flight operations with schedules and routes
- **System** - Aircraft systems (hydraulics, avionics, engines, etc.)
- **Component** - System components
- **Sensor** - Monitoring sensors
- **Reading** - Time-series sensor readings
- **MaintenanceEvent** - Maintenance events and fault reports
- **Delay** - Flight delay incidents

## Available Repositories

- `AircraftRepository` - CRUD operations and queries for aircraft
- `FlightRepository` - Flight queries and delay analysis
- `SystemRepository` - System, component, and sensor queries
- `MaintenanceEventRepository` - Maintenance event queries
- `SensorRepository` - Sensor and reading queries
- `AirportRepository` - Airport queries

## Testing

Run the test suite with pytest:

```bash
pytest
```

Tests use testcontainers to spin up a Neo4j instance automatically. No manual database setup required!

## Project Structure

```
neo4j_client/
├── __init__.py          # Package exports
├── models.py            # Pydantic data models
├── repository.py        # Repository pattern for queries
├── connection.py        # Connection management
└── exceptions.py        # Custom exception classes

tests/
├── __init__.py
├── conftest.py          # Pytest fixtures with testcontainers
└── test_repository.py   # Integration tests
```

## Architecture

For detailed architecture information including system diagrams and design decisions, see [ARCHITECTURE.md](ARCHITECTURE.md).

## What's Included

This client provides:

- ✅ Type-safe Pydantic models for all entities
- ✅ Repository pattern for clean query organization
- ✅ Parameterized Cypher queries (no SQL injection risk)
- ✅ Context manager support for connections
- ✅ Comprehensive test coverage with testcontainers
- ✅ Modern Python packaging (PEP 621)
- ✅ Clear documentation and examples

## What's NOT Included (Intentionally)

This is a **starting point**, not a complete enterprise solution. It does not include:

- ❌ Async/await support
- ❌ Complex transaction management
- ❌ ORM-like abstractions
- ❌ Caching layers
- ❌ Logging frameworks
- ❌ Monitoring/observability
- ❌ CLI tools

These features can be added based on your specific needs.

## Next Steps

Here are some ways you can extend this client:

1. **Add async support** - Use `neo4j.AsyncGraphDatabase` for async operations
2. **Add caching** - Implement Redis or in-memory caching for frequently accessed data
3. **Add logging** - Integrate Python logging for query tracking
4. **Add batch operations** - Implement bulk insert/update methods
5. **Add transaction support** - Wrap operations in explicit transactions
6. **Add query builders** - Create fluent query builder interfaces
7. **Add data validation** - Extend Pydantic models with custom validators
8. **Add monitoring** - Integrate with Prometheus or similar tools

## Security Best Practices

This library follows security best practices:

- **Parameterized queries** - All Cypher queries use named parameters
- **Input validation** - Pydantic models validate all data
- **No string interpolation** - Queries are never constructed from user input
- **Connection management** - Proper resource cleanup with context managers

## Requirements

- Python 3.9+
- Neo4j 5.0+
- neo4j-driver 5.14+
- pydantic 2.0+

## License

MIT License

## Contributing

This is a starting point client library. Feel free to fork and extend it for your specific use case!

## Support

For issues with:
- **This client library** - Open an issue in this repository
- **Neo4j database** - See [Neo4j Documentation](https://neo4j.com/docs/)
- **Pydantic** - See [Pydantic Documentation](https://docs.pydantic.dev/)

## Related Documentation

- [Data Model Documentation](DATA_MODEL.md) - Detailed schema documentation
- [Architecture Documentation](ARCHITECTURE.md) - System architecture and design
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
