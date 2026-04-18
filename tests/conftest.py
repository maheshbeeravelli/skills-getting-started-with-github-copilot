import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

# Store original activities state
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client():
    """Provides a test client for the FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state before each test"""
    # Clear current state
    activities.clear()
    # Restore original data
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Cleanup after test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
