# Neo4j Aircraft Client

A simple, type-safe Python client library for working with aircraft data in Neo4j databases.

## Features

✅ **Pydantic Models** - Type-safe data classes for all entities  
✅ **Repository Pattern** - Clean query organization with CRUD operations  
✅ **Parameterized Queries** - Secure Cypher queries to prevent injection attacks  
✅ **Context Managers** - Proper resource management  
✅ **Integration Tests** - Working examples with pytest and testcontainers  
✅ **Type Hints** - Full type annotation support  

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
from neo4j_aircraft_client import (
    Neo4jConnection,
    AircraftRepository,
    FlightRepository,
    Aircraft,
)

# Connect to Neo4j
conn = Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your-password",
    database="neo4j"
)

# Use repositories to query data
with conn.session() as session:
    # Create repository instances
    aircraft_repo = AircraftRepository(session)
    flight_repo = FlightRepository(session)
    
    # Find an aircraft by tail number
    aircraft = aircraft_repo.find_by_tail_number("N12345")
    if aircraft:
        print(f"Found: {aircraft.model} operated by {aircraft.operator}")
    
    # Get all flights for an aircraft
    flights = flight_repo.find_by_aircraft(aircraft.aircraft_id, limit=10)
    for flight in flights:
        print(f"Flight {flight.flight_number}: {flight.origin} → {flight.destination}")

# Close connection
conn.close()
```

### Using Context Manager

```python
from neo4j_aircraft_client import Neo4jConnection, AirportRepository

# Connection automatically closes when context exits
with Neo4jConnection("bolt://localhost:7687", "neo4j", "password") as conn:
    with conn.session() as session:
        airport_repo = AirportRepository(session)
        
        # Find airport by IATA code
        airport = airport_repo.find_by_iata("LAX")
        if airport:
            print(f"{airport.name} ({airport.iata})")
            print(f"Location: {airport.city}, {airport.country}")
            print(f"Coordinates: {airport.lat}, {airport.lon}")
```

### Creating New Entities

```python
from neo4j_aircraft_client import Neo4jConnection, AircraftRepository, Aircraft

with Neo4jConnection("bolt://localhost:7687", "neo4j", "password") as conn:
    with conn.session() as session:
        aircraft_repo = AircraftRepository(session)
        
        # Create a new aircraft
        new_aircraft = Aircraft(
            aircraft_id="AC-12345",
            tail_number="N54321",
            icao24="A1B2C3",
            model="Boeing 737-800",
            operator="Example Airlines",
            manufacturer="Boeing"
        )
        
        created = aircraft_repo.create(new_aircraft)
        print(f"Created aircraft: {created.aircraft_id}")
```

### Querying Maintenance Events

```python
from neo4j_aircraft_client import Neo4jConnection, MaintenanceEventRepository

with Neo4jConnection("bolt://localhost:7687", "neo4j", "password") as conn:
    with conn.session() as session:
        maintenance_repo = MaintenanceEventRepository(session)
        
        # Find critical maintenance events
        critical_events = maintenance_repo.find_by_severity("CRITICAL", limit=10)
        for event in critical_events:
            print(f"Event {event.event_id}:")
            print(f"  Aircraft: {event.aircraft_id}")
            print(f"  Fault: {event.fault}")
            print(f"  Reported: {event.reported_at}")
            print(f"  Action: {event.corrective_action}")
            print()
        
        # Find all maintenance events for a specific aircraft
        aircraft_events = maintenance_repo.find_by_aircraft("AC-001", limit=20)
        print(f"Found {len(aircraft_events)} maintenance events for aircraft AC-001")
```

### Working with Systems

```python
from neo4j_aircraft_client import Neo4jConnection, SystemRepository

with Neo4jConnection("bolt://localhost:7687", "neo4j", "password") as conn:
    with conn.session() as session:
        system_repo = SystemRepository(session)
        
        # Get all systems for an aircraft
        systems = system_repo.find_by_aircraft("AC-001")
        for system in systems:
            print(f"{system.name} ({system.type})")
