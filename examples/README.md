# Neo4j Client Library Examples

This directory contains example scripts demonstrating how to use the Neo4j Aviation Client Library.

## Prerequisites

Before running these examples, ensure you have:

1. **Neo4j Database Running** - Either:
   - A local Neo4j instance
   - A Neo4j cloud instance (Aura, etc.)
   - Access to the aviation database

2. **Environment Variables Set**:
   ```bash
   export NEO4J_URI="bolt://localhost:7687"
   export NEO4J_USERNAME="neo4j"
   export NEO4J_PASSWORD="your-password"
   export NEO4J_DATABASE="neo4j"  # optional, defaults to "neo4j"
   ```

3. **Client Library Installed**:
   ```bash
   pip install -e .
   ```

## Running Examples

### Basic Usage

```bash
python examples/basic_usage.py
```

This script demonstrates:
- Basic connection to Neo4j
- Finding and listing aircraft
- Creating new entities
- Finding flights for an aircraft
- Querying maintenance events
- Finding significant delays
- Working with airports

## Example Output

```
============================================================
Neo4j Aviation Client Library - Usage Examples
============================================================

Example 1: Basic Connection
----------------------------------------
Total aircraft in database: 60

Example 2: Find Aircraft
----------------------------------------
Found 10 aircraft:
  • N12345: Boeing 737-800 (American Airlines)
  • N67890: Airbus A320 (Delta Airlines)
  ...

Example 3: Create New Aircraft
----------------------------------------
Created aircraft: N-TEST-001
Verified: Found aircraft N-TEST-001
Cleaned up test aircraft

...
```

## Creating Your Own Examples

To create your own examples, follow this pattern:

```python
from neo4j_client import Neo4jConnection, AircraftRepository
import os

# Get connection details from environment
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
username = os.getenv("NEO4J_USERNAME", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password")

# Use context managers for safe resource handling
with Neo4jConnection(uri, username, password) as conn:
    with conn.session() as session:
        # Initialize repository
        repo = AircraftRepository(session)
        
        # Perform operations
        aircraft = repo.find_all(limit=10)
        for a in aircraft:
            print(f"{a.tail_number}: {a.model}")
```

## Security Note

Never hardcode credentials in your scripts. Always use environment variables or secure configuration management systems.

## Need Help?

- See the main [README_CLIENT.md](../README_CLIENT.md) for full documentation
- Check the [tests](../tests/) for more examples
- Review the [DATA_MODEL.md](../DATA_MODEL.md) for schema details
