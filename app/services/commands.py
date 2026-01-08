from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Optional

from app.core.events import EventBus
from app.domain.models import Task
from app.repositories.task_repo import TaskRepository


class Command(Protocol):
    def execute(self) -> None:
        ...

    def undo(self) -> None:
        ...


@dataclass
class AddTaskCommand:
    repo: TaskRepository
    bus: EventBus
    title: str
    created: Optional[Task] = None

    def execute(self) -> None:
        self.created = self.repo.add(self.title)
        self.bus.notify("task_added", {"id": self.created.id, "title": self.created.title})

    def undo(self) -> None:
        if not self.created:
            return
        deleted = self.repo.delete(self.created.id)
        self.bus.notify("task_undone_add", {"id": deleted.id})


@dataclass
class DeleteTaskCommand:
    repo: TaskRepository
    bus: EventBus
    task_id: int
    deleted: Optional[Task] = None

    def execute(self) -> None:
        self.deleted = self.repo.delete(self.task_id)
        self.bus.notify("task_deleted", {"id": self.deleted.id, "title": self.deleted.title})

    def undo(self) -> None:
        if not self.deleted:
            return
        self.repo.restore(self.deleted)
        self.bus.notify("task_restored", {"id": self.deleted.id})


@dataclass
class CompleteTaskCommand:
    repo: TaskRepository
    bus: EventBus
    task_id: int
    prev_done: Optional[bool] = None

    def execute(self) -> None:
        task = self.repo.get(self.task_id)
        if not task:
            raise KeyError(f"Task {self.task_id} not found")

        self.prev_done = task.done
        updated = self.repo.set_done(self.task_id, True)
        self.bus.notify("task_completed", {"id": updated.id})

    def undo(self) -> None:
        if self.prev_done is None:
            return
        updated = self.repo.set_done(self.task_id, self.prev_done)
        self.bus.notify("task_reverted", {"id": updated.id, "done": updated.done})