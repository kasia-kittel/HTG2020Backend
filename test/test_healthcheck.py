
def test_healthcheck(client, app):
    assert client.get("/healthcheck").status_code == 200