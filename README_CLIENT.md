# Neo4j Aviation Client Library

A simple, well-structured Python client library for the Neo4j aviation database. This library provides a clean starting point with Python best practices for interacting with the aviation graph database.

## Features

✅ **Pydantic Models** - Type-safe data classes for all entities  
✅ **Repository Pattern** - Clean, organized query structure  
✅ **Parameterized Queries** - Security-first approach to prevent injection  
✅ **Integration Tests** - Working examples with testcontainers  
✅ **Modern Python Packaging** - Using pyproject.toml (PEP 621)  
✅ **Type Hints** - Full type annotations throughout  
✅ **Context Managers** - Safe resource management  

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/neo4j-partners/org-mcp-demo.git
cd org-mcp-demo

# Install the package
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Requirements

- Python 3.9 or higher
- Neo4j 5.0 or higher

## Quick Start

### Basic Connection

```python
from neo4j_client import Neo4jConnection

# Create a connection
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="password",
    database="neo4j"
) as conn:
    # Use the connection
    session = conn.session()
    result = session.run("MATCH (n:Aircraft) RETURN count(n) as count")
    print(result.single()["count"])
```

### Using Repositories

```python
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft

# Connect to the database
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="password"
) as conn:
    # Create a session
    with conn.session() as session:
        # Initialize repository
        aircraft_repo = AircraftRepository(session)
        
        # Find all aircraft
        aircraft_list = aircraft_repo.find_all(limit=10)
        for aircraft in aircraft_list:
            print(f"{aircraft.tail_number}: {aircraft.model}")
```

### Creating Entities

```python
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    Aircraft
)

with Neo4jConnection(uri, username, password) as conn:
    with conn.session() as session:
        repo = AircraftRepository(session)
        
        # Create a new aircraft
        aircraft = Aircraft(
            aircraft_id="A001",
            tail_number="N12345",
            icao24="A12345",
            model="Boeing 737-800",
            operator="Test Airlines",
            manufacturer="Boeing"
        )
        
        created = repo.create(aircraft)
        print(f"Created: {created.tail_number}")
```

### Finding Entities

```python
from neo4j_client import Neo4jConnection, FlightRepository

with Neo4jConnection(uri, username, password) as conn:
    with conn.session() as session:
        flight_repo = FlightRepository(session)
        
        # Find flights by aircraft
        flights = flight_repo.find_by_aircraft("A001", limit=10)
        for flight in flights:
            print(f"{flight.flight_number}: {flight.origin} -> {flight.destination}")
```

### Complex Queries

```python
from neo4j_client import (
    Neo4jConnection,
    MaintenanceEventRepository
)

with Neo4jConnection(uri, username, password) as conn:
    with conn.session() as session:
        maint_repo = MaintenanceEventRepository(session)
        
        # Find critical maintenance events
        critical = maint_repo.find_by_severity("CRITICAL", limit=20)
        for event in critical:
            print(f"Event: {event.fault} - {event.corrective_action}")
        
        # Find maintenance events for specific aircraft
        aircraft_events = maint_repo.find_by_aircraft("A001")
        print(f"Found {len(aircraft_events)} events for aircraft A001")
```

### Working with Delays

```python
from neo4j_client import Neo4jConnection, DelayRepository

with Neo4jConnection(uri, username, password) as conn:
    with conn.session() as session:
        delay_repo = DelayRepository(session)
        
        # Find significant delays (> 30 minutes)
        delays = delay_repo.find_significant_delays(min_minutes=30, limit=50)
        for delay in delays:
            print(f"{delay.cause}: {delay.minutes} minutes")
```

## Available Models

The library includes Pydantic models for all aviation database entities:

- **Aircraft** - Commercial aircraft in the fleet
- **Airport** - Airports with location data
- **Flight** - Scheduled flight operations
- **System** - Aircraft systems (hydraulics, avionics, engines)
- **Component** - System components
- **Sensor** - Monitoring sensors
- **MaintenanceEvent** - Maintenance events and fault reports
- **Delay** - Flight delay incidents

## Available Repositories

Each entity has a corresponding repository with CRUD operations:

- **AircraftRepository**
  - `create(aircraft)`, `find_by_id(id)`, `find_by_tail_number(tail)`, `find_all()`, `update(aircraft)`, `delete(id)`
  
- **AirportRepository**
  - `create(airport)`, `find_by_id(id)`, `find_by_iata(iata)`, `find_all()`, `delete(id)`
  
- **FlightRepository**
  - `create(flight)`, `find_by_id(id)`, `find_by_aircraft(aircraft_id)`, `find_all()`, `delete(id)`
  
- **SystemRepository**
  - `create(system)`, `find_by_id(id)`, `find_by_aircraft(aircraft_id)`, `delete(id)`
  
