from typing import List, Optional
from app.models.projects import Project
from app.schemas.projects_schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.db.database import get_db_session
from sqlalchemy.orm import Session


def get_projects_by_owner(
    db: Session, owner_id: str, limit: int = 50, offset: int = 0
) -> List[ProjectResponse]:

    db_projects = (
        db.query(Project)
        .filter(Project.owner_id == owner_id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [ProjectResponse.model_validate(project) for project in db_projects]


def get_project_by_id(db: Session, project_id: int) -> Optional[ProjectResponse]:

    db_project = db.query(Project).filter(id=project_id).first()
    if db_project:
        return ProjectResponse.model_validate(db_project)
    return None


def create_project(db: Session, project_data: ProjectCreate) -> ProjectResponse:

    db_project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=project_data.owner_id,
    )

    db.add(db_project)
    db.flush()
    db.refresh(db_project)

    return ProjectResponse.model_validate(db_project)


def update_project(
    db: Session, project_id: int, project_data
) -> Optional[ProjectResponse]:

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


def delete_project(db: Session, project_id: int) -> bool:

    db_project = db.query(Project).filter(id=project_id).first()

    if db_project:
        db.delete(db_project)
        db.flush()
        return True
    else:
        return False
