# Architecture Documentation

This document describes the architecture of the Neo4j Aircraft Client library.

## Overview

The Neo4j Aircraft Client is a Python library that provides a clean, type-safe interface for working with aviation data stored in Neo4j. It follows established design patterns and Python best practices.

## Architecture Principles

1. **Separation of Concerns** - Clear boundaries between connection, data models, and data access
2. **Type Safety** - Pydantic models ensure data validation and type checking
3. **Dependency Injection** - Repositories accept sessions, not connections
4. **Parameterized Queries** - All Cypher queries use parameters to prevent injection
5. **Resource Management** - Context managers ensure proper cleanup

## Component Architecture

```mermaid
graph TB
    Client[Client Application]
    Connection[Neo4jConnection]
    Session[Neo4j Session]
    
    subgraph Repositories
        AircraftRepo[AircraftRepository]
        FlightRepo[FlightRepository]
        MaintenanceRepo[MaintenanceEventRepository]
        SystemRepo[SystemRepository]
        AirportRepo[AirportRepository]
    end
    
    subgraph Models
        Aircraft[Aircraft Model]
        Flight[Flight Model]
        Maintenance[MaintenanceEvent Model]
        System[System Model]
        Airport[Airport Model]
    end
    
    subgraph Exceptions
        ClientError[Neo4jClientError]
        ConnError[ConnectionError]
        QueryError[QueryError]
        NotFoundError[NotFoundError]
    end
    
    Neo4j[(Neo4j Database)]
    
    Client --> Connection
    Connection --> Session
    Session --> Repositories
    Repositories --> Models
    Repositories -.throws.-> Exceptions
    Session --> Neo4j
    
    style Connection fill:#e1f5ff
    style Session fill:#e1f5ff
    style Models fill:#fff4e1
    style Repositories fill:#e8f5e9
    style Exceptions fill:#ffebee
    style Neo4j fill:#f3e5f5
```

## Layer Architecture

```mermaid
graph LR
    subgraph Application Layer
        App[Application Code]
    end
    
    subgraph Client Layer
        Repo[Repositories]
        Models[Pydantic Models]
    end
    
    subgraph Infrastructure Layer
        Connection[Connection Manager]
        Session[Neo4j Session]
    end
    
    subgraph Data Layer
        Neo4j[(Neo4j Database)]
    end
    
    App --> Repo
    App --> Models
    Repo --> Models
    Repo --> Session
    Connection --> Session
    Session --> Neo4j
    
    style App fill:#e3f2fd
    style Repo fill:#e8f5e9
    style Models fill:#fff3e0
    style Connection fill:#fce4ec
    style Session fill:#fce4ec
    style Neo4j fill:#f3e5f5
```

## Data Flow

```mermaid
sequenceDiagram
    participant App as Application
    participant Conn as Neo4jConnection
    participant Sess as Session
    participant Repo as Repository
    participant Model as Pydantic Model
    participant DB as Neo4j Database
    
    App->>Conn: Create connection (URI, credentials)
    Conn->>DB: Verify connectivity
    DB-->>Conn: Connected
    
    App->>Conn: get_session()
    Conn-->>App: Session
    
    App->>Repo: Create repository(session)
    
    App->>Repo: find_by_id("AC001")
    Repo->>Sess: run(query, params)
    Sess->>DB: Execute Cypher query
    DB-->>Sess: Result record
    Sess-->>Repo: Record
    Repo->>Model: Validate with Pydantic
    Model-->>Repo: Aircraft instance
    Repo-->>App: Aircraft model
    
    App->>Conn: close()
    Conn->>DB: Close connection
```

## Repository Pattern

The library uses the Repository Pattern to encapsulate data access logic:

```mermaid
classDiagram
    class AircraftRepository {
        -Session session
        +create(aircraft) Aircraft
        +find_by_id(id) Optional~Aircraft~
        +find_by_tail_number(tail) Optional~Aircraft~
        +find_all(limit) List~Aircraft~
        +find_by_operator(operator, limit) List~Aircraft~
        +update(aircraft) Aircraft
        +delete(id) bool
    }
    
    class FlightRepository {
        -Session session
        +find_by_id(id) Optional~Flight~
        +find_by_aircraft(aircraft_id, limit) List~Flight~
        +find_by_flight_number(number, limit) List~Flight~
        +find_by_route(origin, dest, limit) List~Flight~
        +find_with_delays(min_minutes, limit) List~dict~
    }
    
    class MaintenanceEventRepository {
        -Session session
        +find_by_id(id) Optional~MaintenanceEvent~
        +find_by_aircraft(aircraft_id, severity, limit) List~MaintenanceEvent~
        +find_by_severity(severity, limit) List~MaintenanceEvent~
        +find_by_system(system_id, limit) List~MaintenanceEvent~
        +create(event) MaintenanceEvent
    }
    
    class Session {
        +run(query, params)
        +close()
    }
    
    AircraftRepository --> Session
    FlightRepository --> Session
    MaintenanceEventRepository --> Session
```

