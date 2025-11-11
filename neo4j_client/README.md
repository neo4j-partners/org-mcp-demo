# Neo4j Aviation Database - Python Client Library

A simple, high-quality Python client library for interacting with the Neo4j aviation database. This library provides type-safe models, clean repository patterns, and parameterized queries following Python best practices.

## Features

✅ **Pydantic models** for type safety and validation  
✅ **Repository pattern** for clean query organization  
✅ **Parameterized Cypher queries** to prevent injection attacks  
✅ **Type hints** throughout the codebase  
✅ **Context managers** for connection management  
✅ **Integration tests** using testcontainers  
✅ **Modern Python packaging** with pyproject.toml

## Installation

```bash
pip install -e .
```

For development (includes pytest and testcontainers):

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft

# Create a connection
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password",
    database="neo4j"
) as connection:
    # Get a session and create a repository
    with connection.get_session() as session:
        aircraft_repo = AircraftRepository(session)
        
        # Create a new aircraft
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            icao24="ABC123",
            model="Boeing 737-800",
            operator="Example Airlines",
            manufacturer="Boeing"
        )
        aircraft_repo.create(aircraft)
        
        # Find an aircraft by ID
        found = aircraft_repo.find_by_id("AC001")
        print(f"Found aircraft: {found.tail_number}")
        
        # Find all aircraft
        all_aircraft = aircraft_repo.find_all(limit=10)
        for ac in all_aircraft:
            print(f"- {ac.tail_number}: {ac.model}")
```

### Working with Flights

```python
from neo4j_client import FlightRepository, Flight

with connection.get_session() as session:
    flight_repo = FlightRepository(session)
    
    # Create a flight
    flight = Flight(
        flight_id="FL001",
        flight_number="EX123",
        aircraft_id="AC001",
        operator="Example Airlines",
        origin="JFK",
        destination="LAX",
        scheduled_departure="2024-01-15T10:00:00Z",
        scheduled_arrival="2024-01-15T14:30:00Z"
    )
    flight_repo.create(flight)
    
    # Find flights for a specific aircraft
    aircraft_flights = flight_repo.find_by_aircraft("AC001")
    for flt in aircraft_flights:
        print(f"{flt.flight_number}: {flt.origin} → {flt.destination}")
```

### Working with Maintenance Events

```python
from neo4j_client import MaintenanceEventRepository, MaintenanceEvent

with connection.get_session() as session:
    maintenance_repo = MaintenanceEventRepository(session)
    
    # Create a maintenance event
    event = MaintenanceEvent(
        event_id="ME001",
        aircraft_id="AC001",
        system_id="SYS001",
        component_id="COMP001",
        fault="Engine vibration detected",
        severity="HIGH",
        corrective_action="Replace engine bearing",
        reported_at="2024-01-15T08:30:00Z"
    )
    maintenance_repo.create(event)
    
    # Find all critical maintenance events
    critical_events = maintenance_repo.find_by_severity("CRITICAL")
    for evt in critical_events:
        print(f"Critical: {evt.fault} on {evt.aircraft_id}")
    
    # Find maintenance events for a specific aircraft
    aircraft_events = maintenance_repo.find_by_aircraft("AC001")
    print(f"Found {len(aircraft_events)} events for AC001")
```

### Error Handling

```python
from neo4j_client import NotFoundError, QueryError, ConnectionError

try:
    with Neo4jConnection(uri="bolt://localhost:7687", 
                         username="neo4j", 
                         password="wrong") as conn:
        pass
except ConnectionError as e:
    print(f"Connection failed: {e}")

try:
    with connection.get_session() as session:
        repo = AircraftRepository(session)
        aircraft.aircraft_id = "NONEXISTENT"
        repo.update(aircraft)
except NotFoundError as e:
    print(f"Aircraft not found: {e}")
except QueryError as e:
    print(f"Query failed: {e}")
```

## Available Models

The library includes Pydantic models for all Neo4j entities:

- **Aircraft** - Aircraft information (tail number, model, manufacturer, etc.)
- **Airport** - Airport data (IATA, ICAO, coordinates, etc.)
- **Flight** - Flight details (flight number, origin, destination, schedule)
- **Delay** - Flight delay information (cause, duration)
- **MaintenanceEvent** - Maintenance and fault records
- **System** - Aircraft system information
- **Component** - System component details
- **Sensor** - Sensor metadata
- **Reading** - Sensor reading data

## Available Repositories

Currently implemented repositories:

- **AircraftRepository** - CRUD operations for aircraft
  - `create(aircraft)` - Create or merge aircraft
  - `find_by_id(aircraft_id)` - Find by ID
  - `find_all(limit=100)` - Find all aircraft
  - `update(aircraft)` - Update existing aircraft
  - `delete(aircraft_id)` - Delete aircraft

- **FlightRepository** - Flight operations
  - `create(flight)` - Create or merge flight
  - `find_by_id(flight_id)` - Find by ID
  - `find_by_aircraft(aircraft_id)` - Find flights by aircraft
  - `find_all(limit=100)` - Find all flights

- **MaintenanceEventRepository** - Maintenance event operations
  - `create(event)` - Create or merge event
  - `find_by_id(event_id)` - Find by ID
  - `find_by_aircraft(aircraft_id)` - Find events by aircraft
  - `find_by_severity(severity)` - Find events by severity level

## Testing

The library uses pytest with testcontainers for integration testing:

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

Tests automatically spin up a Neo4j container, run the tests, and clean up afterward.

## Project Structure

```
neo4j_client/
├── __init__.py          # Package exports and version
├── models.py            # Pydantic data models
├── repository.py        # Repository pattern implementations
├── connection.py        # Connection management
└── exceptions.py        # Custom exception classes

tests/
├── __init__.py
├── conftest.py          # pytest fixtures with testcontainers
└── test_repository.py   # Integration tests
```

## Security Best Practices

This library follows security best practices:

1. ✅ **Parameterized queries** - All Cypher queries use named parameters
2. ✅ **No string interpolation** - Prevents injection attacks
3. ✅ **MERGE over CREATE** - Avoids duplicate nodes
4. ✅ **Input validation** - Pydantic validates all data
5. ✅ **Error handling** - Wraps Neo4j exceptions with context

## Next Steps

This is a foundational client library. You can extend it by:

- Adding more repository classes for other entities (Airport, System, Component, etc.)
- Implementing relationship management (e.g., linking flights to airports)
- Adding pagination support for large result sets
- Implementing batch operations for bulk inserts/updates
- Adding async support for concurrent operations
- Creating aggregation queries for analytics
- Adding connection pooling configuration
- Implementing retry logic for transient failures

## Requirements

- Python 3.9+
- Neo4j 5.x
- neo4j-driver 5.15.0+
- Pydantic 2.0+

## License

This library is provided as a starting point for working with Neo4j aviation data. Modify and extend as needed for your use case.

## Contributing

This is a demo/starter library. Feel free to fork and customize for your specific needs.
