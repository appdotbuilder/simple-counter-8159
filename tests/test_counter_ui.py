import pytest
from nicegui.testing import User
from app.database import reset_db


@pytest.fixture
def new_db():
    """Provide fresh database for each test."""
    reset_db()
    yield
    reset_db()


class TestCounterUI:
    """Test suite for counter UI functionality."""

    async def test_counter_page_loads(self, new_db, user: User):
        """Test that the counter page loads successfully."""
        await user.open("/counter")

        # Check for key UI elements
        await user.should_see("Simple Counter")
        await user.should_see("0")  # Initial counter value
        await user.should_see("Increment")
        await user.should_see("Reset")

    async def test_increment_button_works(self, new_db, user: User):
        """Test that clicking increment button increases the counter."""
        await user.open("/counter")

        # Initial state should show 0
        await user.should_see("0")

        # Click increment button
        user.find("Increment").click()
        await user.should_see("1")

        # Click increment again
        user.find("Increment").click()
        await user.should_see("2")

        # Click increment once more
        user.find("Increment").click()
        await user.should_see("3")

    async def test_reset_button_works(self, new_db, user: User):
        """Test that reset button sets counter back to 0."""
        await user.open("/counter")

        # Increment counter first
        user.find("Increment").click()
        await user.should_see("1")

        user.find("Increment").click()
        await user.should_see("2")

        user.find("Increment").click()
        await user.should_see("3")

        # Now reset
        user.find("Reset").click()
        await user.should_see("0")

    async def test_multiple_increment_reset_cycles(self, new_db, user: User):
        """Test multiple cycles of increment and reset."""
        await user.open("/counter")

        # First cycle
        user.find("Increment").click()
        user.find("Increment").click()
        await user.should_see("2")

        user.find("Reset").click()
        await user.should_see("0")

        # Second cycle
        user.find("Increment").click()
        user.find("Increment").click()
        user.find("Increment").click()
        user.find("Increment").click()
        await user.should_see("4")

        user.find("Reset").click()
        await user.should_see("0")

    async def test_counter_persistence_across_page_refreshes(self, new_db, user: User):
        """Test that counter value persists when page is refreshed."""
        await user.open("/counter")

        # Increment counter
        user.find("Increment").click()
        user.find("Increment").click()
        user.find("Increment").click()
        await user.should_see("3")

        # Refresh page (simulate by reopening)
        await user.open("/counter")
        await user.should_see("3")  # Should still show 3

        # Continue incrementing
        user.find("Increment").click()
        await user.should_see("4")

    async def test_root_redirect(self, new_db, user: User):
        """Test that root path redirects to counter page."""
        await user.open("/")

        # Should see counter page content
        await user.should_see("Simple Counter")
        await user.should_see("Increment")

    async def test_ui_notifications(self, new_db, user: User):
        """Test that UI shows appropriate notifications."""
        await user.open("/counter")

        # Increment should show positive notification
        user.find("Increment").click()
        await user.should_see("Count increased to 1")

        # Reset should show info notification
        user.find("Reset").click()
        await user.should_see("Counter reset to 0")