## Model Hierarchy

```mermaid
classDiagram
    class BaseModel {
        <<Pydantic>>
    }
    
    class Aircraft {
        +str aircraft_id
        +str tail_number
        +str icao24
        +str model
        +str operator
        +str manufacturer
    }
    
    class Flight {
        +str flight_id
        +str flight_number
        +str aircraft_id
        +str operator
        +str origin
        +str destination
        +str scheduled_departure
        +str scheduled_arrival
    }
    
    class MaintenanceEvent {
        +str event_id
        +str aircraft_id
        +str system_id
        +str component_id
        +str fault
        +str severity
        +str reported_at
        +str corrective_action
    }
    
    class System {
        +str system_id
        +str aircraft_id
        +str name
        +str type
    }
    
    class Airport {
        +str airport_id
        +str iata
        +str icao
        +str name
        +str city
        +str country
        +float lat
        +float lon
    }
    
    BaseModel <|-- Aircraft
    BaseModel <|-- Flight
    BaseModel <|-- MaintenanceEvent
    BaseModel <|-- System
    BaseModel <|-- Airport
```

## Connection Management

```mermaid
stateDiagram-v2
    [*] --> Disconnected
    Disconnected --> Connecting: __init__(uri, user, pass)
    Connecting --> Connected: verify_connectivity()
    Connecting --> Failed: Connection error
    Failed --> [*]
    
    Connected --> InUse: get_session()
    InUse --> Connected: session.close()
    Connected --> Closing: close()
    Closing --> Disconnected: driver.close()
    Disconnected --> [*]
    
    note right of Connected
        Context manager support:
        __enter__ / __exit__
    end note
```

## Error Handling

```mermaid
graph TD
    Exception[Exception]
    ClientError[Neo4jClientError]
    ConnError[ConnectionError]
    QueryError[QueryError]
    NotFoundError[NotFoundError]
    
    Exception --> ClientError
    ClientError --> ConnError
    ClientError --> QueryError
    ClientError --> NotFoundError
    
    ConnError -.raised by.-> Connection[Connection failures]
    QueryError -.raised by.-> Query[Query execution errors]
    NotFoundError -.raised by.-> Update[Update/delete not found]
    
    style Exception fill:#ffebee
    style ClientError fill:#ffcdd2
    style ConnError fill:#ef9a9a
    style QueryError fill:#ef9a9a
    style NotFoundError fill:#ef9a9a
```

## Query Execution Pattern

All repository methods follow this pattern:

```mermaid
flowchart TD
    Start([Repository Method Called])
    ValidateInput{Valid Input?}
    BuildQuery[Build Parameterized Cypher Query]
    ExecuteQuery[Execute with session.run]
    ParseResult{Result Exists?}
    ValidateModel[Validate with Pydantic]
    ReturnData([Return Model/List])
    ReturnNone([Return None])
    HandleError[Raise QueryError]
    
    Start --> ValidateInput
    ValidateInput -->|Yes| BuildQuery
    ValidateInput -->|No| HandleError
    BuildQuery --> ExecuteQuery
    ExecuteQuery -->|Success| ParseResult
    ExecuteQuery -->|Failure| HandleError
    ParseResult -->|Yes| ValidateModel
    ParseResult -->|No| ReturnNone
    ValidateModel --> ReturnData
    HandleError --> End([Exception Raised])
    ReturnData --> End
    ReturnNone --> End
    
    style Start fill:#e8f5e9
    style End fill:#e8f5e9
    style HandleError fill:#ffebee
    style ValidateModel fill:#fff3e0
```

## Security Considerations

### Parameterized Queries

All Cypher queries use parameters to prevent injection attacks:

```python
# ✅ GOOD - Parameterized query
query = "MATCH (a:Aircraft {aircraft_id: $aircraft_id}) RETURN a"
result = session.run(query, aircraft_id=user_input)

# ❌ BAD - String interpolation (vulnerable to injection)
query = f"MATCH (a:Aircraft {{aircraft_id: '{user_input}'}}) RETURN a"
result = session.run(query)
```

### Input Validation

Pydantic models validate all input data before it reaches the database:

