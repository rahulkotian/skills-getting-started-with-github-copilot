"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint using AAA pattern.
"""
import pytest


class TestDeleteParticipantEndpoint:
    """Test the delete participant DELETE endpoint"""
    
    def test_valid_deletion(self, client):
        """
        Test successful removal of a participant
        
        Arrange: Participant exists in activity
        Act: DELETE request to remove participant
        Assert: Verify 200 status, success message, and participant removed
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"  # Exists in Chess Club
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email_to_remove}"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email_to_remove in result["message"]
        assert activity_name in result["message"]
        
        # Verify participant was actually removed by fetching activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email_to_remove not in activities[activity_name]["participants"]
    
    def test_participant_not_found(self, client):
        """
        Test that deletion fails when participant not signed up
        
        Arrange: Email not in participants list
        Act: Attempt DELETE with email not in activity
        Assert: Verify 400 status and appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        email_not_in_activity = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email_not_in_activity}"
        )
        
        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "not signed up" in result["detail"].lower()
    
    def test_invalid_activity_delete(self, client):
        """
        Test that deletion fails for non-existent activity
        
        Arrange: Activity name that doesn't exist
        Act: DELETE from non-existent activity
        Assert: Verify 404 status and Activity not found error
        """
        # Arrange
        invalid_activity = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "Activity not found" in result["detail"]
    
    def test_delete_integration_participant_count(self, client):
        """
        Test that deletion correctly updates participant count and availability
        
        Arrange: Get initial state of activity with known participant count
        Act: Remove one participant
        Assert: Verify participant count decreased and spots available increased
        """
        # Arrange
        activity_name = "Gym Class"
        email_to_remove = "john@mergington.edu"
        
        # Get initial state
        initial_response = client.get("/activities")
        initial_activities = initial_response.json()
        initial_count = len(initial_activities[activity_name]["participants"])
        initial_max = initial_activities[activity_name]["max_participants"]
        initial_spots = initial_max - initial_count
        
        # Verify email is in participants
        assert email_to_remove in initial_activities[activity_name]["participants"]
        
        # Act
        delete_response = client.delete(
            f"/activities/{activity_name}/participants/{email_to_remove}"
        )
        
        # Assert deletion was successful
        assert delete_response.status_code == 200
        
        # Get updated state
        updated_response = client.get("/activities")
        updated_activities = updated_response.json()
        updated_count = len(updated_activities[activity_name]["participants"])
        updated_max = updated_activities[activity_name]["max_participants"]
        updated_spots = updated_max - updated_count
        
        # Verify counts changed correctly
        assert updated_count == initial_count - 1
        assert updated_spots == initial_spots + 1
        assert email_to_remove not in updated_activities[activity_name]["participants"]
