import os
import sys
sys.path.append(os.getenv("SRC_PATH"))
print(sys.path)

from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from vk_api import endpoints
from vk_api.database import Database
from vk_api.models import User, Group
import os


db = Database()
app = FastAPI()
app.include_router(endpoints.router)

client = TestClient(app)

AUTH_HEADER = {"Authorization": f'Bearer {os.getenv("TOKEN")}'}

@pytest.fixture(autouse=True)
def setup_and_teardown():
    for node in User.nodes.all():
        node.delete()
    for node in Group.nodes.all():
        node.delete()
    yield
    for node in User.nodes.all():
        node.delete()
    for node in Group.nodes.all():
        node.delete()

def test_get_all_nodes():
    response = client.get("/nodes/")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert "groups" in data
    print("Test `test_get_all_nodes` passed.")

def test_add_node_and_relationships():
    response = client.post(
        "/nodes/",
        json={
            "uid": 1,
            "screen_name": "testuser",
            "name": "Test User",
            "sex": 1,
            "home_town": "Test Town",
            "follows": [],
            "subscribes_to": [10]
        },
        headers=AUTH_HEADER
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "Node and relationships added"}
    print("Test `test_add_node_and_relationships` passed.")

def test_get_node_and_relationships():
    user = User(uid=1, screen_name="testuser", name="Test User", sex=1, home_town="Test Town").save()
    group = Group(uid=10, name="Test Group", screen_name="testgroup").save()
    user.subscribes_to.connect(group)
    user.save()

    response = client.get("/nodes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["name"] == "Test User"
    assert len(data["subscribes_to"]) == 1
    print("Test `test_get_node_and_relationships` passed.")

def test_delete_node_and_relationships():
    user = User(uid=2, screen_name="testuser2", name="Test User 2", sex=1, home_town="Test Town").save()

    
    response = client.delete("/nodes/2", headers=AUTH_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "Node and relationships deleted"}
    print("Test `test_delete_node_and_relationships` passed.")

def test_unauthorized_access():
    response = client.post("/nodes/", json={
        "user_data": {
            "uid": 3,
            "screen_name": "unauthorized",
            "name": "Unauthorized User",
            "sex": 1,
            "home_town": "Nowhere",
            "follows": [],
            "subscribes_to": []
        }
    })
    assert response.status_code == 401
    print("Test `test_unauthorized_access` passed with expected Unauthorized status.")
