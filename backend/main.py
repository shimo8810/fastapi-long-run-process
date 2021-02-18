import time
import uuid

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:1234'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Task:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.progress = 0
        self.res = None

    def __call__(self):
        for _ in range(10):
            time.sleep(1)
            self.progress += 10
        self.res = 'result data'


TASKS = {}


@app.post('/task', status_code=202)
async def create_task(background_tasks: BackgroundTasks):
    task = Task()
    TASKS[task.id] = task
    background_tasks.add_task(task)
    return {'task_id': task.id}


@app.get('/task/{task_id}')
async def read_task(task_id: str):
    if task_id not in TASKS:
        return {'message': 'nope'}

    task = TASKS[task_id]

    if task.res is None:
        return {
            'status': 'IN_PROGRESS',
            'progress': task.progress,
            'uri': None
        }
    else:
        return {
            'status': 'SUCCEEDED',
            'progress': 100,
            'uri': f'/task/result/{task.id}'
        }


@app.get('/task/result/{task_id}')
async def read_result(task_id: str):
    if task_id in TASKS:
        task = TASKS[task_id]
        return {'result': task.res}
    else:
        return {'result': 'nothing'}
