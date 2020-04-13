
def test_healthcheck(client):
    assert client.get("/healthcheck").status_code == 200