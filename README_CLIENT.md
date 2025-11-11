# Neo4j Airplane Client

A simple, high-quality Python client library for querying airplane/aviation data from a Neo4j database.

## Features

✅ **Type-safe models** - Pydantic models for all aviation entities  
✅ **Repository pattern** - Clean, organized query interface  
✅ **Parameterized queries** - Secure, injection-safe Cypher queries  
✅ **Integration tests** - Pytest tests with testcontainers  
✅ **Modern Python** - Type hints, Python 3.9+ support  
✅ **Easy to extend** - Modular design for customization

## Installation

```bash
pip install -e .
```

For development with testing:

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from neo4j_client import Neo4jConnection, AircraftRepository, FlightRepository

# Connect to Neo4j
connection = Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password",
    database="neo4j"
)

# Using context manager (recommended)
with connection:
    session = connection.get_session()
    
    # Query aircraft
    aircraft_repo = AircraftRepository(session)
    aircraft = aircraft_repo.find_by_tail_number("N12345")
    print(f"Found: {aircraft.model} operated by {aircraft.operator}")
    
    # Query flights
    flight_repo = FlightRepository(session)
    flights = flight_repo.find_by_aircraft(aircraft.aircraft_id, limit=10)
    for flight in flights:
        print(f"Flight {flight.flight_number}: {flight.origin} → {flight.destination}")
    
    session.close()
```

### Creating New Entities

```python
from neo4j_client import Aircraft, AircraftRepository

with connection:
    session = connection.get_session()
    repo = AircraftRepository(session)
    
    # Create a new aircraft
    new_aircraft = Aircraft(
        aircraft_id="AC001",
        tail_number="N99999",
        icao24="ABC123",
        model="Boeing 737-800",
        operator="Example Airlines",
        manufacturer="Boeing"
    )
    
    created = repo.create(new_aircraft)
    print(f"Created aircraft: {created.tail_number}")
    
    session.close()
```

### Querying Maintenance Events

```python
from neo4j_client import MaintenanceEventRepository

with connection:
    session = connection.get_session()
    repo = MaintenanceEventRepository(session)
    
    # Find critical maintenance events
    critical_events = repo.find_by_severity("CRITICAL", limit=10)
    for event in critical_events:
        print(f"Critical: {event.fault} on {event.reported_at}")
    
    # Find maintenance events for a specific aircraft
    aircraft_events = repo.find_by_aircraft("AC001", limit=20)
    
    session.close()
```

### Finding Delays

```python
from neo4j_client import DelayRepository

with connection:
    session = connection.get_session()
    repo = DelayRepository(session)
    
    # Find significant delays (over 30 minutes)
    delays = repo.find_significant_delays(min_minutes=30, limit=50)
    for delay in delays:
        print(f"Delay: {delay.minutes} min - {delay.cause}")
    
    session.close()
```

## Available Repositories

### AircraftRepository
- `create(aircraft)` - Create or update an aircraft
- `find_by_id(aircraft_id)` - Find by aircraft ID
- `find_by_tail_number(tail_number)` - Find by tail number
- `find_all(limit)` - Get all aircraft
- `update(aircraft)` - Update an aircraft
- `delete(aircraft_id)` - Delete an aircraft

### AirportRepository
- `create(airport)` - Create or update an airport
- `find_by_id(airport_id)` - Find by airport ID
- `find_by_iata(iata)` - Find by IATA code (e.g., "LAX")
- `find_all(limit)` - Get all airports

### FlightRepository
- `create(flight)` - Create or update a flight
- `find_by_id(flight_id)` - Find by flight ID
- `find_by_aircraft(aircraft_id, limit)` - Find flights by aircraft
- `find_all(limit)` - Get all flights

### MaintenanceEventRepository
- `create(event)` - Create or update a maintenance event
- `find_by_id(event_id)` - Find by event ID
- `find_by_aircraft(aircraft_id, limit)` - Find events for an aircraft
- `find_by_severity(severity, limit)` - Find by severity level
- `find_all(limit)` - Get all maintenance events

### DelayRepository
- `create(delay)` - Create or update a delay
- `find_by_id(delay_id)` - Find by delay ID
- `find_by_flight(flight_id)` - Find delays for a flight
- `find_significant_delays(min_minutes, limit)` - Find delays over threshold
- `find_all(limit)` - Get all delays

## Data Models

The client includes Pydantic models for all aviation entities:

- **Aircraft** - Commercial aircraft in the fleet
- **Airport** - Airports with IATA/ICAO codes and coordinates
- **Flight** - Scheduled flight operations
- **System** - Aircraft systems (hydraulics, avionics, etc.)
- **Component** - Components within systems
- **Sensor** - Monitoring sensors
- **Reading** - Time-series sensor readings
- **MaintenanceEvent** - Maintenance events and faults
- **Delay** - Flight delay incidents

See [DATA_MODEL.md](DATA_MODEL.md) for the complete data model documentation.

## Testing

The client includes comprehensive tests using pytest and testcontainers:

```bash
# Run tests (will start a Neo4j container automatically)
pytest

# Run tests with coverage
pytest --cov=neo4j_client --cov-report=html

# Run specific test file
pytest tests/test_repository.py

# Run with verbose output
pytest -v
```

### Using Existing Neo4j Instance

To test against an existing Neo4j instance instead of starting a container:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your_password"
export NEO4J_DATABASE="neo4j"

pytest
```

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

pyproject.toml           # Project configuration
README.md                # This file
```

## Requirements

- Python 3.9+
- Neo4j 5.0+
- Dependencies:
  - `neo4j` - Official Neo4j Python driver
  - `pydantic` - Data validation and type safety

## Security Notes

This client follows security best practices:

✅ All Cypher queries use **parameterized queries** (no string interpolation)  
✅ Uses `MERGE` over `CREATE` to avoid duplicate nodes  
✅ Input validation with Pydantic models  
✅ Proper error handling and custom exceptions

## Next Steps

This is a **starting point** for your aviation data client. Here are some ways to extend it:

- Add async/await support for concurrent queries
- Implement additional relationship queries (e.g., flight routes with airports)
- Add pagination helpers for large result sets
- Create custom queries for specific business logic
- Add caching for frequently accessed data
- Implement transaction support for multi-step operations
- Add logging and monitoring
- Create CLI tools for common operations

## License

MIT License - see LICENSE file for details

## Contributing

This is a basic client library meant to be customized for your specific needs. Feel free to:

1. Fork and modify for your use case
2. Add new repositories for additional entities
3. Extend existing repositories with custom queries
4. Add business logic specific to your domain

## Support

For Neo4j-specific questions, see:
- [Neo4j Python Driver Documentation](https://neo4j.com/docs/python-manual/current/)
- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [Neo4j Community Forum](https://community.neo4j.com/)
