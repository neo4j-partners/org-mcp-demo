# Neo4j Aviation Client

A simple, high-quality Python client library for interacting with a Neo4j aviation/aircraft maintenance database. This client provides a clean, type-safe interface using Pydantic models and the repository pattern.

## Features

✅ **Pydantic models** for type safety and validation  
✅ **Repository pattern** for clean query organization  
✅ **Parameterized Cypher queries** to prevent injection attacks  
✅ **Context managers** for connection management  
✅ **Comprehensive type hints** throughout the codebase  
✅ **Integration tests** using testcontainers  
✅ **Modern Python packaging** with pyproject.toml  

## Installation

### From Source

```bash
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### Complete Example

For a complete working example, see [examples/basic_usage.py](examples/basic_usage.py) which demonstrates:
- Connecting to the database
- Querying aircraft, airports, and flights
- Finding maintenance events
- Using multiple repositories

See [examples/README.md](examples/README.md) for instructions on running the examples.

### Basic Usage

```python
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft

# Create connection
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="password"
) as conn:
    # Get a session
    session = conn.get_session()
    
    # Create repository
    aircraft_repo = AircraftRepository(session)
    
    # Create an aircraft
    aircraft = Aircraft(
        aircraft_id="AC001",
        tail_number="N12345",
        icao24="A12345",
        model="Boeing 737-800",
        operator="Example Airlines",
        manufacturer="Boeing"
    )
    
    created = aircraft_repo.create(aircraft)
    print(f"Created aircraft: {created.tail_number}")
    
    # Find aircraft by ID
    found = aircraft_repo.find_by_id("AC001")
    if found:
        print(f"Found: {found.model}")
    
    # Find all aircraft
    all_aircraft = aircraft_repo.find_all(limit=10)
    for ac in all_aircraft:
        print(f"- {ac.tail_number}: {ac.model}")
    
    session.close()
```

### Working with Airports

```python
from neo4j_client import AirportRepository, Airport

session = conn.get_session()
airport_repo = AirportRepository(session)

# Create an airport
airport = Airport(
    airport_id="LAX001",
    iata="LAX",
    icao="KLAX",
    name="Los Angeles International Airport",
    city="Los Angeles",
    country="USA",
    lat=33.9425,
    lon=-118.4081
)

airport_repo.create(airport)

# Find by IATA code
lax = airport_repo.find_by_iata("LAX")
print(f"{lax.name} is in {lax.city}")

session.close()
```

### Working with Flights

```python
from neo4j_client import FlightRepository, Flight

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
    scheduled_departure="2024-01-01T10:00:00",
    scheduled_arrival="2024-01-01T18:00:00"
)

flight_repo.create(flight)

# Find flights by aircraft
flights = flight_repo.find_by_aircraft("AC001")
for f in flights:
    print(f"Flight {f.flight_number}: {f.origin} -> {f.destination}")

session.close()
```

### Working with Maintenance Events

```python
from neo4j_client import MaintenanceEventRepository, MaintenanceEvent

session = conn.get_session()
event_repo = MaintenanceEventRepository(session)

# Create a maintenance event
event = MaintenanceEvent(
    event_id="ME001",
    aircraft_id="AC001",
    system_id="SYS001",
    component_id="COMP001",
    fault="Engine temperature high",
    severity="CRITICAL",
    reported_at="2024-01-01T12:00:00",
    corrective_action="Replaced temperature sensor"
)

event_repo.create(event)

# Find critical events
critical_events = event_repo.find_by_severity("CRITICAL")
for e in critical_events:
    print(f"Event {e.event_id}: {e.fault}")

# Find events for an aircraft
aircraft_events = event_repo.find_by_aircraft("AC001")
print(f"Found {len(aircraft_events)} events for aircraft AC001")

session.close()
```

## Database Schema

The client supports the following entities:

### Core Entities

- **Aircraft** - Commercial aircraft with tail numbers, models, and operators
- **Airport** - Airports with IATA/ICAO codes and geographic coordinates
- **Flight** - Flight operations with schedules and routes
- **System** - Aircraft systems (e.g., hydraulics, avionics)
- **Component** - Components within systems
- **Sensor** - Sensors monitoring systems and components
- **Reading** - Time-series sensor readings
- **MaintenanceEvent** - Maintenance and fault records
- **Delay** - Flight delay records with causes

### Relationships

- Aircraft → System (HAS_SYSTEM)
- Aircraft → Flight (OPERATES_FLIGHT)
- Flight → Airport (DEPARTS_FROM, ARRIVES_AT)
- Flight → Delay (HAS_DELAY)
- System → Component (HAS_COMPONENT)
- System → Sensor (HAS_SENSOR)
- Component → MaintenanceEvent (HAS_EVENT)
- MaintenanceEvent → Aircraft (AFFECTS_AIRCRAFT)
- MaintenanceEvent → System (AFFECTS_SYSTEM)

For detailed schema diagrams, see [docs/DATA_MODEL.md](docs/DATA_MODEL.md).

## Available Repositories

Each entity has a corresponding repository with CRUD operations:

- `AircraftRepository` - Aircraft operations
- `AirportRepository` - Airport operations
- `FlightRepository` - Flight operations
- `SystemRepository` - System operations
- `SensorRepository` - Sensor operations
- `ReadingRepository` - Reading operations
- `MaintenanceEventRepository` - Maintenance event operations
- `DelayRepository` - Delay operations

### Common Repository Methods

All repositories provide:
- `create(entity)` - Create a new entity (uses MERGE to avoid duplicates)
- `find_by_id(id)` - Find entity by ID
- `find_all(limit)` - Find all entities (with optional limit)

Specific repositories have additional methods like:
- `find_by_tail_number()` - For aircraft
- `find_by_iata()` - For airports
- `find_by_aircraft()` - For flights, events, etc.
- `find_by_severity()` - For maintenance events

## Running Tests

The test suite uses testcontainers to spin up a Neo4j instance automatically:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=neo4j_client --cov-report=html
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture diagrams and design decisions.

## What's Included

This client provides:

- ✅ Clean, typed interfaces for all entities
- ✅ Safe, parameterized queries
- ✅ Basic CRUD operations
- ✅ Connection management with context managers
- ✅ Comprehensive test coverage
- ✅ Modern Python packaging

## What's NOT Included (Yet)

This is a starting point. You may want to add:

- ❌ Async/await support
- ❌ Transaction management helpers
- ❌ Complex relationship traversals
- ❌ Caching layer
- ❌ Retry/circuit breaker patterns
- ❌ Logging framework integration
- ❌ CLI tools

## Security Best Practices

This client follows security best practices:

1. **Parameterized queries** - All Cypher queries use named parameters to prevent injection
2. **MERGE over CREATE** - Uses MERGE where appropriate to avoid duplicate nodes
3. **Input validation** - Pydantic models validate all inputs
4. **Connection security** - Supports secure bolt+s:// connections

## Next Steps

To extend this client:

1. **Add relationship management** - Create methods to link entities (e.g., assign flight to aircraft)
2. **Add graph traversals** - Methods to navigate relationships (e.g., get all sensors for an aircraft)
3. **Add aggregations** - Statistics and analytics queries
4. **Add batch operations** - Bulk create/update methods
5. **Add async support** - Use neo4j async driver for concurrent operations
6. **Add caching** - Cache frequently accessed data

## Requirements

- Python 3.9+
- Neo4j 5.0+

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
