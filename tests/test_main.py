import pytest
import json
from fastapi.testclient import TestClient
from spotify_api.main import app

from spotify_api.models import *

#Create a TestClient instance for testing
client = TestClient(app)


def test_home_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}