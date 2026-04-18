"""Tests for activity endpoints using AAA (Arrange-Act-Assert) pattern"""


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_returns_all_activities(self, client):
        # Arrange - no setup needed, using default activities

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_contains_expected_activities(self, client):
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class", "Soccer Team"]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity_name in expected_activities:
            assert activity_name in data

    def test_activity_structure(self, client):
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup"""

    def test_successful_signup(self, client, reset_activities):
        # Arrange
        test_email = "newstudent@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {test_email} for {activity_name}"

        # Verify state change
        activities = client.get("/activities").json()
        assert test_email in activities[activity_name]["participants"]

    def test_duplicate_signup_fails(self, client, reset_activities):
        # Arrange
        test_email = "duplicate@mergington.edu"
        activity_name = "Programming Class"
        client.post(f"/activities/{activity_name}/signup", params={"email": test_email})

        # Act - attempt duplicate signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_nonexistent_activity_fails(self, client):
        # Arrange
        test_email = "test@mergington.edu"
        activity_name = "Nonexistent Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_adds_to_participant_list(self, client, reset_activities):
        # Arrange
        test_email = "another@mergington.edu"
        activity_name = "Soccer Team"
        initial_activities = client.get("/activities").json()
        initial_count = len(initial_activities[activity_name]["participants"])

        # Act
        client.post(f"/activities/{activity_name}/signup", params={"email": test_email})

        # Assert
        updated_activities = client.get("/activities").json()
        new_count = len(updated_activities[activity_name]["participants"])
        assert new_count == initial_count + 1


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/participants"""

    def test_successful_unregister(self, client, reset_activities):
        # Arrange
        test_email = "testuser@mergington.edu"
        activity_name = "Basketball Club"
        client.post(f"/activities/{activity_name}/signup", params={"email": test_email})

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 200
        assert f"Unregistered {test_email} from {activity_name}" in response.json()["message"]

        # Verify state change
        activities = client.get("/activities").json()
        assert test_email not in activities[activity_name]["participants"]

    def test_participant_not_found(self, client):
        # Arrange
        test_email = "notinclub@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"

    def test_activity_not_found(self, client):
        # Arrange
        test_email = "anyone@mergington.edu"
        activity_name = "Fake Activity"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_removes_from_list(self, client, reset_activities):
        # Arrange
        test_email = "removal@mergington.edu"
        activity_name = "Drama Club"
        client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
        initial_activities = client.get("/activities").json()
        initial_count = len(initial_activities[activity_name]["participants"])

        # Act
        client.delete(f"/activities/{activity_name}/participants", params={"email": test_email})

        # Assert
        updated_activities = client.get("/activities").json()
        new_count = len(updated_activities[activity_name]["participants"])
        assert new_count == initial_count - 1
