# Neo4j Aircraft Client

A simple, type-safe Python client library for working with aircraft data in Neo4j databases.

## Features

✅ **Type Safety** - Pydantic models for all entities with validation  
✅ **Repository Pattern** - Clean query organization and reusability  
✅ **Parameterized Queries** - All Cypher queries use parameters to prevent injection  
✅ **Connection Management** - Context manager support for resource cleanup  
✅ **Error Handling** - Custom exception hierarchy for clear error reporting  
✅ **Tested** - Integration tests using testcontainers  

## Quick Start

### Installation

```bash
pip install -e .
```

For development with testing dependencies:

```bash
pip install -e ".[dev]"
```

### Basic Usage

```python
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft

# Connect to Neo4j
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your-password"
) as conn:
    # Create repository
    aircraft_repo = AircraftRepository(conn)
    
    # Create a new aircraft
    aircraft = Aircraft(
        aircraft_id="A001",
        tail_number="N12345",
        icao24="ABC123",
        model="Boeing 737-800",
        operator="Example Airlines",
        manufacturer="Boeing"
    )
    created = aircraft_repo.create(aircraft)
    print(f"Created: {created.tail_number}")
    
    # Find aircraft by ID
    found = aircraft_repo.find_by_id("A001")
    if found:
        print(f"Found: {found.model}")
    
    # Find all aircraft
    all_aircraft = aircraft_repo.find_all(limit=10)
    for a in all_aircraft:
        print(f"  - {a.tail_number}: {a.model}")
```

## What's Included

### Data Models

The library includes Pydantic models for all aircraft data entities:

- **Aircraft** - Aircraft with tail number, model, operator, manufacturer
- **Airport** - Airport with IATA/ICAO codes, location coordinates
- **Flight** - Flight operations with schedules and routes
- **System** - Aircraft systems (hydraulics, avionics, engines, etc.)
- **Component** - System components
- **Sensor** - Monitoring sensors with units
- **Reading** - Time-series sensor readings
- **MaintenanceEvent** - Maintenance events with severity and corrective actions
- **Delay** - Flight delay incidents with cause and duration

### Repositories

Three main repository classes provide CRUD operations and relationship queries:

#### AircraftRepository

```python
from neo4j_client import AircraftRepository

repo = AircraftRepository(connection)

# CRUD operations
aircraft = repo.create(aircraft_model)
aircraft = repo.find_by_id("A001")
aircraft = repo.find_by_tail_number("N12345")
all_aircraft = repo.find_all(limit=100)
updated = repo.update(aircraft_model)
deleted = repo.delete("A001")

# Relationship queries
systems = repo.get_systems("A001")
flights = repo.get_flights("A001", limit=50)
events = repo.get_maintenance_events("A001")
```

#### FlightRepository

```python
from neo4j_client import FlightRepository

repo = FlightRepository(connection)

# CRUD operations
flight = repo.create(flight_model)
flight = repo.find_by_id("F001")
flights = repo.find_by_flight_number("AA100")
all_flights = repo.find_all(limit=100)

# Relationship queries
delays = repo.get_delays("F001")
```

#### MaintenanceEventRepository

```python
from neo4j_client import MaintenanceEventRepository

repo = MaintenanceEventRepository(connection)

# CRUD operations
event = repo.create(event_model)
event = repo.find_by_id("E001")
critical = repo.find_by_severity("CRITICAL")
all_events = repo.find_all(limit=100)
```

## Usage Examples

### Working with Aircraft

```python
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft

with Neo4jConnection(uri, username, password) as conn:
    repo = AircraftRepository(conn)
    
    # Create aircraft
    aircraft = Aircraft(
        aircraft_id="A001",
        tail_number="N12345",
        icao24="ABC123",
        model="Boeing 737-800",
        operator="Example Airlines",
        manufacturer="Boeing"
    )
    repo.create(aircraft)
    
    # Find and update
    found = repo.find_by_tail_number("N12345")
    if found:
        found.operator = "Updated Airlines"
        repo.update(found)
    
    # Get related systems
    systems = repo.get_systems("A001")
    for system in systems:
        print(f"System: {system.name} ({system.type})")
    
    # Get maintenance history
    events = repo.get_maintenance_events("A001")
    for event in events:
        print(f"{event.severity}: {event.fault}")
```

### Working with Flights

```python
from neo4j_client import FlightRepository, Flight

with Neo4jConnection(uri, username, password) as conn:
    repo = FlightRepository(conn)
    
    # Create flight
    flight = Flight(
        flight_id="F001",
        flight_number="AA100",
        aircraft_id="A001",
        operator="Example Airlines",
        origin="LAX",
        destination="JFK",
        scheduled_departure="2024-01-01T10:00:00Z",
        scheduled_arrival="2024-01-01T18:00:00Z"
    )
    repo.create(flight)
    
    # Find flights by number
    flights = repo.find_by_flight_number("AA100")
    for f in flights:
        print(f"{f.origin} → {f.destination}")
    
    # Check for delays
    delays = repo.get_delays("F001")
    if delays:
        total_delay = sum(d.minutes for d in delays)
        print(f"Total delay: {total_delay} minutes")
```

### Working with Maintenance Events