```mermaid
sequenceDiagram
    participant App
    participant Model as Pydantic Model
    participant Repo as Repository
    participant DB as Neo4j
    
    App->>Model: Create Aircraft(data)
    Model->>Model: Validate types, constraints
    alt Invalid Data
        Model-->>App: ValidationError
    else Valid Data
        Model-->>App: Aircraft instance
        App->>Repo: create(aircraft)
        Repo->>DB: Parameterized query
        DB-->>Repo: Result
        Repo-->>App: Created aircraft
    end
```

## Package Structure

```
neo4j_client/
├── __init__.py          # Package exports and public API
├── connection.py        # Connection management (Neo4jConnection)
├── models.py            # Pydantic data models
├── repository.py        # Repository classes for data access
└── exceptions.py        # Custom exception hierarchy

tests/
├── __init__.py
├── conftest.py          # Pytest fixtures (testcontainers)
└── test_repository.py   # Integration tests

pyproject.toml           # Modern Python packaging (PEP 621)
README_CLIENT.md         # User documentation
ARCHITECTURE.md          # This file
```

## Design Patterns Used

### 1. Repository Pattern
Encapsulates data access logic and provides a clean API for queries.

### 2. Dependency Injection
Repositories accept sessions as constructor parameters, allowing for flexible testing and connection management.

### 3. Context Manager
`Neo4jConnection` implements `__enter__` and `__exit__` for safe resource cleanup:

```python
with Neo4jConnection(uri, user, pass) as conn:
    session = conn.get_session()
    # ... use session
    # Automatic cleanup on exit
```

### 4. Factory Pattern
Repositories create Pydantic model instances from database records.

### 5. Data Transfer Object (DTO)
Pydantic models serve as DTOs, transferring data between layers with validation.

## Testing Strategy

```mermaid
graph TB
    Tests[Integration Tests]
    Container[Testcontainers Neo4j]
    Fixtures[Pytest Fixtures]
    Session[Test Session]
    Cleanup[Cleanup After Each Test]
    
    Tests --> Fixtures
    Fixtures --> Container
    Container --> Session
    Tests --> Session
    Session --> Cleanup
    
    style Tests fill:#e8f5e9
    style Container fill:#e1f5ff
    style Fixtures fill:#fff3e0
```

The test suite uses:
- **Testcontainers** - Spins up real Neo4j instance in Docker
- **Pytest fixtures** - Manages container lifecycle
- **Session-scoped fixtures** - Reuses container across tests
- **Cleanup** - Deletes all data after each test

## Extension Points

The library is designed to be extended:

### 1. Add New Repositories
```python
class SensorRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def find_by_system(self, system_id: str) -> List[Sensor]:
        # Implementation
        pass
```

### 2. Add Custom Query Methods
```python
class AircraftRepository:
    # ... existing methods ...
    
    def find_by_manufacturer_and_operator(
        self,
        manufacturer: str,
        operator: str
    ) -> List[Aircraft]:
        query = """
        MATCH (a:Aircraft {manufacturer: $manufacturer, operator: $operator})
        RETURN a
        """
        result = self.session.run(query, manufacturer=manufacturer, operator=operator)
        return [Aircraft(**record["a"]) for record in result]
```

### 3. Add Computed Properties to Models
```python
class Flight(BaseModel):
    # ... existing fields ...
    
    @property
    def route(self) -> str:
        return f"{self.origin}-{self.destination}"
```

### 4. Add Batch Operations
```python
class AircraftRepository:
    def create_batch(self, aircraft_list: List[Aircraft]) -> List[Aircraft]:
        # Batch insert implementation
        pass
```

## Performance Considerations

### Connection Pooling
The Neo4j driver manages connection pooling automatically. Reuse the same `Neo4jConnection` instance across requests.

### Session Management
Create sessions per transaction or logical unit of work, not per query.

### Query Optimization
- Use indexes for frequently queried properties
- Limit result sets with the `limit` parameter
- Consider pagination for large result sets

### Future Optimizations
- Implement result caching for read-heavy workloads
- Add batch operations for bulk inserts
- Consider async support for concurrent operations

## Summary

The Neo4j Aircraft Client provides:

✅ Clean separation of concerns with clear layers  
✅ Type-safe models with Pydantic validation  
✅ Secure parameterized queries  
✅ Repository pattern for organized data access  
✅ Comprehensive error handling  
✅ Context manager support for resource management  
✅ Integration tests with testcontainers  
✅ Extensible design for custom requirements  

This architecture balances simplicity with best practices, providing a solid foundation for working with aircraft data in Neo4j.
