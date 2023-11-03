import pytest
import json
from fastapi.testclient import TestClient
from main import app

#Create a TestClient instance for testing
client = TestClient(app)

def test_get_artist():
    response = client.get("/artist/radiohead")
    assert response.status_code == 200
    with open("./tests/artist_test.json", "r") as f:
        data = f.read()
    assert response.json() == data



