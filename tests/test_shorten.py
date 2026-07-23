def test_create_short_url(client):
    response = client.post(
        "/shorten",
        json={
            "original_url": "https://google.com"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["original_url"] == "https://google.com/"
    assert isinstance(data["short_code"], str)
    assert data["short_url"].startswith("http")

def test_invalid_url(client):
    response = client.post(
        "/shorten",
        json={
            "original_url": "not-a-url"
        }
    )

    assert response.status_code == 422