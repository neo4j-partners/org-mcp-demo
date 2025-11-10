"""Tests for Aircraft repository."""

import pytest
from neo4j_client.models import Aircraft
from neo4j_client.repository import AircraftRepository
from neo4j_client.exceptions import NotFoundError


@pytest.fixture
def aircraft_repo(neo4j_connection, clean_database):
    """Provide an AircraftRepository instance for testing."""
    return AircraftRepository(neo4j_connection)


@pytest.fixture
def sample_aircraft():
    """Provide a sample aircraft for testing."""
    return Aircraft(
        aircraft_id="AC9999",
        tail_number="N12345",
        icao24="abcdef",
        model="B777-300ER",
        operator="TestAir",
        manufacturer="Boeing"
    )


class TestAircraftRepository:
    """Tests for AircraftRepository class."""
    
    def test_create_aircraft(self, aircraft_repo, sample_aircraft):
        """Test creating a new aircraft."""
        created = aircraft_repo.create(sample_aircraft)
        
        assert created.aircraft_id == sample_aircraft.aircraft_id
        assert created.tail_number == sample_aircraft.tail_number
        assert created.icao24 == sample_aircraft.icao24
        assert created.model == sample_aircraft.model
        assert created.operator == sample_aircraft.operator
        assert created.manufacturer == sample_aircraft.manufacturer
    
    def test_create_aircraft_idempotent(self, aircraft_repo, sample_aircraft):
        """Test that creating the same aircraft twice uses MERGE."""
        created1 = aircraft_repo.create(sample_aircraft)
        
        # Modify some fields
        sample_aircraft.tail_number = "N99999"
        created2 = aircraft_repo.create(sample_aircraft)
        
        # Should update the existing aircraft
        assert created1.aircraft_id == created2.aircraft_id
        assert created2.tail_number == "N99999"
    
    def test_find_by_id_exists(self, aircraft_repo, sample_aircraft):
        """Test finding an aircraft by ID when it exists."""
        aircraft_repo.create(sample_aircraft)
        
        found = aircraft_repo.find_by_id(sample_aircraft.aircraft_id)
        
        assert found is not None
        assert found.aircraft_id == sample_aircraft.aircraft_id
        assert found.tail_number == sample_aircraft.tail_number
    
    def test_find_by_id_not_exists(self, aircraft_repo):
        """Test finding an aircraft by ID when it doesn't exist."""
        found = aircraft_repo.find_by_id("NONEXISTENT")
        
        assert found is None
    
    def test_find_by_tail_number_exists(self, aircraft_repo, sample_aircraft):
        """Test finding an aircraft by tail number when it exists."""
        aircraft_repo.create(sample_aircraft)
        
        found = aircraft_repo.find_by_tail_number(sample_aircraft.tail_number)
        
        assert found is not None
        assert found.aircraft_id == sample_aircraft.aircraft_id
        assert found.tail_number == sample_aircraft.tail_number
    
    def test_find_by_tail_number_not_exists(self, aircraft_repo):
        """Test finding an aircraft by tail number when it doesn't exist."""
        found = aircraft_repo.find_by_tail_number("N00000")
        
        assert found is None
    
    def test_find_all_empty(self, aircraft_repo):
        """Test finding all aircraft when database is empty."""
        aircraft_list = aircraft_repo.find_all()
        
        assert aircraft_list == []
    
    def test_find_all_with_data(self, aircraft_repo, sample_aircraft):
        """Test finding all aircraft when database has data."""
        aircraft_repo.create(sample_aircraft)
        
        aircraft2 = Aircraft(
            aircraft_id="AC8888",
            tail_number="N54321",
            icao24="123456",
            model="A380",
            operator="MegaAir",
            manufacturer="Airbus"
        )
        aircraft_repo.create(aircraft2)
        
        aircraft_list = aircraft_repo.find_all()
        
        assert len(aircraft_list) == 2
        aircraft_ids = [a.aircraft_id for a in aircraft_list]
        assert "AC9999" in aircraft_ids
        assert "AC8888" in aircraft_ids
    
    def test_find_all_respects_limit(self, aircraft_repo):
        """Test that find_all respects the limit parameter."""
        # Create 5 aircraft
        for i in range(5):
            aircraft = Aircraft(
                aircraft_id=f"AC{i}",
                tail_number=f"N{i}",
                icao24=f"icao{i}",
                model="B737",
                operator="TestAir",
                manufacturer="Boeing"
            )
            aircraft_repo.create(aircraft)
        
        aircraft_list = aircraft_repo.find_all(limit=3)
        
        assert len(aircraft_list) == 3
    
    def test_find_by_operator(self, aircraft_repo, sample_aircraft):
        """Test finding aircraft by operator."""
        aircraft_repo.create(sample_aircraft)
        
        aircraft2 = Aircraft(
            aircraft_id="AC8888",
            tail_number="N54321",
            icao24="123456",
            model="A380",
            operator="TestAir",  # Same operator
            manufacturer="Airbus"
        )
        aircraft_repo.create(aircraft2)
        
        aircraft3 = Aircraft(
            aircraft_id="AC7777",
            tail_number="N11111",
            icao24="999999",
            model="B787",
            operator="OtherAir",  # Different operator
            manufacturer="Boeing"
        )
        aircraft_repo.create(aircraft3)
        
        test_air_aircraft = aircraft_repo.find_by_operator("TestAir")
        
        assert len(test_air_aircraft) == 2
        assert all(a.operator == "TestAir" for a in test_air_aircraft)
    
    def test_find_by_manufacturer(self, aircraft_repo, sample_aircraft):
        """Test finding aircraft by manufacturer."""
        aircraft_repo.create(sample_aircraft)
        
        aircraft2 = Aircraft(
            aircraft_id="AC8888",
            tail_number="N54321",
            icao24="123456",
            model="B787",
            operator="MegaAir",
            manufacturer="Boeing"  # Same manufacturer
        )
        aircraft_repo.create(aircraft2)
        
        aircraft3 = Aircraft(
            aircraft_id="AC7777",
            tail_number="N11111",
            icao24="999999",
            model="A380",
            operator="OtherAir",
            manufacturer="Airbus"  # Different manufacturer
        )
        aircraft_repo.create(aircraft3)
        
        boeing_aircraft = aircraft_repo.find_by_manufacturer("Boeing")
        
        assert len(boeing_aircraft) == 2
        assert all(a.manufacturer == "Boeing" for a in boeing_aircraft)
    
    def test_update_aircraft(self, aircraft_repo, sample_aircraft):
        """Test updating an existing aircraft."""
        aircraft_repo.create(sample_aircraft)
        
        # Update fields
        sample_aircraft.tail_number = "N99999"
        sample_aircraft.operator = "NewAir"
        
        updated = aircraft_repo.update(sample_aircraft)
        
        assert updated.aircraft_id == sample_aircraft.aircraft_id
        assert updated.tail_number == "N99999"
        assert updated.operator == "NewAir"
        
        # Verify in database
        found = aircraft_repo.find_by_id(sample_aircraft.aircraft_id)
        assert found.tail_number == "N99999"
        assert found.operator == "NewAir"
    
    def test_update_nonexistent_aircraft(self, aircraft_repo, sample_aircraft):
        """Test updating an aircraft that doesn't exist."""
        with pytest.raises(NotFoundError):
            aircraft_repo.update(sample_aircraft)
    
    def test_delete_aircraft(self, aircraft_repo, sample_aircraft):
        """Test deleting an aircraft."""
        aircraft_repo.create(sample_aircraft)
        
        deleted = aircraft_repo.delete(sample_aircraft.aircraft_id)
        
        assert deleted is True
        
        # Verify it's gone
        found = aircraft_repo.find_by_id(sample_aircraft.aircraft_id)
        assert found is None
    
    def test_delete_nonexistent_aircraft(self, aircraft_repo):
        """Test deleting an aircraft that doesn't exist."""
        deleted = aircraft_repo.delete("NONEXISTENT")
        
        assert deleted is False
