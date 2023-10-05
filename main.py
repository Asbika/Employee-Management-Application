from typing import List
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from models import Gender, Role, User, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(id=UUID("4e277288-5d72-47ae-be06-7c8cc934385e"), first_name="John", last_name="Doe", middle_name="Smith",
         gender=Gender.female, roles=[Role.student]),
    User(id=UUID("2844fc4e-312a-40aa-b6b9-b0df1c064e83"), first_name="Jane", last_name="Smith",
         middle_name="MiddleNameHere", gender=Gender.female, roles=[Role.user])
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    new_user_id = uuid4()
    user.id = new_user_id
    db.append(user)
    return {"id": new_user_id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name

            if user_update.last_name is not None:
                user.last_name = user_update.last_name

            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name

            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )
