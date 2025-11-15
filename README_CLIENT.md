# Neo4j Aviation Client Library

A high-quality Python client library for interacting with Neo4j aviation databases. Built with modern Python best practices including Pydantic models, type hints, and the repository pattern.

## Features

✅ **Type-Safe Models** - Pydantic models for all entities with full type hints  
✅ **Repository Pattern** - Clean, organized query structure  
✅ **Parameterized Queries** - Secure, injection-safe Cypher queries  
✅ **Connection Management** - Context manager support for clean resource handling  
✅ **Comprehensive Tests** - Integration tests using testcontainers  
✅ **Modern Packaging** - PEP 621 compliant pyproject.toml  

## Installation

### From Source

```bash
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft

# Connect to Neo4j
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your-password"
) as conn:
    # Get a session
    session = conn.get_session()
    
    # Create a repository
    aircraft_repo = AircraftRepository(session)
    
    # Create a new aircraft
    aircraft = Aircraft(
        aircraft_id="AC001",
        tail_number="N12345",
        icao24="A12345",
        model="Boeing 737-800",
        operator="Example Airlines",
        manufacturer="Boeing"
    )
    aircraft_repo.create(aircraft)
    
    # Find aircraft by ID
    found = aircraft_repo.find_by_id("AC001")
    print(f"Found: {found.model}")
    
    # Find all aircraft
    all_aircraft = aircraft_repo.find_all(limit=10)
    for a in all_aircraft:
        print(f"{a.tail_number}: {a.model}")
```

### Working with Flights

```python
from neo4j_client import FlightRepository, Flight

with Neo4jConnection(uri, username, password) as conn:
    session = conn.get_session()
    flight_repo = FlightRepository(session)
    
    # Create a flight
    flight = Flight(
        flight_id="FL001",
        flight_number="AA100",
        aircraft_id="AC001",
        operator="American Airlines",
        origin="LAX",
        destination="JFK",
        scheduled_departure="2024-01-01T10:00:00Z",
        scheduled_arrival="2024-01-01T18:00:00Z"
    )
    flight_repo.create(flight)
    
    # Find flights by aircraft
    flights = flight_repo.find_by_aircraft("AC001", limit=100)
    for f in flights:
        print(f"{f.flight_number}: {f.origin} → {f.destination}")
```

### Maintenance Events

```python
from neo4j_client import MaintenanceEventRepository, MaintenanceEvent

with Neo4jConnection(uri, username, password) as conn:
    session = conn.get_session()
    maint_repo = MaintenanceEventRepository(session)
    
    # Create a maintenance event
    event = MaintenanceEvent(
        event_id="ME001",
        aircraft_id="AC001",
        system_id="SYS001",
        component_id="COMP001",
        fault="Hydraulic pressure low",
        severity="WARNING",
        reported_at="2024-01-01T12:00:00Z",
        corrective_action="Replaced hydraulic pump"
    )
    maint_repo.create(event)
    
    # Find critical maintenance events
    critical = maint_repo.find_by_severity("CRITICAL", limit=50)
    for e in critical:
        print(f"{e.event_id}: {e.fault}")
    
    # Find events for specific aircraft
    aircraft_events = maint_repo.find_by_aircraft("AC001")
    for e in aircraft_events:
        print(f"{e.reported_at}: {e.fault}")
```

### Airport Operations

```python
from neo4j_client import AirportRepository, Airport

with Neo4jConnection(uri, username, password) as conn:
    session = conn.get_session()
    airport_repo = AirportRepository(session)
    
    # Create an airport
    airport = Airport(
        airport_id="AP001",
        iata="LAX",
        icao="KLAX",
        name="Los Angeles International",
        city="Los Angeles",
        country="USA",
        lat=33.9425,
        lon=-118.408
    )
    airport_repo.create(airport)
    
    # Find by IATA code
    lax = airport_repo.find_by_iata("LAX")
    print(f"{lax.name}: ({lax.lat}, {lax.lon})")
```

## Available Models

All models are Pydantic-based with full type hints:

- **Aircraft** - Commercial aircraft in the fleet
- **Airport** - Airports with location data
- **Flight** - Scheduled flight operations
- **System** - Aircraft systems (hydraulics, avionics, etc.)
- **Component** - System components
- **Sensor** - Monitoring sensors
- **Reading** - Time-series sensor readings
- **MaintenanceEvent** - Maintenance records and fault reports
- **Delay** - Flight delay incidents

