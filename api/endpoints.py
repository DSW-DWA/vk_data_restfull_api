from fastapi import APIRouter, HTTPException, Depends
from models import User, Group
from pydantic import BaseModel
from neomodel import db, config

router = APIRouter()

class UserCreate(BaseModel):
    id: int
    screen_name: str
    name: str
    sex: int
    home_town: str

class GroupCreate(BaseModel):
    id: int
    name: str
    screen_name: str

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

@router.post("/nodes/")
async def add_node_and_relationships(user_data: UserCreate, group_data: GroupCreate = None):
    user = User(**user_data.dict()).save()
    if group_data:
        group = Group(**group_data.dict()).save()
        user.subscribes_to.connect(group)
    return {"status": "Node and relationships added"}

@router.delete("/nodes/{id}")
async def delete_node_and_relationships(id: int):
    user = User.nodes.get_or_none(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return {"status": "Node and relationships deleted"}
