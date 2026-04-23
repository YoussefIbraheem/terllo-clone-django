import os

os.environ["DB_URL"] = "sqlite:///:memory:"

import pytest
from app import create_app
import app.services.project_service as project_service


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


def test_projects_list_returns_projects(client, monkeypatch):
    expected = [
        {
            "id": 1,
            "name": "Test Project",
            "description": "Description",
            "owner_id": 10,
        }
    ]

    def fake_get_projects_by_owner(owner_id, limit, offset):
        assert owner_id == "10"
        assert limit == "5"
        assert offset == "0"
        return [DummyModel(expected[0])]

    monkeypatch.setattr("app.apis.project_api.get_projects_by_owner", fake_get_projects_by_owner)

    response = client.get("/api/v1/projects/?owner_id=10&limit=5&offset=0")

    assert response.status_code == 200
    assert response.get_json() == expected


def test_project_details_returns_project(client, monkeypatch):
    expected = {
        "id": 2,
        "name": "Detail Project",
        "description": "Detail description",
        "owner_id": 20,
    }

    monkeypatch.setattr(
        "app.apis.project_api.get_project_by_id",
        lambda project_id: DummyModel(expected),
    )

    response = client.get("/api/v1/projects/2")

    assert response.status_code == 200
    assert response.get_json() == expected


def test_project_create_returns_201(client, monkeypatch):
    payload = {"name": "New Project", "description": "New description", "owner_id": 30}
    expected = {
        "id": 3,
        "name": "New Project",
        "description": "New description",
        "owner_id": 30,
    }

    monkeypatch.setattr(
        "app.apis.project_api.create_project",
        lambda project_data: DummyModel(expected),
    )

    response = client.post("/api/v1/projects/", json=payload)

    assert response.status_code == 201
    assert response.get_json() == expected


def test_project_update_returns_201(client, monkeypatch):
    expected = {
        "id": 4,
        "name": "Updated Project",
        "description": "Updated description",
        "owner_id": 40,
    }

    monkeypatch.setattr(
        "app.apis.project_api.update_project",
        lambda project_id, project_data: DummyModel(expected),
    )

    response = client.put("/api/v1/projects/4", json={"name": "Updated Project"})

    assert response.status_code == 201
    assert response.get_json() == expected


def test_project_delete_returns_200(client, monkeypatch):
    monkeypatch.setattr("app.apis.project_api.delete_project", lambda project_id: True)

    response = client.delete("/api/v1/projects/5")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Project Deleted Successfully!"}


def test_project_delete_not_found_returns_404(client, monkeypatch):
    def fake_delete_project(project_id):
        raise ValueError("Project with id 5 does not exist")

    monkeypatch.setattr("app.apis.project_api.delete_project", fake_delete_project)

    response = client.delete("/api/v1/projects/5")

    assert response.status_code == 404
    assert "error" in response.get_json()
