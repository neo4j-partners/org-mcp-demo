# Neo4j Aviation Client Library

A Python client library for the Neo4j aviation database, providing a clean, type-safe interface with Pydantic models and the repository pattern.

## Features

✅ **Type Safety** - Pydantic models for all entities with full type hints  
✅ **Repository Pattern** - Clean separation of concerns with CRUD operations  
✅ **Parameterized Queries** - All Cypher queries use parameters to prevent injection  
✅ **Connection Management** - Context manager support for automatic cleanup  
✅ **Integration Tests** - Working tests with testcontainers  
✅ **Modern Packaging** - PEP 621 compliant pyproject.toml  

## Installation

```bash
# Install from source
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft

# Create connection
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your-password"
) as conn:
    # Get a session
    session = conn.get_session()
    
    # Create repository
    repo = AircraftRepository(session)
    
    # Create an aircraft
    aircraft = Aircraft(
        aircraft_id="AC001",
        tail_number="N12345",
        icao24="ABC123",
        model="Boeing 737-800",
        operator="Example Airlines",
        manufacturer="Boeing"
    )
    created = repo.create(aircraft)
    
    # Find aircraft
    found = repo.find_by_id("AC001")
    print(f"Found: {found.tail_number} - {found.model}")
    
    # Update aircraft
    found.operator = "New Airlines"
    updated = repo.update(found)
    
    # List all aircraft
    all_aircraft = repo.find_all(limit=50)
    for ac in all_aircraft:
        print(f"{ac.tail_number}: {ac.model}")
    
    session.close()
```

### Working with Airports

```python
from neo4j_client import Neo4jConnection, AirportRepository, Airport

with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your-password"
) as conn:
    session = conn.get_session()
    repo = AirportRepository(session)
    
    # Create airport
    airport = Airport(
        airport_id="AP001",
        iata="LAX",
        icao="KLAX",
        name="Los Angeles International Airport",
        city="Los Angeles",
        country="USA",
        lat=33.9425,
        lon=-118.4081
    )
    repo.create(airport)
    
    # Find by IATA code
    lax = repo.find_by_iata("LAX")
    print(f"{lax.name} at ({lax.lat}, {lax.lon})")
    
    session.close()
```

### Working with Flights

```python
from neo4j_client import Neo4jConnection, FlightRepository, Flight

with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your-password"
) as conn:
    session = conn.get_session()
    repo = FlightRepository(session)
    
    # Create flight
    flight = Flight(
        flight_id="FL001",
        flight_number="AA100",
        aircraft_id="AC001",
        operator="American Airlines",
        origin="LAX",
        destination="JFK",
        scheduled_departure="2024-01-15T08:00:00Z",
        scheduled_arrival="2024-01-15T16:30:00Z"
    )
    repo.create(flight)
    
    # Find flights by aircraft (requires OPERATES_FLIGHT relationship)
    flights = repo.find_by_aircraft("AC001", limit=10)
    for f in flights:
        print(f"{f.flight_number}: {f.origin} → {f.destination}")
    
    # Find by flight number
    aa_flights = repo.find_by_flight_number("AA100", limit=5)
    
    session.close()
```

### Working with Maintenance Events

```python
from neo4j_client import Neo4jConnection, MaintenanceEventRepository, MaintenanceEvent

with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your-password"
) as conn:
    session = conn.get_session()
    repo = MaintenanceEventRepository(session)
    
    # Create maintenance event
    event = MaintenanceEvent(
        event_id="ME001",
        aircraft_id="AC001",
        system_id="SYS001",
        component_id="COMP001",
        fault="Hydraulic leak detected",
        severity="CRITICAL",
        reported_at="2024-01-15T10:30:00Z",
        corrective_action="Replaced hydraulic seal and tested system"
    )
    repo.create(event)
    
    # Find critical events
    critical = repo.find_by_severity("CRITICAL", limit=20)
    for e in critical:
        print(f"{e.reported_at}: {e.fault}")
    
    # Find events for specific aircraft (requires AFFECTS_AIRCRAFT relationship)
    aircraft_events = repo.find_by_aircraft("AC001", limit=10)
    
    session.close()
```

## Environment Configuration

Set up your Neo4j connection using environment variables:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
export NEO4J_DATABASE="neo4j"
```

Then use them in your code:

```python
import os
from neo4j_client import Neo4jConnection

