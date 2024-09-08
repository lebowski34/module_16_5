from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/", response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/users/{user_id}", response_class=HTMLResponse)
async def read_user(request: Request, user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

@app.post("/user/{username}/{age}", response_model=User)
def create_user(
    username: Annotated[str, Path(title="Enter username", min_length=5, max_length=20, example="UrbanUser")],
    age: Annotated[int, Path(title="Enter age", ge=18, le=120, example=24)]
):
    new_user_id = 1 if not users else users[-1].id + 1
    new_user = User(id=new_user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}", response_model=User)
def update_user(
    user_id: Annotated[int, Path(title="Enter User ID", ge=1, example=1)],
    username: Annotated[str, Path(title="Enter username", min_length=5, max_length=20, example="UrbanProfi")],
    age: Annotated[int, Path(title="Enter age", ge=18, le=120, example=28)]
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}", response_model=User)
def delete_user(user_id: Annotated[int, Path(title="Enter User ID", ge=1, example=2)]):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")
