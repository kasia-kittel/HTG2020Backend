
def test_professional_exist(client):
    maybe_consumer = client.get("/professional/1")

    json_data = maybe_consumer.get_json()

    assert maybe_consumer.status_code == 200
    assert json_data['username'] == 'doc1'


def test_professional_not_exist(client):
    maybe_consumer = client.get("/professional/1000")

    assert maybe_consumer.status_code == 404