```

## Data Models

The library includes Pydantic models for the following entities:

- **Aircraft** - Commercial aircraft in the fleet
- **Airport** - Airports with location and identification codes
- **Flight** - Scheduled flight operations
- **System** - Aircraft systems (hydraulics, avionics, engines, etc.)
- **Component** - Components within aircraft systems
- **Sensor** - Sensors that monitor systems
- **MaintenanceEvent** - Maintenance events and fault reports
- **Delay** - Flight delay incidents

See the [DATA_MODEL.md](DATA_MODEL.md) for detailed schema documentation.

## Available Repositories

### AircraftRepository

- `create(aircraft: Aircraft) -> Aircraft`
- `find_by_id(aircraft_id: str) -> Optional[Aircraft]`
- `find_by_tail_number(tail_number: str) -> Optional[Aircraft]`
- `find_all(limit: int = 100) -> List[Aircraft]`
- `update(aircraft: Aircraft) -> Aircraft`
- `delete(aircraft_id: str) -> bool`

### FlightRepository

- `create(flight: Flight) -> Flight`
- `find_by_id(flight_id: str) -> Optional[Flight]`
- `find_by_aircraft(aircraft_id: str, limit: int = 100) -> List[Flight]`
- `find_all(limit: int = 100) -> List[Flight]`
- `delete(flight_id: str) -> bool`

### AirportRepository

- `create(airport: Airport) -> Airport`
- `find_by_id(airport_id: str) -> Optional[Airport]`
- `find_by_iata(iata: str) -> Optional[Airport]`
- `find_all(limit: int = 100) -> List[Airport]`

### SystemRepository

- `create(system: System) -> System`
- `find_by_id(system_id: str) -> Optional[System]`
- `find_by_aircraft(aircraft_id: str) -> List[System]`

### MaintenanceEventRepository

- `create(event: MaintenanceEvent) -> MaintenanceEvent`
- `find_by_id(event_id: str) -> Optional[MaintenanceEvent]`
- `find_by_aircraft(aircraft_id: str, limit: int = 100) -> List[MaintenanceEvent]`
- `find_by_severity(severity: str, limit: int = 100) -> List[MaintenanceEvent]`

## Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=neo4j_aircraft_client --cov-report=html
```

The tests use testcontainers to automatically spin up a Neo4j instance, or you can point to an existing instance using environment variables:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
export NEO4J_DATABASE="neo4j"
pytest
```

## Environment Variables

The client supports the following environment variables for configuration:

- `NEO4J_URI` - Database URI (e.g., `bolt://localhost:7687`)
- `NEO4J_USERNAME` - Authentication username
- `NEO4J_PASSWORD` - Authentication password
- `NEO4J_DATABASE` - Target database name (default: `neo4j`)

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation with diagrams.

## Security

This library follows security best practices:

- ✅ All Cypher queries use **parameterized queries** to prevent injection attacks
- ✅ Uses `MERGE` instead of `CREATE` to avoid duplicate nodes
- ✅ Pydantic models validate all input data before queries
- ✅ Proper exception handling with custom error types
- ✅ No string interpolation in queries

## What's Included

This is a **starting point** for working with aircraft data in Neo4j. It provides:

- Clean, type-safe models for core entities
- Basic CRUD operations with the repository pattern
- Secure, parameterized queries
- Integration tests with testcontainers
- Clear examples and documentation

## Next Steps

To extend this library for production use, consider adding:

- **Relationship Management** - Methods to create/query relationships between entities
- **Transaction Support** - Methods for multi-operation transactions
- **Batch Operations** - Bulk create/update/delete methods
- **Async Support** - Async/await for non-blocking operations
- **Query Builders** - Flexible query construction for complex searches
- **Caching** - Cache frequently accessed data
- **Monitoring** - Logging and metrics collection
- **Connection Pooling** - Advanced connection management
- **Migration Tools** - Schema migration and versioning

## Requirements

- Python 3.9+
- Neo4j 5.0+
- neo4j-python-driver 5.0+
- pydantic 2.0+

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! This is a starting point library, and we encourage you to:

1. Fork the repository
2. Add new features or improvements
3. Write tests for your changes
4. Submit a pull request

## Support

For issues or questions:

- Open an issue on GitHub
- Check the [Neo4j Community Forum](https://community.neo4j.com/)
- Review the [Neo4j Python Driver Documentation](https://neo4j.com/docs/python-manual/current/)