conn = Neo4jConnection(
    uri=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database=os.getenv("NEO4J_DATABASE", "neo4j")
)
```

## Available Models

All models are Pydantic `BaseModel` subclasses with full type hints:

- **Aircraft** - Commercial aircraft in the fleet
- **Airport** - Airports with location and codes
- **Flight** - Scheduled flight operations
- **System** - Aircraft systems (hydraulics, avionics, etc.)
- **Component** - Components within systems
- **Sensor** - Sensors monitoring systems
- **Reading** - Time-series sensor readings
- **MaintenanceEvent** - Maintenance events and fault reports
- **Delay** - Flight delay incidents

## Available Repositories

Repository classes provide CRUD operations with parameterized Cypher queries:

- **AircraftRepository** - CRUD for aircraft
  - `create()`, `find_by_id()`, `find_by_tail_number()`, `find_all()`, `update()`, `delete()`
  
- **AirportRepository** - CRUD for airports
  - `create()`, `find_by_id()`, `find_by_iata()`, `find_all()`, `update()`, `delete()`
  
- **FlightRepository** - CRUD for flights
  - `create()`, `find_by_id()`, `find_by_flight_number()`, `find_by_aircraft()`, `find_all()`, `update()`, `delete()`
  
- **MaintenanceEventRepository** - CRUD for maintenance events
  - `create()`, `find_by_id()`, `find_by_aircraft()`, `find_by_severity()`, `find_all()`, `update()`, `delete()`

## Testing

Run tests using pytest with testcontainers:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=neo4j_client --cov-report=html

# Run specific test file
pytest tests/test_repository.py

# Run specific test
pytest tests/test_repository.py::TestAircraftRepository::test_create_aircraft
```

**Note:** Tests use testcontainers to spin up a temporary Neo4j instance. Docker must be running on your system.

## Error Handling

The library provides custom exceptions for different error scenarios:

```python
from neo4j_client import Neo4jConnection, AircraftRepository
from neo4j_client.exceptions import ConnectionError, QueryError, NotFoundError

try:
    with Neo4jConnection(uri="bolt://invalid:7687", username="neo4j", password="pass") as conn:
        session = conn.get_session()
except ConnectionError as e:
    print(f"Failed to connect: {e}")

try:
    repo = AircraftRepository(session)
    aircraft = repo.find_by_id("NONEXISTENT")
    if aircraft is None:
        print("Aircraft not found")
except QueryError as e:
    print(f"Query failed: {e}")
```

## What's Included

✅ Connection management with context manager support  
✅ Pydantic models for 9 entity types  
✅ Repository pattern for 4 main entities  
✅ Parameterized Cypher queries (no SQL injection risk)  
✅ Type hints throughout the codebase  
✅ Integration tests with testcontainers  
✅ Modern Python packaging (PEP 621)  
✅ Comprehensive error handling  

## What's Not Included (Future Extensions)

This is a **starting point** library. Consider adding:

- ❌ Async/await support (use `neo4j-driver` async features)
- ❌ Advanced transaction management
- ❌ Retry logic and circuit breakers
- ❌ Logging and monitoring integration
- ❌ Caching layer
- ❌ ORM-like relationship traversal
- ❌ Migration tools
- ❌ CLI tools
- ❌ Repositories for all 9 entities (only 4 included)

## Architecture

### Repository Pattern

Each repository encapsulates database operations for a specific entity type:

```
User Code → Repository → Neo4j Session → Database
              ↓
         Pydantic Model (validation)
```

### Security

All queries use **parameterized Cypher** to prevent injection attacks:

```python
# ✅ SAFE - Uses parameters
query = "MATCH (a:Aircraft {aircraft_id: $aircraft_id}) RETURN a"
result = session.run(query, aircraft_id=user_input)

# ❌ UNSAFE - String interpolation (never do this!)
query = f"MATCH (a:Aircraft {{aircraft_id: '{user_input}'}}) RETURN a"
```

## Contributing

This library is a starting point. To extend it:

1. Add new models in `neo4j_client/models.py`
2. Create corresponding repositories in `neo4j_client/repository.py`
3. Export them in `neo4j_client/__init__.py`
4. Add tests in `tests/test_repository.py`

## License

MIT License

## Database Schema

This client is designed for the Neo4j aviation database schema with:

- **9 Node Types**: Aircraft, Airport, Flight, System, Component, Sensor, Reading, MaintenanceEvent, Delay
- **9 Relationship Types**: OPERATES_FLIGHT, DEPARTS_FROM, ARRIVES_AT, HAS_SYSTEM, HAS_COMPONENT, HAS_SENSOR, HAS_EVENT, AFFECTS_AIRCRAFT, AFFECTS_SYSTEM, HAS_DELAY

See [DATA_MODEL.md](DATA_MODEL.md) for complete schema documentation.

## Next Steps

1. **Add more repositories** - Create repositories for System, Component, Sensor, Reading, and Delay entities
2. **Add relationship helpers** - Methods to create/query relationships between entities
3. **Add bulk operations** - Batch create/update/delete methods
4. **Add query builders** - Fluent API for complex queries
5. **Add async support** - Use `neo4j.AsyncGraphDatabase` for async operations
6. **Add logging** - Integrate Python logging for debugging
7. **Add caching** - Cache frequently accessed data
8. **Add migrations** - Schema migration tools

## Support

For issues and questions:
- Check the [DATA_MODEL.md](DATA_MODEL.md) for schema details
- Review test examples in `tests/test_repository.py`
- See Neo4j driver docs: https://neo4j.com/docs/python-manual/current/
