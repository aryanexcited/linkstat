def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["ok", "healthy"]

def test_create_short_url(client):
    response = client.post(
        "/shorten",
        json={
            "original_url": "https://google.com"
        }
    )

    assert response.status_code in (200, 201)
    data = response.json()

    assert data["original_url"] == "https://google.com/"
    assert isinstance(data["short_code"], str)
    assert data["short_url"].startswith("http")
    assert "created_at" in data

def test_redirect(client):
    # Create a short URL
    response = client.post(
        "/shorten",
        json={
            "original_url": "https://google.com"
        }
    )

    assert response.status_code == 201

    short_code = response.json()["short_code"]

    # Follow the redirect manually
    redirect_response = client.get(
        f"/{short_code}",
        follow_redirects=False
    )

    assert redirect_response.status_code == 302
    assert redirect_response.headers["location"] == "https://google.com/"