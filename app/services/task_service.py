from __future__ import annotations
from typing import List

from app.core.events import EventBus
from app.domain.models import Task
from app.repositories.task_repo import TaskRepository
from app.services.command_manager import CommandManager
from app.services.commands import AddTaskCommand, DeleteTaskCommand, CompleteTaskCommand


class TaskService:
    """
    Business layer: orchestrates use-cases.
    Routers should call this, not repositories directly.
    """
    def __init__(self, repo: TaskRepository, bus: EventBus, cm: CommandManager) -> None:
        self._repo = repo
        self._bus = bus
        self._cm = cm

    def list_tasks(self) -> List[Task]:
        return self._repo.list()

    def add_task(self, title: str) -> Task:
        cmd = AddTaskCommand(repo=self._repo, bus=self._bus, title=title)
        self._cm.run(cmd)
        assert cmd.created is not None
        return cmd.created

    def delete_task(self, task_id: int) -> None:
        self._cm.run(DeleteTaskCommand(repo=self._repo, bus=self._bus, task_id=task_id))

    def complete_task(self, task_id: int) -> None:
        self._cm.run(CompleteTaskCommand(repo=self._repo, bus=self._bus, task_id=task_id))

    def undo(self) -> bool:
        return self._cm.undo()

    def redo(self) -> bool:
        return self._cm.redo()