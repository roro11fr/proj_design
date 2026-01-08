from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_list_complete_undo_redo():
    # create
    r = client.post("/tasks", json={"title": "API Task"})
    assert r.status_code == 201
    created = r.json()
    task_id = created["id"]

    # list
    r = client.get("/tasks")
    assert r.status_code == 200
    tasks = r.json()
    assert any(t["id"] == task_id and t["title"] == "API Task" for t in tasks)

    # complete
    r = client.post(f"/tasks/{task_id}/complete")
    assert r.status_code == 204

    # undo (should revert completion)
    r = client.post("/tasks/undo")
    assert r.status_code == 200
    assert r.json()["ok"] is True

    # redo (should apply completion again)
    r = client.post("/tasks/redo")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_complete_unknown_task_returns_404():
    r = client.post("/tasks/999/complete")
    assert r.status_code == 404


def test_delete_unknown_task_returns_404():
    r = client.delete("/tasks/999")
    assert r.status_code == 404