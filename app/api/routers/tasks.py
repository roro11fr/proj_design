from fastapi import APIRouter, HTTPException

from app.core.container import container
from app.schemas.task import TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks():
    tasks = container.task_service.list_tasks()
    return [TaskRead(id=t.id, title=t.title, done=t.done) for t in tasks]


@router.post("", response_model=TaskRead, status_code=201)
def add_task(body: TaskCreate):
    t = container.task_service.add_task(body.title)
    return TaskRead(id=t.id, title=t.title, done=t.done)


@router.post("/{task_id}/complete", status_code=204)
def complete_task(task_id: int):
    try:
        container.task_service.complete_task(task_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    try:
        container.task_service.delete_task(task_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None


@router.post("/undo")
def undo():
    return {"ok": container.task_service.undo()}


@router.post("/redo")
def redo():
    return {"ok": container.task_service.redo()}