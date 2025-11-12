# Neo4j Aircraft Data Python Client

A clean, well-structured Python client library for working with aircraft data in Neo4j databases. This library provides a simple starting point with Python best practices, Pydantic models, and a repository pattern for organizing queries.

## Features

✅ **Pydantic Models** - Type-safe data models for all entities  
✅ **Repository Pattern** - Clean separation of data access logic  
✅ **Parameterized Queries** - Secure, injection-safe Cypher queries  
✅ **Type Hints** - Full type annotations throughout  
✅ **Integration Tests** - Working tests with testcontainers  
✅ **Modern Packaging** - PEP 621 compliant pyproject.toml  

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

# Create connection
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="password"
) as conn:
    # Initialize repository
    repo = AircraftRepository(conn)
    
    # Find an aircraft by ID
    aircraft = repo.find_by_id("AC001")
    if aircraft:
        print(f"Found: {aircraft.model} ({aircraft.tail_number})")
    
    # Find all aircraft for an operator
    aircraft_list = repo.find_by_operator("American Airlines")
    for ac in aircraft_list:
        print(f"{ac.tail_number}: {ac.model}")
```

### Working with Flights

```python
from neo4j_client import FlightRepository

with Neo4jConnection(uri, username, password) as conn:
    flight_repo = FlightRepository(conn)
    
    # Get all flights for an aircraft
    flights = flight_repo.find_by_aircraft_id("AC001")
    for flight in flights:
        print(f"{flight.flight_number}: {flight.origin} → {flight.destination}")
```

### Maintenance Events

```python
from neo4j_client import MaintenanceEventRepository

with Neo4jConnection(uri, username, password) as conn:
    maint_repo = MaintenanceEventRepository(conn)
    
    # Find critical maintenance events
    critical_events = maint_repo.find_by_severity("CRITICAL")
    for event in critical_events:
        print(f"Event {event.event_id}: {event.fault}")
    
    # Get maintenance history for an aircraft
    events = maint_repo.find_by_aircraft_id("AC001")
    for event in events:
        print(f"{event.reported_at}: {event.fault} - {event.corrective_action}")
```

### Creating and Updating Aircraft

```python
from neo4j_client import Aircraft, AircraftRepository

with Neo4jConnection(uri, username, password) as conn:
    repo = AircraftRepository(conn)
    
    # Create new aircraft
    aircraft = Aircraft(
        aircraft_id="AC999",
        tail_number="N12345",
        icao24="ABC123",
        model="Boeing 737-800",
        operator="Test Airlines",
        manufacturer="Boeing"
    )
    repo.create(aircraft)
    
    # Update existing aircraft
    aircraft.operator = "New Operator"
    repo.update(aircraft)
```

## Available Models

The library includes Pydantic models for all major entities:

- **Aircraft** - Commercial aircraft with tail numbers, models, operators
- **Airport** - Airports with IATA/ICAO codes and coordinates
- **Flight** - Scheduled flight operations
- **System** - Aircraft systems (hydraulics, avionics, engines, etc.)
- **Component** - System components
- **Sensor** - Monitoring sensors
- **Reading** - Time-series sensor readings
- **MaintenanceEvent** - Maintenance events and fault reports
- **Delay** - Flight delay incidents

## Available Repositories

### AircraftRepository

- `create(aircraft)` - Create or merge aircraft
- `find_by_id(aircraft_id)` - Find by unique ID
- `find_by_tail_number(tail_number)` - Find by tail number
- `find_all(limit)` - Get all aircraft
- `find_by_operator(operator, limit)` - Filter by operator
- `update(aircraft)` - Update existing aircraft
- `delete(aircraft_id)` - Delete aircraft

### FlightRepository

- `find_by_aircraft_id(aircraft_id, limit)` - Get flights for aircraft
- `find_by_id(flight_id)` - Find specific flight

### AirportRepository

- `find_by_iata(iata)` - Find airport by IATA code
- `find_all(limit)` - Get all airports

### SystemRepository

- `find_by_aircraft_id(aircraft_id)` - Get systems for aircraft

### MaintenanceEventRepository

- `find_by_aircraft_id(aircraft_id, limit)` - Get maintenance events for aircraft
- `find_by_severity(severity, limit)` - Filter by severity level

## Testing

The library includes comprehensive tests using pytest and testcontainers:

```bash
pytest
```

Tests automatically spin up a Neo4j container, run integration tests, and clean up.

## Environment Configuration

Set these environment variables for production use:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
export NEO4J_DATABASE="neo4j"
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation including:
- System design overview
- Component diagrams
- Data flow
- Query patterns

## What's Included

This is a **starting point** focused on:

- ✅ Clean, readable code with type hints
- ✅ Pydantic models for validation
- ✅ Repository pattern for queries
- ✅ Parameterized Cypher queries (security)
- ✅ Basic CRUD operations
- ✅ Working integration tests
- ✅ Modern Python packaging

## What's Not Included (Yet)

This library focuses on simplicity. Consider adding:

- Async/await support
- Connection pooling configuration
- Advanced transaction management
- Retry logic and circuit breakers
- Caching layers
- CLI tools
- Logging frameworks
- Monitoring/observability

## Next Steps

To extend this library:

1. **Add more repositories** - Create repositories for Component, Sensor, Reading, Delay entities
2. **Add complex queries** - Implement graph traversals, aggregations, recommendations
3. **Add batch operations** - Bulk insert/update methods
4. **Add relationship methods** - Link aircraft to flights, systems, etc.
5. **Add async support** - Use neo4j async driver if needed
6. **Add validation** - Enhanced Pydantic validators for business rules
7. **Add monitoring** - Integrate with your logging/metrics system

## Security

This library follows security best practices:

- ✅ **Parameterized queries** - All Cypher queries use parameters, never string formatting
- ✅ **MERGE over CREATE** - Prevents accidental duplicates
- ✅ **Pydantic validation** - Input validation before database operations
- ✅ **Error handling** - Custom exceptions for different error types

## Contributing

This is a demonstration library. For production use, consider:

- Adding comprehensive error handling
- Implementing connection pooling
- Adding query performance monitoring
- Implementing audit logging
- Adding schema validation

## License

MIT

## Support

This library is provided as a starting point for developers working with aircraft data in Neo4j. Extend and customize it for your specific needs.
