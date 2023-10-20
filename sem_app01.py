from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()


class Task(BaseModel):
    id: Optional[int]
    title: str
    description: str
    status: bool = True


tasks = []


@app.get('/tasks', response_model=List[Task])
async def read_tasks():
    return tasks


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
