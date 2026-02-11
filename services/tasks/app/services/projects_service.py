from typing import List, Optional
from app.models.projects import Project
from app.schemas.projects_schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.db.database import get_db_session


def get_projects_by_owner(
    owner_id: str, limit: int = 50, offest: int = 0
) -> List[ProjectResponse]:

    with get_db_session() as db:
        db_projects = (
            db.query(Project)
            .filter(Project.owner_id == owner_id)
            .offset(offest)
            .limit(limit)
            .all()
        )

        return [ProjectResponse.model_validate(project) for project in db_projects]


def get_project_by_id(project_id: int) -> Optional[ProjectResponse]:

    with get_db_session() as db:

        db_project = db.query(Project).filter(id=project_id).first()
        if db_project:
            return ProjectResponse.model_validate(db_project)
        return None


def create_project(project_data: ProjectCreate) -> ProjectResponse:
    with get_db_session() as db:
        db_project = Project(
            name=project_data.name,
            description=project_data.description,
            owner_id=project_data.owner_id,
        )

        db.add(db_project)
        db.flush()
        db.refresh(db_project)

        return ProjectResponse.model_validate(db_project)


def update_project(project_id: int, project_data) -> Optional[ProjectResponse]:
    with get_db_session() as db:

        db_project = db.query(Project).filter(id=project_id).first()

        if not db_project:
            return None

        if project_data.name is not None:
            db_project.name = project_data.name

        if project_data.description is not None:
            db_project.description = project_data.description

        db.flush()
        db.refresh(db_project)

        return ProjectResponse.model_validate(db_project)


def delete_project(project_id: int) -> bool:
    with get_db_session() as db:

        db_project = db.query(Project).filter(id=project_id).first()

        if db_project:
            db.delete(db_project)
            db.flush()
            return True
        else:
            return False
