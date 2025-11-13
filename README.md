# Neo4j Aircraft Data Client

A Python client library for working with aircraft data in Neo4j. This library provides a clean, type-safe interface to query and manage aviation-related data including aircraft, flights, airports, maintenance events, and more.

## Features

✅ **Type-safe models** - Pydantic models with full type hints  
✅ **Repository pattern** - Clean separation of data access logic  
✅ **Parameterized queries** - Protection against injection attacks  
✅ **Connection management** - Context manager support for safe resource handling  
✅ **Comprehensive testing** - Integration tests using testcontainers  
✅ **Modern Python** - Built for Python 3.9+ with latest best practices  

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

### Running the Example

A comprehensive usage example is provided in `examples/usage_example.py`:

```bash
python examples/usage_example.py
```

This example demonstrates:
- Querying aircraft and their properties
- Finding flights for specific aircraft
- Searching flights by route
- Querying airports
- Finding maintenance events
- Creating new aircraft (with cleanup)

### Basic Usage

```python
from neo4j_client import Neo4jConnection, AircraftRepository, FlightRepository

# Create connection
connection = Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your-password",
    database="neo4j"
)

# Use context manager for automatic cleanup
with connection:
    session = connection.get_session()
    
    # Create repository instances
    aircraft_repo = AircraftRepository(session)
    flight_repo = FlightRepository(session)
    
    # Find an aircraft
    aircraft = aircraft_repo.find_by_tail_number("N12345")
    if aircraft:
        print(f"Found: {aircraft.model} operated by {aircraft.operator}")
        
        # Get flights for this aircraft
        flights = flight_repo.find_by_aircraft(aircraft.aircraft_id, limit=10)
        print(f"Recent flights: {len(flights)}")
    
    session.close()
```

### Creating New Aircraft

```python
from neo4j_client import Aircraft, AircraftRepository, Neo4jConnection

aircraft = Aircraft(
    aircraft_id="AC001",
    tail_number="N54321",
    icao24="A54321",
    model="Boeing 737-800",
    operator="Example Airlines",
    manufacturer="Boeing"
)

with Neo4jConnection(uri, username, password) as connection:
    session = connection.get_session()
    repo = AircraftRepository(session)
    
    created = repo.create(aircraft)
    print(f"Created aircraft: {created.aircraft_id}")
    
    session.close()
```

### Querying Flights by Route

```python
from neo4j_client import FlightRepository, Neo4jConnection

with Neo4jConnection(uri, username, password) as connection:
    session = connection.get_session()
    flight_repo = FlightRepository(session)
    
    # Find all flights from LAX to JFK
    flights = flight_repo.find_by_route("LAX", "JFK", limit=50)
    
    for flight in flights:
        print(f"{flight.flight_number}: {flight.scheduled_departure}")
    
    session.close()
```

### Finding Maintenance Events

```python
from neo4j_client import MaintenanceEventRepository, Neo4jConnection

with Neo4jConnection(uri, username, password) as connection:
    session = connection.get_session()
    maintenance_repo = MaintenanceEventRepository(session)
    
    # Find critical maintenance events
    critical_events = maintenance_repo.find_critical_events(limit=20)
    
    for event in critical_events:
        print(f"Event {event.event_id}: {event.fault}")
        print(f"  Severity: {event.severity}")
        print(f"  Action: {event.corrective_action}")
    
    session.close()
```

## Available Models

The library includes Pydantic models for all major entities:

- **Aircraft** - Commercial aircraft in the fleet
- **Airport** - Airports with location data
- **Flight** - Scheduled flight operations
- **System** - Aircraft systems (hydraulics, avionics, etc.)
- **Component** - System components
- **Sensor** - Monitoring sensors
- **Reading** - Time-series sensor readings
- **MaintenanceEvent** - Maintenance events and fault reports
- **Delay** - Flight delay incidents

See the [DATA_MODEL.md](DATA_MODEL.md) for complete schema documentation.

## Available Repositories

### AircraftRepository

```python
# CRUD operations
aircraft = repo.create(aircraft_model)
aircraft = repo.find_by_id(aircraft_id)
aircraft = repo.find_by_tail_number(tail_number)
aircraft_list = repo.find_all(limit=100)
aircraft_list = repo.find_by_operator(operator, limit=100)
success = repo.delete(aircraft_id)
```

### FlightRepository

```python
# Query operations
flight = repo.find_by_id(flight_id)
flights = repo.find_by_aircraft(aircraft_id, limit=100)
flights = repo.find_by_route(origin, destination, limit=100)
flights = repo.find_with_delays(min_delay_minutes=30, limit=100)
```

### SystemRepository

```python
# Query operations
system = repo.find_by_id(system_id)
systems = repo.find_by_aircraft(aircraft_id)
```

### MaintenanceEventRepository

```python
# Query operations
events = repo.find_by_aircraft(aircraft_id, limit=100)
events = repo.find_by_severity(severity, limit=100)
events = repo.find_critical_events(limit=100)
```

### AirportRepository

```python
# Query operations
airport = repo.find_by_iata(iata_code)
airport = repo.find_by_icao(icao_code)
airports = repo.find_all(limit=100)
```

## Testing

This library uses pytest with testcontainers for integration testing.

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=neo4j_client --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_repository.py
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation including diagrams.

## Environment Variables

For production use, configure connection using environment variables:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
export NEO4J_DATABASE="neo4j"
```

```python
import os
from neo4j_client import Neo4jConnection

connection = Neo4jConnection(
    uri=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database=os.getenv("NEO4J_DATABASE", "neo4j")
)
```

## Error Handling

The library provides custom exceptions for better error handling:

```python
from neo4j_client import (
    Neo4jClientError,      # Base exception
    ConnectionError,       # Connection failures
    QueryError,            # Query execution failures
    NotFoundError,         # Entity not found
)

try:
    aircraft = repo.find_by_id("AC001")
except ConnectionError as e:
    print(f"Failed to connect: {e}")
except QueryError as e:
    print(f"Query failed: {e}")
except Neo4jClientError as e:
    print(f"Client error: {e}")
```

## Security

This library follows security best practices:

- ✅ All queries use parameterization (no string interpolation)
- ✅ Input validation using Pydantic models
- ✅ No raw Cypher query construction from user input
- ✅ Connection credentials never logged or exposed

## Next Steps

This is a starting point for working with aircraft data in Neo4j. You can extend it by:

1. **Add more repository methods** - Custom queries for your specific use cases
2. **Implement write operations** - Update methods for flights, systems, etc.
3. **Add relationship management** - Methods to create/manage relationships
4. **Enhance error handling** - More granular exception types
5. **Add async support** - For high-performance applications
6. **Implement caching** - For frequently accessed data
7. **Add monitoring** - Logging and metrics collection

## Contributing

Contributions are welcome! This library is designed to be simple and extensible.

## License

MIT License

## Related Documentation

- [Neo4j Python Driver Documentation](https://neo4j.com/docs/python-manual/current/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Aircraft Data Model](DATA_MODEL.md)
- [Architecture Documentation](ARCHITECTURE.md)