- **ComponentRepository**
  - `create(component)`, `find_by_id(id)`, `find_by_system(system_id)`, `delete(id)`
  
- **MaintenanceEventRepository**
  - `create(event)`, `find_by_id(id)`, `find_by_aircraft(aircraft_id)`, `find_by_severity(severity)`, `delete(id)`
  
- **DelayRepository**
  - `create(delay)`, `find_by_id(id)`, `find_by_flight(flight_id)`, `find_significant_delays(min_minutes)`, `delete(id)`

## Exception Handling

The library provides custom exceptions for better error handling:

```python
from neo4j_client import (
    Neo4jConnection,
    AircraftRepository,
    NotFoundError,
    QueryError,
    ConnectionError
)

try:
    with Neo4jConnection(uri, username, password) as conn:
        with conn.session() as session:
            repo = AircraftRepository(session)
            aircraft = repo.find_by_id("A001")
            
            if aircraft:
                aircraft.operator = "New Operator"
                repo.update(aircraft)
            else:
                print("Aircraft not found")
                
except ConnectionError as e:
    print(f"Failed to connect: {e}")
except QueryError as e:
    print(f"Query failed: {e}")
except NotFoundError as e:
    print(f"Entity not found: {e}")
```

## Testing

The library includes a comprehensive test suite using pytest and testcontainers:

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

### Test Requirements

Tests use testcontainers to spin up a Neo4j instance automatically. Ensure Docker is running before executing tests.

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/neo4j-partners/org-mcp-demo.git
cd org-mcp-demo

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Code Style

The library follows Python best practices:

- Type hints on all functions and methods
- PEP 8 naming conventions
- Docstrings for all public APIs
- Single responsibility principle
- Parameterized Cypher queries for security

## Data Model

The aviation database models operational and maintenance aspects of an aviation fleet:

### Core Entities

- **Aircraft** (60 nodes) - Fleet aircraft
- **Airport** (36 nodes) - Route network
- **Flight** (2,400 nodes) - Flight operations
- **System** (240 nodes) - Aircraft systems
- **Component** (960 nodes) - System components
- **Sensor** (480 nodes) - Monitoring sensors
- **MaintenanceEvent** (900 nodes) - Maintenance records
- **Delay** (1,542 nodes) - Delay incidents

### Key Relationships

- `OPERATES_FLIGHT` - Aircraft to Flight
- `DEPARTS_FROM` / `ARRIVES_AT` - Flight to Airport
- `HAS_SYSTEM` - Aircraft to System
- `HAS_COMPONENT` - System to Component
- `HAS_SENSOR` - System to Sensor
- `HAS_EVENT` - Component to MaintenanceEvent
- `AFFECTS_AIRCRAFT` / `AFFECTS_SYSTEM` - MaintenanceEvent relationships
- `HAS_DELAY` - Flight to Delay

See [DATA_MODEL.md](DATA_MODEL.md) for complete data model documentation.

## Security Best Practices

This library follows security best practices:

✅ **Parameterized Queries** - All Cypher queries use named parameters  
✅ **No String Interpolation** - Never uses f-strings or format() for queries  
✅ **Input Validation** - Pydantic models validate all data  
✅ **Context Managers** - Safe resource cleanup  
✅ **Error Handling** - Proper exception wrapping  

## What's Included

This is a **starting point** that demonstrates:

- ✅ Clean package structure
- ✅ Pydantic models for type safety
- ✅ Repository pattern for queries
- ✅ Parameterized Cypher queries
- ✅ Integration tests with testcontainers
- ✅ Modern Python packaging
- ✅ Type hints throughout
- ✅ Basic error handling

## What's NOT Included

This is intentionally kept simple. Enterprise features not included:

- ❌ Async/await support
- ❌ ORM-like abstractions
- ❌ Complex transaction management
- ❌ Logging frameworks
- ❌ Monitoring/observability
- ❌ Caching layers
- ❌ CLI tools
- ❌ Retry/circuit breaker logic

These can be added as needed for your specific use case.

## Next Steps

To extend this client library:

1. **Add More Queries** - Extend repositories with domain-specific queries
2. **Add Relationships** - Create methods to manage relationships between entities
3. **Add Batch Operations** - Implement bulk create/update operations
4. **Add Transactions** - Wrap operations in explicit transactions
5. **Add Async Support** - Use `neo4j.AsyncGraphDatabase` for async operations
6. **Add Logging** - Integrate Python logging for debugging
7. **Add Caching** - Add caching layer for frequently accessed data
8. **Add Monitoring** - Integrate with monitoring tools

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: https://github.com/neo4j-partners/org-mcp-demo/issues
- Neo4j Community: https://community.neo4j.com/

## Acknowledgments

This library was generated using GitHub Copilot custom agents with the Neo4j MCP Cypher Server integration.
