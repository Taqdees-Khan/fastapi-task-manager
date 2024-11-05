from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# In-memory list to store tasks
tasks = []

# Define the Task model
class Task(BaseModel):
    id: int
    title: str
    description: str = None

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Task API. Use /tasks to interact with tasks."}

# Get all tasks
@app.get("/tasks", response_model=list[Task])
def get_tasks():
    logger.info("Fetching all tasks")
    return tasks

# Add a new task
@app.post("/tasks", response_model=Task)
def add_task(task: Task):
    tasks.append(task)
    logger.info(f"Task added: {task}")
    return task

# Delete a task by ID
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    logger.info(f"Task deleted: {task_id}")
    return {"message": "Task deleted"}

# Exception handler for logging errors
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"An error occurred: {exc}")
    return {"detail": "An unexpected error occurred."}
