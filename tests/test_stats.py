def test_stats_endpoint(client):
    # Create a short URL
    response = client.post(
        "/shorten",
        json={"original_url": "https://google.com"}
    )

    assert response.status_code == 201

    short_code = response.json()["short_code"]

    # Simulate one click
    client.get(f"/{short_code}", follow_redirects=False)

    # Fetch stats
    stats = client.get(f"/stats/{short_code}")

    assert stats.status_code == 200

    data = stats.json()

    assert data["short_code"] == short_code
    assert data["original_url"] == "https://google.com/"
    assert data["total_clicks"] >= 1
    assert len(data["clicks_last_7_days"]) == 7

def test_stats_invalid_short_code(client):
    response = client.get("/stats/does-not-exist")

    assert response.status_code == 404