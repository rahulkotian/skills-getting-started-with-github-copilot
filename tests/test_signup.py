"""
Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern.
"""
import pytest


class TestSignupEndpoint:
    """Test the signup POST endpoint"""
    
    def test_valid_signup(self, client):
        """
        Test successful signup of a new participant
        
        Arrange: New email address not yet registered
        Act: POST request to signup endpoint with new email
        Assert: Verify 200 status, success message, and participant added
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert new_email in result["message"]
        assert activity_name in result["message"]
        
        # Verify participant was actually added by fetching activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert new_email in activities[activity_name]["participants"]
    
    def test_duplicate_signup(self, client):
        """
        Test that signup fails when student already registered
        
        Arrange: Email already in participants list
        Act: Attempt POST signup with existing email
        Assert: Verify 400 status and appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={existing_email}"
        )
        
        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "already signed up" in result["detail"].lower()
    
    def test_invalid_activity_signup(self, client):
        """
        Test that signup fails for non-existent activity
        
        Arrange: Activity name that doesn't exist
        Act: POST signup to non-existent activity
        Assert: Verify 404 status and Activity not found error
        """
        # Arrange
        invalid_activity = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "Activity not found" in result["detail"]
    
    def test_signup_integration_participant_count(self, client):
        """
        Test that signup correctly updates participant count and availability
        
        Arrange: Get initial state of activity with known participant count
        Act: Register new participant
        Assert: Verify participant count increased and spots available decreased
        """
        # Arrange
        activity_name = "Programming Class"
        new_email = "integration_test@mergington.edu"
        
        # Get initial state
        initial_response = client.get("/activities")
        initial_activities = initial_response.json()
        initial_count = len(initial_activities[activity_name]["participants"])
        initial_max = initial_activities[activity_name]["max_participants"]
        initial_spots = initial_max - initial_count
        
        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )
        
        # Assert signup was successful
        assert signup_response.status_code == 200
        
        # Get updated state
        updated_response = client.get("/activities")
        updated_activities = updated_response.json()
        updated_count = len(updated_activities[activity_name]["participants"])
        updated_max = updated_activities[activity_name]["max_participants"]
        updated_spots = updated_max - updated_count
        
        # Verify counts changed correctly
        assert updated_count == initial_count + 1
        assert updated_spots == initial_spots - 1
        assert new_email in updated_activities[activity_name]["participants"]
