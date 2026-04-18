"""Tests for root endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_root_redirects_to_static_index(client):
    # Arrange - no setup needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in [307, 308]  # Temporary or permanent redirect
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follows_to_index(client):
    # Arrange - allow following redirects

    # Act
    response = client.get("/", follow_redirects=True)

    # Assert
    assert response.status_code == 200
    # Verify we ended up at the static HTML page
    assert "text/html" in response.headers.get("content-type", "")
