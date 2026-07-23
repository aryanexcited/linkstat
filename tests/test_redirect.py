def test_redirect(client):
    response = client.post(
        "/shorten",
        json={
            "original_url": "https://google.com"
        }
    )

    assert response.status_code == 201

    short_code = response.json()["short_code"]

    redirect_response = client.get(
        f"/{short_code}",
        follow_redirects=False
    )

    assert redirect_response.status_code == 302
    assert redirect_response.headers["location"] == "https://google.com/"

def test_unknown_short_code(client):
    response = client.get(
        "/this-code-does-not-exist",
        follow_redirects=False
    )

    assert response.status_code == 404