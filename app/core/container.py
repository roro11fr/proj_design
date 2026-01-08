from __future__ import annotations

from app.core.events import EventBus, ConsoleObserver
from app.repositories.memory_task_repo import InMemoryTaskRepository
from app.services.command_manager import CommandManager
from app.services.task_service import TaskService


class Container:
    """
    Simple DI container (manual wiring).
    Keeps app composition in one place.
    """
    def __init__(self) -> None:
        self.bus = EventBus()
        self.bus.subscribe(ConsoleObserver())

        self.repo = InMemoryTaskRepository()
        self.command_manager = CommandManager()

        self.task_service = TaskService(
            repo=self.repo,
            bus=self.bus,
            cm=self.command_manager,
        )


container = Container()