```python
from neo4j_client import MaintenanceEventRepository, MaintenanceEvent

with Neo4jConnection(uri, username, password) as conn:
    repo = MaintenanceEventRepository(conn)
    
    # Create maintenance event
    event = MaintenanceEvent(
        event_id="E001",
        aircraft_id="A001",
        system_id="S001",
        component_id="C001",
        fault="Hydraulic leak detected",
        severity="CRITICAL",
        reported_at="2024-01-01T12:00:00Z",
        corrective_action="Replaced hydraulic pump"
    )
    repo.create(event)
    
    # Find critical events
    critical_events = repo.find_by_severity("CRITICAL")
    print(f"Found {len(critical_events)} critical events")
    
    for event in critical_events:
        print(f"Aircraft {event.aircraft_id}: {event.fault}")
```

### Error Handling

```python
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    ConnectionError,
    QueryError,
    NotFoundError
)

try:
    with Neo4jConnection(uri, username, password) as conn:
        repo = AircraftRepository(conn)
        aircraft = repo.find_by_id("A001")
        if not aircraft:
            print("Aircraft not found")
            
except ConnectionError as e:
    print(f"Failed to connect to Neo4j: {e}")
except QueryError as e:
    print(f"Query execution failed: {e}")
except NotFoundError as e:
    print(f"Entity not found: {e}")
```

## Testing

The library includes integration tests using testcontainers.

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=neo4j_client --cov-report=term-missing

# Run specific test file
pytest tests/test_repository.py

# Run specific test
pytest tests/test_repository.py::TestAircraftRepository::test_create_aircraft
```

### Test Structure

Tests use real Neo4j containers for accurate integration testing:

```python
def test_create_aircraft(aircraft_repo, sample_aircraft):
    """Test creating an aircraft."""
    created = aircraft_repo.create(sample_aircraft)
    assert created.aircraft_id == sample_aircraft.aircraft_id
    assert created.tail_number == sample_aircraft.tail_number
```

The `conftest.py` fixture provides:
- Session-scoped Neo4j container
- Function-scoped connection with automatic cleanup
- Sample data fixtures

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation including:

- Component design and diagrams
- Data flow visualizations
- Design patterns used
- Security considerations
- Extension points

## Security

### Parameterized Queries

All Cypher queries use named parameters to prevent injection attacks:

```python
# ✅ SAFE - Uses parameters
query = "MATCH (a:Aircraft {aircraft_id: $aircraft_id}) RETURN a"
session.run(query, aircraft_id=aircraft_id)

# ❌ UNSAFE - Never do this!
query = f"MATCH (a:Aircraft {{aircraft_id: '{aircraft_id}'}}) RETURN a"
```

### MERGE vs CREATE

The library uses `MERGE` instead of `CREATE` to avoid duplicate nodes and ensure idempotency.

### Input Validation

All inputs are validated using Pydantic models before executing queries:

```python
aircraft = Aircraft(
    aircraft_id="A001",
    tail_number="N12345",
    # Pydantic validates all fields
)
```

## Development

### Project Structure

```
neo4j_client/
├── __init__.py          # Package exports
├── models.py            # Pydantic data classes
├── repository.py        # Repository pattern
├── connection.py        # Connection management
└── exceptions.py        # Custom exceptions

tests/
├── conftest.py          # pytest fixtures
└── test_repository.py   # Integration tests
```

### Adding New Repositories

1. Add entity model to `models.py`
2. Create repository class in `repository.py`
3. Export from `__init__.py`
4. Add tests to `tests/test_repository.py`

Example:

```python
class AirportRepository:
    def __init__(self, connection: Neo4jConnection):
        self.connection = connection
    
    def find_by_iata(self, iata: str) -> Optional[Airport]:
        query = "MATCH (a:Airport {iata: $iata}) RETURN a"
        with self.connection.get_session() as session:
            result = session.run(query, iata=iata)
            record = result.single()
            if record:
                return Airport(**dict(record["a"]))
            return None
```

## Dependencies

### Core Dependencies

- `neo4j>=5.14.0` - Official Neo4j Python driver
- `pydantic>=2.0.0` - Data validation using type hints

### Development Dependencies

- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Test coverage reporting
- `testcontainers>=3.7.0` - Neo4j container for testing

## Requirements

- Python 3.9 or higher
- Neo4j 5.0 or higher
- Docker (for running tests with testcontainers)

## Next Steps

### Extending the Client

Here are some ideas for extending this client library:

1. **Add more repositories** - Create repositories for Airport, System, Component, Sensor
2. **Add relationship management** - Methods to create/delete relationships
3. **Add async support** - Async/await versions of all methods
4. **Add batch operations** - Bulk create/update methods
5. **Add query builder** - Fluent API for building complex queries
6. **Add caching** - Optional caching layer for read operations
7. **Add pagination** - Cursor-based pagination for large result sets
8. **Add transaction support** - Explicit transaction management

### Integration Examples

- Connect to your existing Neo4j database
- Build data pipelines for aircraft data ingestion
- Create analytics dashboards with real-time queries
- Implement maintenance prediction models
- Build flight tracking applications

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Support

For issues and questions:
- Open an issue in the GitHub repository
- Check the [ARCHITECTURE.md](ARCHITECTURE.md) for design details
- Review the [DATA_MODEL.md](DATA_MODEL.md) for schema information

## Acknowledgments

This client library was generated using the Neo4j MCP Cypher Server integration with GitHub Copilot custom agents. It demonstrates best practices for:

- Type-safe Python client libraries
- Repository pattern implementation
- Secure Cypher query execution
- Integration testing with testcontainers
- Modern Python packaging

See the main [README.md](README.md) for more information about the custom agent setup.
