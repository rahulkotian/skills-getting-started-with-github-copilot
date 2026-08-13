import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Original activities data - used to reset between tests
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Practice team strategies and play friendly matches",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Improve shooting, dribbling, and defensive skills",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, perform scenes, and develop stage confidence",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["zoe@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore drawing, painting, and visual design techniques",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["grace@mergington.edu", "lucas@mergington.edu"]
    },
    "Mathletes": {
        "description": "Solve challenging math problems and compete in contests",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Fridays, 2:00 PM - 3:30 PM",
        "max_participants": 14,
        "participants": ["amelia@mergington.edu", "benjamin@mergington.edu"]
    }
}


@pytest.fixture
def reset_activities():
    """
    Reset activities to original state before each test.
    This ensures test isolation and prevents state leakage between tests.
    """
    # Clear the current activities
    activities.clear()
    
    # Repopulate with original data (deep copy to avoid reference issues)
    for activity_name, activity_data in ORIGINAL_ACTIVITIES.items():
        activities[activity_name] = {
            "description": activity_data["description"],
            "schedule": activity_data["schedule"],
            "max_participants": activity_data["max_participants"],
            "participants": activity_data["participants"].copy()
        }
    
    yield


@pytest.fixture
def client(reset_activities):
    """
    Provide a TestClient instance with reset activities.
    Each test receives a fresh API client with clean data.
    """
    return TestClient(app)
