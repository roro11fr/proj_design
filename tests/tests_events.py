from typing import Dict, Any, List, Tuple

from app.core.events import EventBus
from app.repositories.memory_task_repo import InMemoryTaskRepository
from app.services.command_manager import CommandManager
from app.services.task_service import TaskService


class SpyObserver:
    def __init__(self) -> None:
        self.events: List[Tuple[str, Dict[str, Any]]] = []

    def update(self, event: str, payload: Dict[str, Any]) -> None:
        self.events.append((event, payload))


def test_eventbus_emits_on_add_and_complete():
    bus = EventBus()
    spy = SpyObserver()
    bus.subscribe(spy)

    service = TaskService(
        repo=InMemoryTaskRepository(),
        bus=bus,
        cm=CommandManager()
    )

    t = service.add_task("Obs task")
    assert spy.events[0][0] == "task_added"
    assert spy.events[0][1]["id"] == t.id

    service.complete_task(t.id)
    # the last event should be completion
    assert spy.events[-1][0] == "task_completed"
    assert spy.events[-1][1]["id"] == t.id