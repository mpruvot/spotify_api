from spotify_api.oauth import get_token


def test_token():
    token = get_token()
    assert isinstance(token, str)
    assert len(token) > 0