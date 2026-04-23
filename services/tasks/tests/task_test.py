import os

os.environ["DB_URL"] = "sqlite:///:memory:"

import pytest
from app import create_app
import app.services.task_service as task_service
from app.models.task import TaskStatus, TaskPriority

class DummyModel:
    def __init__(self, data):
        self._data = data

    def model_dump(self):
        return self._data


@pytest.fixture
def client():
    os.environ["DB_URL"] = "sqlite:///:memory:"
    from app.db.database import create_tables

    create_tables()
    app = create_app()
    app.testing = True
    return app.test_client()


def test_tasks_list_returns_tasks(client, monkeypatch):
    expected = [
        {
            "id": 1,
            "title": "Task One",
            "description": "Task description",
            "status": TaskStatus.TODO.value,
            "priority": TaskPriority.MEDIUM.value,
            "user_id": "user-1",
            "assigned_to": "assignee-1",
            "board_id": 21,
            "due_date": "2024-05-01T00:00:00",
            "created_at": "2024-05-01T00:00:00",
            "updated_at": None,
        }
    ]

    def fake_get_tasks(board_id, user_id, assigned_to, status, priority, limit, offset):
        assert board_id == "21"
        assert user_id == "user-1"
        assert assigned_to == "assignee-1"
        assert status == "TODO"
        assert priority == "MEDIUM"
        assert limit == "10"
        assert offset == "0"
        return [DummyModel(expected[0])]

    monkeypatch.setattr("app.apis.task_api.get_tasks", fake_get_tasks)

    response = client.get(
        "/api/v1/tasks/?board_id=21&user_id=user-1&assigned_to=assignee-1&status=TODO&priority=MEDIUM&limit=10&offset=0"
    )

    assert response.status_code == 200
    assert response.get_json() == expected


def test_task_get_returns_task(client, monkeypatch):
    expected = {
        "id": 2,
        "title": "Task Two",
        "description": "Another task",
        "status": TaskStatus.IN_PROGRESS.value,
        "priority": TaskPriority.HIGH.value,
        "user_id": "user-2",
        "assigned_to": "assignee-2",
        "board_id": 22,
        "due_date": "2024-06-01T00:00:00",
        "created_at": "2024-06-01T00:00:00",
        "updated_at": None,
    }

    monkeypatch.setattr(
        "app.apis.task_api.get_task_by_id", lambda task_id: DummyModel(expected)
    )

    response = client.get("/api/v1/tasks/2")

    assert response.status_code == 200
    assert response.get_json() == expected


def test_task_create_returns_task(client, monkeypatch):
    payload = {
        "title": "New Task",
        "description": "New task description",
        "status": TaskStatus.TODO.value,
        "priority": TaskPriority.LOW.value,
        "user_id": "user-3",
        "assigned_to": "assignee-3",
        "board_id": 23,
        "due_date": "2024-07-01T00:00:00",
    }
    expected = {
        "id": 3,
        **payload,
    }

    monkeypatch.setattr(
        "app.apis.task_api.create_task", lambda task_data: DummyModel(expected)
    )

    response = client.post("/api/v1/tasks/", json=payload)

    assert response.status_code == 200
    assert response.get_json() == expected


def test_task_update_returns_task(client, monkeypatch):
    expected = {
        "id": 4,
        "title": "Updated Task",
        "description": "Updated description",
        "status": TaskStatus.DONE.value,
        "priority": TaskPriority.HIGH.value,
        "user_id": "user-4",
        "assigned_to": "assignee-4",
        "board_id": 24,
        "due_date": "2024-08-01T00:00:00",
    }

    monkeypatch.setattr(
        "app.apis.task_api.update_task", lambda task_id, task_data: DummyModel(expected)
    )

    response = client.put("/api/v1/tasks/4", json={"title": "Updated Task"})

    assert response.status_code == 200
    assert response.get_json() == expected


def test_task_delete_returns_200(client, monkeypatch):
    monkeypatch.setattr("app.apis.task_api.delete_task", lambda task_id: True)

    response = client.delete("/api/v1/tasks/5")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Task deleted successfully!"}


def test_task_update_no_data_returns_400(client):
    response = client.put("/api/v1/tasks/6",json={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "No Data Provided"}
