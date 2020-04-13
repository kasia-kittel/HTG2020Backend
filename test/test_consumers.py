
def test_consumers_exist(client):
    maybe_consumer = client.get("/consumer/1")

    json_data = maybe_consumer.get_json()

    assert maybe_consumer.status_code == 200
    assert json_data['username'] == 'Joe'


def test_consumers_not_exist(client):
    maybe_consumer = client.get("/consumer/1000")

    assert maybe_consumer.status_code == 404
