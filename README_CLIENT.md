# Neo4j Aircraft Client

A simple, well-structured Python client library for managing aircraft information in Neo4j databases. This library provides a clean starting point with Python best practices, including Pydantic models, repository pattern, and parameterized Cypher queries.

## Features

- ✅ **Type-safe models** - Pydantic models for all entities
- ✅ **Repository pattern** - Clean separation of concerns
- ✅ **Parameterized queries** - Prevents SQL injection attacks
- ✅ **Context managers** - Proper resource management
- ✅ **Integration tests** - Using testcontainers for Neo4j
- ✅ **Modern Python** - Type hints and Python 3.9+ support

## Installation

Install the package and its dependencies:

```bash
pip install -e .
```

For development, install with dev dependencies:

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from neo4j_client import Neo4jConnection, AircraftRepository, Aircraft

# Connect to Neo4j
with Neo4jConnection(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password"
) as conn:
    # Create repository
    aircraft_repo = AircraftRepository(conn)
    
    # Create a new aircraft
    aircraft = Aircraft(
        aircraft_id="AC1001",
        tail_number="N12345",
        icao24="abc123",
        model="B737-800",
        operator="ExampleAir",
        manufacturer="Boeing"
    )
    
    created = aircraft_repo.create(aircraft)
    print(f"Created: {created.tail_number}")
    
    # Find aircraft by ID
    found = aircraft_repo.find_by_id("AC1001")
    if found:
        print(f"Found: {found.model}")
    
    # Find all aircraft from an operator
    operator_aircraft = aircraft_repo.find_by_operator("ExampleAir")
    print(f"Found {len(operator_aircraft)} aircraft")
    
    # Update aircraft
    aircraft.operator = "NewAir"
    updated = aircraft_repo.update(aircraft)
    
    # Delete aircraft
    aircraft_repo.delete("AC1001")
```

### Environment Variables

You can use environment variables for configuration:

```python
import os
from neo4j_client import Neo4jConnection

conn = Neo4jConnection(
    uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    username=os.getenv("NEO4J_USERNAME", "neo4j"),
    password=os.getenv("NEO4J_PASSWORD"),
    database=os.getenv("NEO4J_DATABASE", "neo4j")
)
```

## Available Models

The library includes Pydantic models for the following entities:

- **Aircraft** - Core aircraft information (tail number, model, operator, etc.)
- **System** - Aircraft systems (avionics, hydraulics, etc.)
- **Component** - System components
- **Sensor** - Monitoring sensors
- **Flight** - Flight operations
- **Airport** - Airport information

## Repository Methods

The `AircraftRepository` provides the following methods:

### Create
```python
aircraft = aircraft_repo.create(aircraft_model)
```
Creates or updates an aircraft using MERGE to avoid duplicates.

### Find
```python
# By ID
aircraft = aircraft_repo.find_by_id("AC1001")

# By tail number
aircraft = aircraft_repo.find_by_tail_number("N12345")

# All aircraft (with limit)
aircraft_list = aircraft_repo.find_all(limit=100)

# By operator
aircraft_list = aircraft_repo.find_by_operator("ExampleAir")

# By manufacturer
aircraft_list = aircraft_repo.find_by_manufacturer("Boeing")
```

### Update
```python
aircraft.operator = "NewOperator"
updated = aircraft_repo.update(aircraft)
```

### Delete
```python
deleted = aircraft_repo.delete("AC1001")  # Returns True if deleted
```

## Running Tests

The library includes comprehensive integration tests using testcontainers:

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

**Note**: Tests require Docker to be running, as they use testcontainers to spin up a Neo4j instance.

## Database Schema

The client is designed to work with the following Neo4j schema:

```
(Aircraft)
  ├─[:HAS_SYSTEM]─>(System)
  │                  ├─[:HAS_COMPONENT]─>(Component)
  │                  │                      └─[:HAS_EVENT]─>(MaintenanceEvent)
  │                  └─[:HAS_SENSOR]─>(Sensor)
  └─[:OPERATES_FLIGHT]─>(Flight)
                         ├─[:DEPARTS_FROM]─>(Airport)
                         ├─[:ARRIVES_AT]─>(Airport)
                         └─[:HAS_DELAY]─>(Delay)
```

## Security Best Practices

This library follows security best practices:

- ✅ **Parameterized queries** - All Cypher queries use named parameters
- ✅ **No string interpolation** - Prevents injection attacks
- ✅ **Input validation** - Pydantic models validate all inputs
- ✅ **Error handling** - Custom exceptions for different error types
- ✅ **MERGE over CREATE** - Prevents duplicate nodes

## Next Steps

This is a starting point for your aircraft management system. Here are some ideas for extending it:

### Additional Repositories
Create repositories for other entities:
- `SystemRepository` - Manage aircraft systems
- `FlightRepository` - Manage flight operations
- `MaintenanceEventRepository` - Track maintenance events

### Relationships
Add methods to manage relationships:
- Link aircraft to systems
- Associate flights with aircraft
- Track maintenance history

### Advanced Queries
Implement more complex queries:
- Find aircraft due for maintenance
- Get flight history for an aircraft
- Analyze sensor readings and patterns

### Transaction Management
Add transaction support for multi-step operations:
- Create aircraft with systems in one transaction
- Update multiple related entities atomically

## Project Structure

```
neo4j-aircraft-client/
├── neo4j_client/
│   ├── __init__.py          # Package exports
│   ├── models.py            # Pydantic data models
│   ├── repository.py        # Repository pattern implementation
│   ├── connection.py        # Connection management
│   └── exceptions.py        # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest fixtures
│   └── test_repository.py   # Integration tests
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

## Requirements

- Python 3.9 or higher
- Neo4j 5.x database
- Docker (for running tests)

## License

MIT License - feel free to use and modify as needed.

## Contributing

This is a starting point library. Feel free to extend it for your specific needs:

1. Add new repository classes for other entities
2. Implement additional query methods
3. Add relationship management
4. Extend models with validation rules
5. Add async support if needed

## Support

For issues related to:
- **Neo4j Python Driver**: https://github.com/neo4j/neo4j-python-driver
- **Pydantic**: https://docs.pydantic.dev/
- **This library**: Open an issue in this repository
