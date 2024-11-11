from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from vk_api.models import User, Group
from pydantic import BaseModel
from neomodel import db, config
import os

router = APIRouter()

class UserCreate(BaseModel):
    uid: int
    screen_name: str
    name: str
    sex: int
    home_town: str
    follows: list[int]
    subscribes_to: list[int]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_token(token: str = Depends(oauth2_scheme)):
    # В этом примере мы жестко задаем правильный токен (например, "secret-token")
    # В реальном приложении можно проверять его в базе данных или другом хранилище
    # В headers должно быть поле Authorization: Bearer secret-token
    if token != os.getenv("TOKEN"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

@router.get("/nodes/")
async def get_all_nodes():
    users = User.nodes.all()
    groups = Group.nodes.all()
    return {"users": [user.__properties__ for user in users], "groups": [group.__properties__ for group in groups]}

@router.get("/nodes/{id}")
async def get_node_and_relationships(id: int):
    user = User.nodes.get_or_none(uid=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "user": user.__properties__,
        "follows": [f.__properties__ for f in user.follows],
        "subscribes_to": [g.__properties__ for g in user.subscribes_to]
    }

@router.post("/nodes/", dependencies=[Depends(get_current_token)])
async def add_node_and_relationships(user_data: UserCreate):
    user = User(uid=user_data.uid, screen_name=user_data.screen_name, name=user_data.name,
                sex=user_data.sex, home_town=user_data.home_town).save()
    
    for follow_id in user_data.follows:
        followed_user = User.nodes.get_or_none(uid=follow_id)
        if not followed_user:
            followed_user = User(uid=follow_id).save()
        user.follows.connect(followed_user)

    for subscribe_id in user_data.subscribes_to:
        subscribed_group = Group.nodes.get_or_none(uid=subscribe_id)
        if not subscribed_group:
            subscribed_group = Group(uid=subscribe_id).save()
        user.subscribes_to.connect(subscribed_group)

    user.save()
    return {"status": "Node and relationships added"}

@router.delete("/nodes/{id}", dependencies=[Depends(get_current_token)])
async def delete_node_and_relationships(id: int):
    user = User.nodes.get_or_none(uid=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return {"status": "Node and relationships deleted"}