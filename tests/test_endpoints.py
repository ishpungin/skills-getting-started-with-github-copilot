import pytest
from fastapi import HTTPException
from src.app import get_activities, signup_for_activity, unregister_participant


class TestGetActivities:
    def test_get_activities(self, test_activities, monkeypatch):
        """Test GET /activities returns activities dict"""
        import src.app as app
        monkeypatch.setattr(app, "activities", test_activities)
        
        result = get_activities()
        
        assert isinstance(result, dict)
        assert "Chess Club" in result
        assert "Programming Class" in result
        assert result["Chess Club"]["max_participants"] == 12


class TestSignup:
    def test_signup_for_activity_success(self, test_activities, monkeypatch):
        """Test successful signup appends email to participants"""
        import src.app as app
        monkeypatch.setattr(app, "activities", test_activities)
        
        result = signup_for_activity("Chess Club", "newstudent@mergington.edu")
        
        assert "Signed up" in result["message"]
        assert "newstudent@mergington.edu" in test_activities["Chess Club"]["participants"]
    
    def test_signup_activity_not_found(self, test_activities, monkeypatch):
        """Test signup raises 404 when activity doesn't exist"""
        import src.app as app
        monkeypatch.setattr(app, "activities", test_activities)
        
        with pytest.raises(HTTPException) as exc_info:
            signup_for_activity("Nonexistent Activity", "student@mergington.edu")
        
        assert exc_info.value.status_code == 404
        assert "Activity not found" in exc_info.value.detail
    
    def test_signup_already_registered(self, test_activities, monkeypatch):
        """Test signup raises 400 when student already registered"""
        import src.app as app
        monkeypatch.setattr(app, "activities", test_activities)
        
        with pytest.raises(HTTPException) as exc_info:
            signup_for_activity("Chess Club", "michael@mergington.edu")
        
        assert exc_info.value.status_code == 400
        assert "already signed up" in exc_info.value.detail


class TestUnregister:
    def test_unregister_participant_success(self, test_activities, monkeypatch):
        """Test successful unregister removes email from participants"""
        import src.app as app
        monkeypatch.setattr(app, "activities", test_activities)
        
        result = unregister_participant("Chess Club", "michael@mergington.edu")
        
        assert "Unregistered" in result["message"]
        assert "michael@mergington.edu" not in test_activities["Chess Club"]["participants"]
    
    def test_unregister_activity_not_found(self, test_activities, monkeypatch):
        """Test unregister raises 404 when activity doesn't exist"""
        import src.app as app
        monkeypatch.setattr(app, "activities", test_activities)
        
        with pytest.raises(HTTPException) as exc_info:
            unregister_participant("Nonexistent Activity", "student@mergington.edu")
        
        assert exc_info.value.status_code == 404
        assert "Activity not found" in exc_info.value.detail
    
    def test_unregister_participant_not_found(self, test_activities, monkeypatch):
        """Test unregister raises 404 when participant not in activity"""
        import src.app as app
        monkeypatch.setattr(app, "activities", test_activities)
        
        with pytest.raises(HTTPException) as exc_info:
            unregister_participant("Chess Club", "nonexistent@mergington.edu")
        
        assert exc_info.value.status_code == 404
        assert "Participant not found" in exc_info.value.detail
