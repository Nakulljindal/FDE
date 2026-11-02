from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

class Task(BaseModel):
    id : int
    task : str
    status : Optional[bool] = False


tasks : List[Task] = []

@app.get("/")
def load_tasks():
    return tasks


@app.post("/create_task")
def add_task(task : Task):
    tasks.append(task)
    return task

@app.put("/update_task")
def update_task(task_id : int, updated_task : Task):
    for index, task in enumerate(tasks):
        if task_id == task.id:
            tasks[index] = updated_task
            return updated_task
    return "Error updating task"

@app.delete("/delete_task/{task_id}")
def delete_task(task_id : int):
    for index, task in enumerate(tasks):
        if task_id == task.id:
            deleted = tasks.pop(index)
            return deleted
    raise HTTPException(status_code=404, detail="Task not found.")


        