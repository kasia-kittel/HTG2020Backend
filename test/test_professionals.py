
def test_professional_exist(client):
    maybe_consumer = client.get("/professional/1")

    json_data = maybe_consumer.get_json()

    assert maybe_consumer.status_code == 200
    assert json_data['username'] == 'doc1'


def test_professional_not_exist(client):
    maybe_consumer = client.get("/professional/1000")

    assert maybe_consumer.status_code == 404


def test_create_criteria():
    from app.professionals import create_criteria_list

    res = create_criteria_list("    aaa; bbbbb;ccc      ddd   ,eee;   ,+ ff +ggg ")
    assert res == ["aaa", "bbbbb", "ccc", "ddd", "eee"]


def test_create_matching_term():
    from app.professionals import create_matching_term

    in1 = ["aaa", "bbbbb", "ccc", "ddd", "eee"]
    res1 = create_matching_term(in1)
    assert res1 == "aaa bbbbb AND (ccc OR ddd OR eee)"

    in2 = ["aaa"]
    res2 = create_matching_term(in2)
    assert res2 == "aaa"

    in3 = ["aaa", "bbbbb"]
    res3 = create_matching_term(in3)
    assert res3 == "aaa bbbbb"