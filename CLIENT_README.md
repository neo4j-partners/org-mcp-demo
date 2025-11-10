# Neo4j Airplane Information Client

A clean, type-safe Python client for managing airplane information in Neo4j databases. This library provides a solid foundation with best practices including Pydantic models, repository pattern, parameterized queries, and integration tests.

## Features

✅ **Type-Safe Models** - Pydantic models for Aircraft, Flight, Airport, and MaintenanceEvent entities  
✅ **Repository Pattern** - Clean separation of concerns with dedicated repositories for each entity  
✅ **Parameterized Queries** - All Cypher queries use parameters to prevent injection attacks  
✅ **Connection Management** - Context manager support for resource cleanup  
✅ **Integration Tests** - Full test suite using testcontainers for realistic testing  
✅ **Modern Python** - Built with Python 3.9+ and modern packaging (PEP 621)

## Installation

```bash
# Install the package
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from neo4j_client import Neo4jConnection, Aircraft, AircraftRepository

# Create a connection
connection = Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your-password",
    database="neo4j"
)

# Use context manager for automatic cleanup
with connection:
    # Get a session and create repository
    with connection.get_session() as session:
        repo = AircraftRepository(session)
        
        # Create a new aircraft
        aircraft = Aircraft(
            aircraft_id="AC001",
            tail_number="N12345",
            manufacturer="Boeing",
            model="737-800",
            operator="United Airlines",
            icao24="ABC123"
        )
        repo.create(aircraft)
        
        # Find aircraft by ID
        found = repo.find_by_id("AC001")
        print(f"Found: {found.tail_number} - {found.model}")
        
        # Find all aircraft by operator
        united_aircraft = repo.find_by_operator("United Airlines")
        print(f"United has {len(united_aircraft)} aircraft")
```

### Working with Flights

```python
from neo4j_client import Flight, FlightRepository

with connection:
    with connection.get_session() as session:
        repo = FlightRepository(session)
        
        # Create a flight
        flight = Flight(
            flight_id="FL001",
            flight_number="UA123",
            aircraft_id="AC001",
            operator="United Airlines",
            origin="SFO",
            destination="LAX",
            scheduled_departure="2024-01-15T10:00:00Z",
            scheduled_arrival="2024-01-15T12:00:00Z"
        )
        repo.create(flight)
        
        # Find flights by aircraft
        flights = repo.find_by_aircraft("AC001")
        for f in flights:
            print(f"{f.flight_number}: {f.origin} → {f.destination}")
```

### Working with Airports

```python
from neo4j_client import Airport, AirportRepository

with connection:
    with connection.get_session() as session:
        repo = AirportRepository(session)
        
        # Create an airport
        airport = Airport(
            airport_id="AP001",
            name="Los Angeles International Airport",
            iata="LAX",
            icao="KLAX",
            city="Los Angeles",
            country="USA",
            lat=33.9425,
            lon=-118.4081
        )
        repo.create(airport)
        
        # Find by IATA code
        lax = repo.find_by_iata("LAX")
        print(f"{lax.name} at ({lax.lat}, {lax.lon})")
```

### Working with Maintenance Events

```python
from neo4j_client import MaintenanceEvent, MaintenanceEventRepository

with connection:
    with connection.get_session() as session:
        repo = MaintenanceEventRepository(session)
        
        # Create a maintenance event
        event = MaintenanceEvent(
            event_id="ME001",
            aircraft_id="AC001",
            system_id="SYS001",
            component_id="COMP001",
            fault="Hydraulic leak detected",
            severity="HIGH",
            corrective_action="Replaced hydraulic line",
            reported_at="2024-01-15T08:30:00Z"
        )
        repo.create(event)
        
        # Find all events for an aircraft
        events = repo.find_by_aircraft("AC001")
        for e in events:
            print(f"{e.reported_at}: {e.fault} - {e.severity}")
```

## Environment Variables

You can use environment variables for configuration:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
export NEO4J_DATABASE="neo4j"
```

Then in your code:

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

## Testing

The project includes a comprehensive test suite using pytest and testcontainers:

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

The tests use testcontainers to spin up a real Neo4j instance, ensuring your code works with an actual database.

## Project Structure

```
.
├── neo4j_client/
│   ├── __init__.py          # Package exports
│   ├── models.py            # Pydantic data models
│   ├── repository.py        # Repository implementations
│   ├── connection.py        # Connection management
│   └── exceptions.py        # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest fixtures
│   └── test_repository.py   # Repository tests
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

