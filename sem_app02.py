from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()
templates = Jinja2Templates(directory='./templates')


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


users = []


@app.get('/add_users')
async def add_users():
    for i in range(10):
        users.append(User(id=i, name=f'name_{i}', email=f'mail{i}@.mail.ru', password=f'{i + 1}'))
    print(users)
    return {'msg': 'ok'}


@app.get('/users')
async def read_users(request: Request):
    return templates.TemplateResponse('users.html', context={'request': request, "users": users})



@app.get('/tasks/{task_id}', response_model=Task)
async def read_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    return HTTPException(status_code=404, detail="task not found")


@app.post('/tasks', response_model=Task)
async def create_task(task: Task):
    old_id = tasks[-1].id if tasks else 0
    task.id = old_id + 1
    tasks.append(task)
    return task


@app.put('/tasks/{task_id}', response_model=Task)
async def update_task(task_id: int, task: Task):
    for i, task_ in enumerate(tasks):
        if task_id == task_.id:
            tasks[i] = task
            return task
    return HTTPException(status_code=404, detail="task not found")


@app.delete('/tasks/{task_id}', response_model=Task)
async def delete_task(task_id: int):
    for i, task_ in enumerate(tasks):
        if task_id == task_.id:
            tasks[i].status = False
            return {'msg': 'all done'}
    return HTTPException(status_code=404, detail="task not found")