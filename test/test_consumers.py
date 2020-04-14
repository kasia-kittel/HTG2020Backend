
def test_consumers_exist(client):
    maybe_consumer = client.get("/consumer/1")

    json_data = maybe_consumer.get_json()

    assert maybe_consumer.status_code == 200
    assert json_data['username'] == 'Joe'


def test_consumers_not_exist(client):
    maybe_consumer = client.get("/consumer/1000")

    assert maybe_consumer.status_code == 404


def test_consumers_get_bookmarks(client):
    maybe_bookmarks1 = client.get("/consumer/1/bookmarks")

    assert maybe_bookmarks1.status_code == 200
    assert len(maybe_bookmarks1.get_json()) == 2

    maybe_bookmarks20 = client.get("/consumer/20/bookmarks")
    assert maybe_bookmarks20.status_code == 404
    assert len(maybe_bookmarks20.get_json()) == 0


def test_consumers_update_bookmark(client):
    res = client.put("/consumer/1/bookmark/2")
    bookmarks = client.get("/consumer/1/bookmarks")

    assert len(bookmarks.get_json()) == 3
    assert res.status_code == 202

    res = client.put("/consumer/1/bookmark/2")
    bookmarks = client.get("/consumer/1/bookmarks")

    assert len(bookmarks.get_json()) == 2
    assert res.status_code == 202

# TODO investigate why FK are not enforced
# def test_consumers_update_bookmark_that_doesnt_exist(client):
#     res = client.put("/consumer/1/bookmark/2000")
#     assert res.status_code == 404
