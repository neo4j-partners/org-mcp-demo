# Examples

This directory contains example scripts demonstrating the Neo4j Aviation Client.

## basic_usage.py

Demonstrates basic operations with the Neo4j Aviation Client:
- Connecting to the database
- Querying aircraft, airports, and flights
- Finding maintenance events
- Using the repository pattern

### Running the Example

Set the required environment variables:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
export NEO4J_DATABASE="neo4j"  # optional, defaults to "neo4j"
```

Then run the script:

```bash
python examples/basic_usage.py
```

### Expected Output

The script demonstrates:
1. Listing sample aircraft in the fleet
2. Listing airports with location data
3. Finding flights for a specific aircraft
4. Querying critical maintenance events
5. Looking up aircraft by tail number
6. Retrieving maintenance history for an aircraft

### Sample Output

```
======================================================================
Neo4j Aviation Client - Example Usage
======================================================================

1. Sample Aircraft in Fleet:
----------------------------------------------------------------------
  • N95040A - Boeing B737-800
    Operator: ExampleAir
  • N30268B - Airbus A320-200
    Operator: SkyWays
  • N54980C - Airbus A321neo
    Operator: RegionalCo

2. Sample Airports:
----------------------------------------------------------------------
  • LAX/KLAX - Los Angeles International Airport
    Location: Los Angeles, USA (33.9425, -118.4081)
  • JFK/KJFK - John F. Kennedy International Airport
    Location: New York, USA (40.6413, -73.7781)
  
3. Recent Flights for N95040A:
----------------------------------------------------------------------
  • AA100: LAX → JFK
    Departure: 2024-01-15T10:00:00
  • AA200: JFK → ORD
    Departure: 2024-01-15T18:30:00

4. Critical Maintenance Events:
----------------------------------------------------------------------
  • Event ME001
    Fault: Engine temperature high
    Aircraft: AC001
    Reported: 2024-01-10T12:00:00
    Action: Replaced temperature sensor

...
======================================================================
Example completed successfully!
======================================================================
```

## Customizing the Examples

You can modify the example scripts to:
- Query different entities
- Test CRUD operations (create, update, delete)
- Explore relationships between entities
- Practice writing Cypher queries through the repository pattern
