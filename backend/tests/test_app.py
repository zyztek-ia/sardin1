def test_health_check(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/health' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/health')
    assert response.status_code == 200
    assert b"OK" in response.data

def test_protected_route_unauthorized(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a protected endpoint is requested without a token
    THEN check that a 401 Unauthorized response is returned
    """
    response = client.get('/api/users')
    assert response.status_code == 401
    assert b"Missing Authorization Header" in response.data
