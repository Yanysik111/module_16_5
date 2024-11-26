from fastapi import FastAPI, status, Body, HTTPException, Path, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated, List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory = 'templates')
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/", response_class=HTMLResponse)
def get_all(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})
@app.get(path='/user/{user_id}', response_class=HTMLResponse)
async def get_users(request: Request, user_id =  int) -> HTMLResponse:
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code= 404, detail='User not found')
    return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id - 1]})


@app.post(path='/user/{username}/{age}', response_model=str)
async def post_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                    age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> str:
    if users:

        new_id = max(user.id for user in users) + 1
    else:
        new_id = 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put(path='/user/{user_id}/{username}/{age}', response_model=str)
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> str:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user

    else:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete(path='/user/{user_id}', response_model=str)
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')]) -> str:
    for i, user in enumerate(users):
        if user.id == user_id:
            return users.pop(i)

    else:
        raise HTTPException(status_code=404, detail='User was not found')