## Available Repositories

- **AircraftRepository** - CRUD operations for aircraft
  - `create(aircraft)` - Create new aircraft
  - `find_by_id(aircraft_id)` - Find by ID
  - `find_by_tail_number(tail_number)` - Find by tail number
  - `find_all(limit)` - Find all aircraft
  - `update(aircraft)` - Update existing aircraft
  - `delete(aircraft_id)` - Delete aircraft

- **FlightRepository** - Operations for flights
  - `create(flight)` - Create new flight
  - `find_by_id(flight_id)` - Find by ID
  - `find_by_aircraft(aircraft_id, limit)` - Find flights for aircraft
  - `find_all(limit)` - Find all flights
  - `delete(flight_id)` - Delete flight

- **MaintenanceEventRepository** - Maintenance event operations
  - `create(event)` - Create new event
  - `find_by_id(event_id)` - Find by ID
  - `find_by_aircraft(aircraft_id, limit)` - Find events for aircraft
  - `find_by_severity(severity, limit)` - Find by severity level

- **AirportRepository** - Airport operations
  - `create(airport)` - Create new airport
  - `find_by_id(airport_id)` - Find by ID
  - `find_by_iata(iata)` - Find by IATA code
  - `find_all(limit)` - Find all airports

## Error Handling

The client provides custom exceptions for different error scenarios:

```python
from neo4j_client import NotFoundError, QueryError, ConnectionError

try:
    aircraft = aircraft_repo.find_by_id("NONEXISTENT")
    if aircraft is None:
        print("Aircraft not found")
except QueryError as e:
    print(f"Query failed: {e}")
except ConnectionError as e:
    print(f"Connection failed: {e}")
```

## Testing

The library includes comprehensive integration tests using testcontainers:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=neo4j_client --cov-report=html

# Run specific test file
pytest tests/test_repository.py

# Run specific test
pytest tests/test_repository.py::TestAircraftRepository::test_create_aircraft
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Pytest fixtures with testcontainers
└── test_repository.py   # Integration tests for repositories
```

## Configuration

### Environment Variables

You can use environment variables for configuration:

```python
import os
from neo4j_client import Neo4jConnection

uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
username = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD")
database = os.getenv("NEO4J_DATABASE", "neo4j")

with Neo4jConnection(uri, username, password, database) as conn:
    # Your code here
    pass
```

## Security

The client follows security best practices:

✅ **Parameterized Queries** - All Cypher queries use named parameters to prevent injection attacks  
✅ **No String Interpolation** - Never constructs queries from user input directly  
✅ **MERGE Operations** - Uses `MERGE` instead of `CREATE` to avoid duplicate nodes  
✅ **Input Validation** - Pydantic models validate all data before queries  
✅ **Error Handling** - Catches and wraps Neo4j driver exceptions  

## Project Structure

```
neo4j_client/
├── __init__.py          # Package exports
├── models.py            # Pydantic data models
├── repository.py        # Repository pattern implementations
├── connection.py        # Connection management
└── exceptions.py        # Custom exception classes

tests/
├── __init__.py
├── conftest.py          # Pytest fixtures
└── test_repository.py   # Integration tests

pyproject.toml           # Modern Python packaging
README_CLIENT.md         # This file
```

## Dependencies

### Core Dependencies
- `neo4j>=5.0.0` - Official Neo4j Python driver
- `pydantic>=2.0.0` - Data validation and models

### Development Dependencies
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `testcontainers>=3.7.0` - Docker-based test fixtures

## Next Steps

This client provides a solid foundation. Consider extending it with:

- **Additional Repositories** - System, Component, Sensor repositories
- **Relationship Management** - Methods to create relationships between entities
- **Bulk Operations** - Batch create/update for better performance
- **Query Builders** - Flexible query construction for complex searches
- **Async Support** - AsyncIO support for concurrent operations
- **Caching Layer** - Optional caching for frequently accessed data
- **Transaction Support** - Multi-operation transactions with rollback
- **Schema Migrations** - Version control for database schema

## Contributing

This is a starting point client library. Feel free to extend and customize based on your needs.

## License

MIT License - See LICENSE file for details

## Links

- [Neo4j Python Driver Documentation](https://neo4j.com/docs/python-manual/current/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Testcontainers Python](https://testcontainers-python.readthedocs.io/)
