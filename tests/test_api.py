"""
Tests for GET endpoints using AAA (Arrange-Act-Assert) pattern.
"""
import pytest


class TestRootEndpoint:
    """Test the root GET / endpoint"""
    
    def test_root_redirect(self, client):
        """
        Test that GET / redirects to /static/index.html
        
        Arrange: TestClient ready
        Act: Make GET request to /
        Assert: Verify 307 status and Location header
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert "static/index.html" in response.headers["Location"]


class TestActivitiesEndpoint:
    """Test the GET /activities endpoint"""
    
    def test_get_all_activities(self, client):
        """
        Test that GET /activities returns all 9 activities
        
        Arrange: Fresh activities data loaded
        Act: Make GET request to /activities
        Assert: Verify 200 status and 9 activities returned
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Science Club" in activities
    
    def test_activities_structure(self, client):
        """
        Test that activities have correct structure with all required fields
        
        Arrange: Activities endpoint available
        Act: Get activities and check structure of first activity
        Assert: Verify all required fields present in activity object
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        # Assert
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        
        # Verify field types
        assert isinstance(chess_club["description"], str)
        assert isinstance(chess_club["schedule"], str)
        assert isinstance(chess_club["max_participants"], int)
        assert isinstance(chess_club["participants"], list)
    
    def test_activities_participants_present(self, client):
        """
        Test that activities include participants list with data
        
        Arrange: Activities with populated participants
        Act: Get activities and check participants
        Assert: Verify participants list is not empty for activities
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert - All activities should have at least 2 participants initially
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)
            assert len(activity_data["participants"]) >= 2, \
                f"{activity_name} should have participants"
            # Verify participants are email strings
            for participant in activity_data["participants"]:
                assert "@" in participant, \
                    f"Participant {participant} should be an email"
