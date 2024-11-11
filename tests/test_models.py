import os
import sys
sys.path.append(os.getenv("SRC_PATH"))

from vk_api.models import User, Group
import pytest


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

def test_user_creation():
    user = User(uid=1, screen_name="testuser", name="Test User", sex=1, home_town="Test Town").save()
    assert user.uid == 1
    assert user.name == "Test User"
    print("Test `test_user_creation` passed.")

def test_group_creation():
    group = Group(uid=10, name="Test Group", screen_name="testgroup").save()
    assert group.uid == 10
    assert group.name == "Test Group"
    print("Test `test_group_creation` passed.")

def test_follow_relationship():
    user1 = User(uid=1, screen_name="user1", name="User 1", sex=1, home_town="Town 1").save()
    user2 = User(uid=2, screen_name="user2", name="User 2", sex=2, home_town="Town 2").save()
    user1.follows.connect(user2)

    assert len(user1.follows) == 1
    assert user1.follows.all()[0].uid == 2
    print("Test `test_follow_relationship` passed.")

def test_subscribe_relationship():
    user = User(uid=1, screen_name="user", name="User", sex=1, home_town="Town").save()
    group = Group(uid=10, name="Test Group", screen_name="testgroup").save()
    user.subscribes_to.connect(group)

    assert len(user.subscribes_to) == 1
    assert user.subscribes_to.all()[0].uid == 10
    print("Test `test_subscribe_relationship` passed.")
