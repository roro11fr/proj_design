from __future__ import annotations
from typing import Dict, List, Optional
from app.domain.models import Task
from app.repositories.task_repo import TaskRepository

class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1

    def list(self) -> List[Task]:
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def get(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def add(self, title: str) -> Task:
        task = Task(id=self._next_id, title=title, done=False)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def delete(self, task_id: int) -> Task:
        return self._tasks.pop(task_id)  # raises KeyError if missing

    def set_done(self, task_id: int, done: bool) -> Task:
        task = self._tasks[task_id]  # raises KeyError if missing
        task.done = done
        return task

    def restore(self, task: Task) -> None:
        self._tasks[task.id] = task
        self._next_id = max(self._next_id, task.id + 1)