# Architecture Documentation

This document describes the architecture of the Neo4j Aircraft Client library, including package structure, data flow, and design patterns.

## Table of Contents

- [Overview](#overview)
- [Package Structure](#package-structure)
- [Design Patterns](#design-patterns)
- [Data Flow](#data-flow)
- [Component Diagrams](#component-diagrams)
- [Security Architecture](#security-architecture)
- [Extension Points](#extension-points)

## Overview

The Neo4j Aircraft Client is designed as a lightweight, type-safe Python library for working with aviation data stored in Neo4j. It follows modern Python best practices and provides a clean, extensible foundation for building aircraft data applications.

### Design Principles

1. **Simplicity First** - Easy to understand and use
2. **Type Safety** - Pydantic models with full type hints
3. **Security by Default** - Parameterized queries, no string interpolation
4. **Separation of Concerns** - Clear boundaries between layers
5. **Extensibility** - Easy to add new entities and operations

## Package Structure

```mermaid
graph TD
    A[neo4j_aircraft_client/] --> B[__init__.py]
    A --> C[models.py]
    A --> D[repository.py]
    A --> E[connection.py]
    A --> F[exceptions.py]
    
    G[tests/] --> H[conftest.py]
    G --> I[test_repository.py]
    
    J[Root] --> K[pyproject.toml]
    J --> L[README_CLIENT.md]
    J --> M[ARCHITECTURE.md]
    
    style A fill:#e1f5ff
    style G fill:#fff4e1
    style J fill:#f0f0f0
```

### Module Responsibilities

| Module | Purpose | Key Components |
|--------|---------|----------------|
| `models.py` | Data models and validation | Aircraft, Flight, Airport, System, MaintenanceEvent, Delay (Pydantic models) |
| `repository.py` | Data access layer | AircraftRepository, FlightRepository, AirportRepository, SystemRepository, MaintenanceEventRepository |
| `connection.py` | Database connectivity | Neo4jConnection (context manager) |
| `exceptions.py` | Error handling | Neo4jClientError, ConnectionError, QueryError, NotFoundError |
| `__init__.py` | Public API exports | Package interface and version |

## Design Patterns

### Repository Pattern

The library uses the Repository Pattern to abstract data access logic and provide a clean interface for CRUD operations.

```mermaid
classDiagram
    class Repository {
        <<interface>>
        +create(entity)
        +find_by_id(id)
        +find_all(limit)
        +update(entity)
        +delete(id)
    }
    
    class AircraftRepository {
        -session: Session
        +create(aircraft: Aircraft)
        +find_by_id(aircraft_id: str)
        +find_by_tail_number(tail_number: str)
        +find_all(limit: int)
        +update(aircraft: Aircraft)
        +delete(aircraft_id: str)
    }
    
    class FlightRepository {
        -session: Session
        +create(flight: Flight)
        +find_by_id(flight_id: str)
        +find_by_aircraft(aircraft_id: str, limit: int)
        +find_all(limit: int)
        +delete(flight_id: str)
    }
    
    class AirportRepository {
        -session: Session
        +create(airport: Airport)
        +find_by_id(airport_id: str)
        +find_by_iata(iata: str)
        +find_all(limit: int)
    }
    
    Repository <|.. AircraftRepository
    Repository <|.. FlightRepository
    Repository <|.. AirportRepository
```

**Benefits:**

- Centralized data access logic
- Easy to test (can mock repositories)
- Clean separation from business logic
- Consistent API across entities

### Pydantic Models

All entities are defined as Pydantic models for automatic validation and type safety.

```mermaid
classDiagram
    class BaseModel {
        <<Pydantic>>
        +model_dump()
        +model_validate()
    }
    
    class Aircraft {
        +aircraft_id: str
        +tail_number: str
        +icao24: str
        +model: str
        +operator: str
        +manufacturer: str
    }
    
    class Flight {
        +flight_id: str
        +flight_number: str
        +aircraft_id: str
        +operator: str
        +origin: str
        +destination: str
        +scheduled_departure: str
        +scheduled_arrival: str
    }
    
    class Airport {
        +airport_id: str
        +iata: str
        +icao: str
        +name: str
        +city: str
        +country: str
        +lat: float
        +lon: float
    }
    
    class MaintenanceEvent {
        +event_id: str
        +aircraft_id: str
        +system_id: str
        +component_id: str
        +fault: str
        +severity: str
        +reported_at: str
        +corrective_action: str
    }
    
    BaseModel <|-- Aircraft
    BaseModel <|-- Flight
    BaseModel <|-- Airport
    BaseModel <|-- MaintenanceEvent
```

**Benefits:**

- Automatic data validation
- Type hints for IDE support
- Easy serialization/deserialization
- Self-documenting code

## Data Flow

### Read Operation Flow

```mermaid
sequenceDiagram
    participant App as Application
    participant Conn as Neo4jConnection
    participant Sess as Session
    participant Repo as Repository
    participant Neo4j as Neo4j Database
    participant Model as Pydantic Model
    
    App->>Conn: Create connection
    Conn->>Neo4j: Verify connectivity
    Neo4j-->>Conn: Connection OK
    
    App->>Conn: Get session
    Conn-->>Sess: Return session
    
    App->>Repo: Create repository(session)
    App->>Repo: find_by_id(id)
    
    Repo->>Repo: Build parameterized query
    Repo->>Sess: Run query with parameters
    Sess->>Neo4j: Execute Cypher query
    Neo4j-->>Sess: Return results
    
    Sess-->>Repo: Query result
    Repo->>Model: Validate and create model
    Model-->>Repo: Validated model instance
    Repo-->>App: Return entity
    
    App->>Sess: Close session
    App->>Conn: Close connection
```

### Write Operation Flow

```mermaid
sequenceDiagram
    participant App as Application
    participant Model as Pydantic Model
    participant Repo as Repository
    participant Sess as Session
    participant Neo4j as Neo4j Database
    
    App->>Model: Create entity instance
    Model->>Model: Validate data
    Model-->>App: Validated entity
    
    App->>Repo: create(entity)
    Repo->>Model: Extract data (model_dump)
    Model-->>Repo: Dictionary of values
    
    Repo->>Repo: Build MERGE query
    Repo->>Sess: Run query with parameters
    Sess->>Neo4j: Execute MERGE statement
    Neo4j-->>Sess: Return created node
    
    Sess-->>Repo: Query result
    Repo->>Model: Create model from result
    Model-->>Repo: Created entity
    Repo-->>App: Return created entity
```

## Component Diagrams

### System Context

```mermaid
graph TB
    App[Python Application] -->|Uses| Client[Neo4j Aircraft Client]
    Client -->|Connects to| Neo4j[(Neo4j Database)]
    
    Client -->|Validates with| Pydantic[Pydantic]
    Client -->|Queries via| Driver[Neo4j Python Driver]
    Driver -->|Bolt Protocol| Neo4j
    
    style Client fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Neo4j fill:#008CC1,stroke:#005F8C,color:#fff
    style App fill:#FFC107,stroke:#F57C00
```

### Layer Architecture

```mermaid
graph TB
    subgraph Application Layer
        A1[Your Application Code]
    end
    
    subgraph Client Library
        B1[Models<br/>Pydantic Validation]
        B2[Repositories<br/>Query Logic]
        B3[Connection<br/>Session Management]
        B4[Exceptions<br/>Error Handling]
    end
    
    subgraph Infrastructure Layer
        C1[Neo4j Python Driver]
        C2[Neo4j Database]
    end
    
    A1 --> B1
    A1 --> B2
    A1 --> B3
    
    B2 --> B1
    B2 --> B3
    B2 --> B4
    
    B3 --> C1
    C1 --> C2
    
    style B1 fill:#E8F5E9
    style B2 fill:#E3F2FD
    style B3 fill:#FFF3E0
    style B4 fill:#FCE4EC
```

### Dependency Graph

```mermaid
graph LR
    App[Application] --> Init[__init__.py]
    
    Init --> Models[models.py]
    Init --> Repo[repository.py]
    Init --> Conn[connection.py]
    Init --> Exc[exceptions.py]
    
    Repo --> Models
    Repo --> Exc
    Conn --> Exc
    
    Repo --> Neo4jDriver[neo4j.Session]
    Conn --> Neo4jDriver2[neo4j.GraphDatabase]
    
    Models --> Pydantic[pydantic.BaseModel]
    
    style Init fill:#4CAF50,color:#fff
    style Models fill:#2196F3,color:#fff
    style Repo fill:#FF9800,color:#fff
    style Conn fill:#9C27B0,color:#fff
    style Exc fill:#F44336,color:#fff
```

## Security Architecture

### Query Parameterization

All queries use Neo4j's parameterized query system to prevent Cypher injection attacks.

```mermaid
graph LR
    A[User Input] -->|Validated by| B[Pydantic Model]
    B -->|model_dump| C[Dictionary]
    C -->|Parameters| D[Cypher Query]
    D -->|session.run| E[Neo4j Driver]
    E -->|Parameterized| F[(Neo4j)]
    
    style A fill:#FFEBEE
    style B fill:#E8F5E9
    style D fill:#FFF3E0
    style F fill:#E3F2FD
```

**Example:**

```python
# ❌ BAD - String interpolation (vulnerable to injection)
query = f"MATCH (a:Aircraft {{tail_number: '{tail_number}'}}) RETURN a"

# ✅ GOOD - Parameterized query (secure)
query = "MATCH (a:Aircraft {tail_number: $tail_number}) RETURN a"
result = session.run(query, tail_number=tail_number)
```

### Error Handling Flow

```mermaid
graph TD
    A[Repository Method] --> B{Try Query}
    B -->|Success| C[Return Result]
    B -->|Neo4j Error| D[Catch Exception]
    B -->|Not Found| E[Return None/Empty]
    
    D --> F{Error Type}
    F -->|Connection| G[Raise ConnectionError]
    F -->|Query Syntax| H[Raise QueryError]
    F -->|Not Found| I[Raise NotFoundError]
    
    style G fill:#F44336,color:#fff
    style H fill:#FF9800,color:#fff
    style I fill:#FFC107,color:#fff
```

## Extension Points

### Adding New Entities

To add a new entity type:

1. **Define Model** in `models.py`:
```python
class NewEntity(BaseModel):
    entity_id: str
    name: str
    # ... other fields
```

2. **Create Repository** in `repository.py`:
```python
class NewEntityRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, entity: NewEntity) -> NewEntity:
        # Implementation
    
    # ... other methods
```

3. **Export** in `__init__.py`:
```python
from .models import NewEntity
from .repository import NewEntityRepository

__all__ = [..., "NewEntity", "NewEntityRepository"]
```

### Adding Custom Queries

```mermaid
graph TB
    A[Identify Query Need] --> B[Add Method to Repository]
    B --> C[Write Parameterized Cypher]
    C --> D[Add Type Hints]
    D --> E[Handle Errors]
    E --> F[Return Typed Results]
    F --> G[Add Tests]
    G --> H[Document in README]
    
    style A fill:#E3F2FD
    style G fill:#E8F5E9
    style H fill:#FFF3E0
```

### Repository Extension Pattern

```python
class ExtendedAircraftRepository(AircraftRepository):
    """Extended repository with custom queries."""
    
    def find_by_operator(self, operator: str, limit: int = 100) -> List[Aircraft]:
        """Find aircraft by operator."""
        query = """
        MATCH (a:Aircraft {operator: $operator})
        RETURN a
        ORDER BY a.tail_number
        LIMIT $limit
        """
        result = self.session.run(query, operator=operator, limit=limit)
        return [Aircraft(**dict(record["a"])) for record in result]
```

## Testing Architecture

### Test Structure

```mermaid
graph TB
    subgraph Test Suite
        A[conftest.py<br/>Fixtures]
        B[test_repository.py<br/>Integration Tests]
    end
    
    subgraph Test Infrastructure
        C[pytest]
        D[testcontainers<br/>Neo4j Container]
    end
    
    subgraph System Under Test
        E[Repositories]
        F[Models]
        G[Connection]
    end
    
    A --> C
    A --> D
    B --> A
    B --> E
    E --> F
    E --> G
    
    D -->|Provides| H[(Test Neo4j)]
    G -->|Connects to| H
    
    style A fill:#E8F5E9
    style B fill:#E3F2FD
    style D fill:#FFF3E0
```

### Test Data Flow

```mermaid
sequenceDiagram
    participant Test as Test Case
    participant Fixture as Pytest Fixture
    participant Container as Testcontainer
    participant Neo4j as Neo4j Instance
    participant Repo as Repository
    
    Test->>Fixture: Request session fixture
    Fixture->>Container: Start Neo4j container
    Container->>Neo4j: Launch Neo4j
    Neo4j-->>Container: Ready
    Container-->>Fixture: Connection details
    
    Fixture->>Repo: Create repository with session
    Fixture-->>Test: Return session
    
    Test->>Repo: Execute test operations
    Repo->>Neo4j: Query database
    Neo4j-->>Repo: Results
    Repo-->>Test: Assertions
    
    Test->>Fixture: Test complete
    Fixture->>Container: Cleanup
    Container->>Neo4j: Shutdown
```

## Performance Considerations

### Connection Pooling

```mermaid
graph LR
    A[Application] -->|Requests| B[Connection Pool]
    B -->|Allocates| C[Session 1]
    B -->|Allocates| D[Session 2]
    B -->|Allocates| E[Session N]
    
    C -->|Queries| F[(Neo4j)]
    D -->|Queries| F
    E -->|Queries| F
    
    C -.->|Returns| B
    D -.->|Returns| B
    E -.->|Returns| B
    
    style B fill:#4CAF50,color:#fff
    style F fill:#008CC1,color:#fff
```

**Note:** The current implementation uses single connections. For production, consider implementing connection pooling.

### Query Optimization

```mermaid
graph TD
    A[Query Request] --> B{Check Cache}
    B -->|Hit| C[Return Cached]
    B -->|Miss| D[Execute Query]
    D --> E{Use Index?}
    E -->|Yes| F[Index Scan]
    E -->|No| G[Full Scan]
    F --> H[Return Results]
    G --> H
    H --> I[Cache Results]
    I --> J[Return to Client]
    
    style C fill:#4CAF50,color:#fff
    style F fill:#8BC34A,color:#fff
    style G fill:#FF9800,color:#fff
```

**Recommendations:**

1. Create indexes on frequently queried properties
2. Limit result sets with `LIMIT` clauses
3. Use relationship traversal instead of property matching when possible
4. Consider caching for frequently accessed data

## Summary

The Neo4j Aircraft Client architecture is designed to be:

- **Modular** - Clear separation of concerns
- **Extensible** - Easy to add new entities and queries
- **Secure** - Parameterized queries by default
- **Type-Safe** - Full Pydantic validation
- **Testable** - Repository pattern enables easy testing
- **Simple** - Minimal abstractions, clear code

This architecture provides a solid foundation for building aircraft data applications while remaining flexible enough to accommodate future requirements.
