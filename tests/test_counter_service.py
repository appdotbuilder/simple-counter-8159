import pytest
from app.counter_service import (
    get_counter,
    create_counter,
    get_or_create_counter,
    increment_counter,
    update_counter,
    reset_counter,
    get_counter_value,
)
from app.models import CounterCreate, CounterUpdate
from app.database import reset_db


@pytest.fixture
def new_db():
    """Provide fresh database for each test."""
    reset_db()
    yield
    reset_db()


class TestCounterService:
    """Test suite for counter service functions."""

    def test_get_counter_nonexistent(self, new_db):
        """Test getting a counter that doesn't exist returns None."""
        result = get_counter("nonexistent")
        assert result is None

    def test_create_counter_default(self, new_db):
        """Test creating a counter with default values."""
        counter_data = CounterCreate(name="test_counter", count=0)
        counter = create_counter(counter_data)

        assert counter.name == "test_counter"
        assert counter.count == 0
        assert counter.id is not None

    def test_create_counter_with_initial_value(self, new_db):
        """Test creating a counter with initial value."""
        counter_data = CounterCreate(name="test_counter", count=42)
        counter = create_counter(counter_data)

        assert counter.name == "test_counter"
        assert counter.count == 42
        assert counter.id is not None

    def test_get_or_create_counter_new(self, new_db):
        """Test get_or_create_counter creates new counter when none exists."""
        counter = get_or_create_counter("new_counter")

        assert counter.name == "new_counter"
        assert counter.count == 0
        assert counter.id is not None

    def test_get_or_create_counter_existing(self, new_db):
        """Test get_or_create_counter returns existing counter."""
        # Create initial counter
        counter_data = CounterCreate(name="existing_counter", count=5)
        initial_counter = create_counter(counter_data)

        # Get or create should return existing
        counter = get_or_create_counter("existing_counter")

        assert counter.id == initial_counter.id
        assert counter.count == 5
        assert counter.name == "existing_counter"

    def test_increment_counter_new(self, new_db):
        """Test incrementing a counter that doesn't exist creates it with count 1."""
        counter = increment_counter("new_counter")

        assert counter.name == "new_counter"
        assert counter.count == 1
        assert counter.id is not None

    def test_increment_counter_existing(self, new_db):
        """Test incrementing an existing counter increases count by 1."""
        # Create initial counter
        counter_data = CounterCreate(name="test_counter", count=10)
        create_counter(counter_data)

        # Increment it
        updated_counter = increment_counter("test_counter")

        assert updated_counter.name == "test_counter"
        assert updated_counter.count == 11

    def test_increment_counter_multiple_times(self, new_db):
        """Test multiple increments work correctly."""
        counter1 = increment_counter("test_counter")
        assert counter1.count == 1

        counter2 = increment_counter("test_counter")
        assert counter2.count == 2

        counter3 = increment_counter("test_counter")
        assert counter3.count == 3

    def test_update_counter_existing(self, new_db):
        """Test updating an existing counter."""
        # Create initial counter
        counter_data = CounterCreate(name="test_counter", count=5)
        create_counter(counter_data)

        # Update it
        update_data = CounterUpdate(count=20)
        updated_counter = update_counter("test_counter", update_data)

        assert updated_counter is not None
        assert updated_counter.count == 20
        assert updated_counter.name == "test_counter"

    def test_update_counter_nonexistent(self, new_db):
        """Test updating a nonexistent counter returns None."""
        update_data = CounterUpdate(count=10)
        result = update_counter("nonexistent", update_data)

        assert result is None

    def test_update_counter_none_values(self, new_db):
        """Test updating counter with None values doesn't change anything."""
        # Create initial counter
        counter_data = CounterCreate(name="test_counter", count=15)
        initial_counter = create_counter(counter_data)

        # Update with None values
        update_data = CounterUpdate(count=None)
        updated_counter = update_counter("test_counter", update_data)

        assert updated_counter is not None
        assert updated_counter.count == initial_counter.count
        assert updated_counter.name == initial_counter.name

    def test_reset_counter_existing(self, new_db):
        """Test resetting an existing counter to 0."""
        # Create counter with non-zero value
        counter_data = CounterCreate(name="test_counter", count=42)
        create_counter(counter_data)

        # Reset it
        reset_counter_result = reset_counter("test_counter")

        assert reset_counter_result is not None
        assert reset_counter_result.count == 0
        assert reset_counter_result.name == "test_counter"

    def test_reset_counter_nonexistent(self, new_db):
        """Test resetting a nonexistent counter returns None."""
        result = reset_counter("nonexistent")
        assert result is None

    def test_get_counter_value_existing(self, new_db):
        """Test getting counter value for existing counter."""
        counter_data = CounterCreate(name="test_counter", count=25)
        create_counter(counter_data)

        value = get_counter_value("test_counter")
        assert value == 25

    def test_get_counter_value_nonexistent(self, new_db):
        """Test getting counter value for nonexistent counter returns 0."""
        value = get_counter_value("nonexistent")
        assert value == 0

    def test_default_counter_name(self, new_db):
        """Test that default counter name works throughout the service."""
        # Test with default name (should be "default")
        counter1 = get_or_create_counter()
        assert counter1.name == "default"
        assert counter1.count == 0

        counter2 = increment_counter()
        assert counter2.name == "default"
        assert counter2.count == 1

        value = get_counter_value()
        assert value == 1

        reset_result = reset_counter()
        assert reset_result is not None
        assert reset_result.count == 0

    def test_counter_persistence(self, new_db):
        """Test that counter values persist across different service calls."""
        # Create and increment counter
        increment_counter("persistent_test")
        increment_counter("persistent_test")
        increment_counter("persistent_test")

        # Retrieve counter separately
        retrieved_counter = get_counter("persistent_test")
        assert retrieved_counter is not None
        assert retrieved_counter.count == 3

        # Get value separately
        value = get_counter_value("persistent_test")
        assert value == 3
