from app.core.events import EventBus
from app.repositories.memory_task_repo import InMemoryTaskRepository
from app.services.command_manager import CommandManager
from app.services.task_service import TaskService


def make_service() -> TaskService:
    bus = EventBus()
    repo = InMemoryTaskRepository()
    cm = CommandManager()
    return TaskService(repo=repo, bus=bus, cm=cm)


def test_add_task_increases_list():
    service = make_service()

    service.add_task("Task A")
    tasks = service.list_tasks()

    assert len(tasks) == 1
    assert tasks[0].title == "Task A"
    assert tasks[0].done is False


def test_complete_undo_redo_flow():
    service = make_service()

    t = service.add_task("Task B")
    assert service.list_tasks()[0].done is False

    service.complete_task(t.id)
    assert service.list_tasks()[0].done is True

    assert service.undo() is True
    assert service.list_tasks()[0].done is False

    assert service.redo() is True
    assert service.list_tasks()[0].done is True


def test_delete_and_undo_restore():
    service = make_service()

    t = service.add_task("Task C")
    assert len(service.list_tasks()) == 1

    service.delete_task(t.id)
    assert len(service.list_tasks()) == 0

    assert service.undo() is True
    tasks = service.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Task C"


def test_undo_empty_returns_false():
    service = make_service()
    assert service.undo() is False


def test_redo_empty_returns_false():
    service = make_service()
    assert service.redo() is False