## Data Models

### Aircraft
- `aircraft_id`: Unique identifier
- `tail_number`: Aircraft registration number
- `manufacturer`: Aircraft manufacturer (e.g., "Boeing")
- `model`: Aircraft model (e.g., "737-800")
- `operator`: Operating airline
- `icao24`: ICAO 24-bit address (optional)

### Flight
- `flight_id`: Unique identifier
- `flight_number`: Flight number (e.g., "UA123")
- `aircraft_id`: Aircraft operating this flight
- `operator`: Operating airline
- `origin`: Origin airport code
- `destination`: Destination airport code
- `scheduled_departure`: Scheduled departure time (ISO format)
- `scheduled_arrival`: Scheduled arrival time (ISO format)

### Airport
- `airport_id`: Unique identifier
- `name`: Airport name
- `iata`: IATA 3-letter code
- `icao`: ICAO 4-letter code
- `city`: City name
- `country`: Country name
- `lat`: Latitude coordinate
- `lon`: Longitude coordinate

### MaintenanceEvent
- `event_id`: Unique identifier
- `aircraft_id`: Aircraft affected
- `system_id`: System affected (optional)
- `component_id`: Component affected (optional)
- `fault`: Fault description
- `severity`: Severity level
- `corrective_action`: Corrective action taken
- `reported_at`: When event was reported (ISO format)

### Delay
- `delay_id`: Unique identifier
- `flight_id`: Flight affected
- `cause`: Delay cause
- `minutes`: Delay duration in minutes

## Available Repository Methods

### AircraftRepository
- `create(aircraft)` - Create a new aircraft
- `find_by_id(aircraft_id)` - Find aircraft by ID
- `find_by_tail_number(tail_number)` - Find aircraft by tail number
- `find_all(limit=100)` - Find all aircraft
- `find_by_operator(operator)` - Find aircraft by operator
- `update(aircraft)` - Update an aircraft
- `delete(aircraft_id)` - Delete an aircraft

### FlightRepository
- `create(flight)` - Create a new flight
- `find_by_id(flight_id)` - Find flight by ID
- `find_by_flight_number(flight_number)` - Find flights by flight number
- `find_by_aircraft(aircraft_id)` - Find flights by aircraft
- `delete(flight_id)` - Delete a flight

### AirportRepository
- `create(airport)` - Create a new airport
- `find_by_id(airport_id)` - Find airport by ID
- `find_by_iata(iata)` - Find airport by IATA code
- `find_all(limit=100)` - Find all airports
- `delete(airport_id)` - Delete an airport

### MaintenanceEventRepository
- `create(event)` - Create a new maintenance event
- `find_by_id(event_id)` - Find event by ID
- `find_by_aircraft(aircraft_id)` - Find events by aircraft

## Next Steps

This client provides a solid foundation. Here are some ideas for extending it:

### Additional Features
- [ ] Add support for Delay entity operations
- [ ] Add support for System and Component entities
- [ ] Add support for Sensor and Reading entities
- [ ] Implement relationship queries (e.g., flights between airports)
- [ ] Add batch operations for bulk inserts
- [ ] Add pagination support for large result sets
- [ ] Add date range filtering for flights and events

### Advanced Functionality
- [ ] Implement async/await support with `neo4j` async driver
- [ ] Add caching layer for frequently accessed data
- [ ] Implement change tracking and audit logging
- [ ] Add data validation rules beyond basic type checking
- [ ] Implement complex queries (e.g., flight path analysis)
- [ ] Add migration tools for schema changes

### Production Readiness
- [ ] Add comprehensive logging
- [ ] Implement retry logic for transient failures
- [ ] Add connection pooling configuration
- [ ] Implement circuit breaker pattern
- [ ] Add performance monitoring hooks
- [ ] Create CLI tools for data management

## Security

This client follows security best practices:

- ✅ All Cypher queries use parameterized statements
- ✅ No string interpolation or f-strings in queries
- ✅ Input validation through Pydantic models
- ✅ Proper exception handling and error messages
- ✅ Resource cleanup with context managers

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License - see LICENSE file for details.
