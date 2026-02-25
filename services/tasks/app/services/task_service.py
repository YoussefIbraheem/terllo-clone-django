from typing import List, Optional
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.board import Board
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from app.db.database import get_db_session


def get_tasks(
    board_id: int,
    user_id: Optional[str] = None,
    assigned_to: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    limit: int = 50,
    offest: int = 0,
) -> List[TaskResponse]:
    with get_db_session() as db:

        check_board = db.query(Board).filter(Board.id == board_id).first()

        if not check_board:
            raise ValueError(f"Board with ID of {board_id} does not exist!")

        query = db.query(Task).filter(check_board.id == board_id)

        if user_id:
            query = query.filter(Task.user_id == user_id)
        if assigned_to:
            query = query.filter(Task.assigned_to == assigned_to)
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)

        data = query.order_by(Task.created_at.desc()).limit(limit).offset(offest).all()

        return [TaskResponse.model_validate(task) for task in data]


def get_task_by_id(task_id: int) -> Optional[TaskResponse]:
    with get_db_session() as db:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            return TaskResponse.model_validate(task)
        raise ValueError({"error": f"Task with ID {task_id} not found!"})


def get_user_tasks(user_id: int):
    with get_db_session() as db:
        data = (
            db.query(Task)
            .filter(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
            .all()
        )

        return [TaskResponse.model_validate(task) for task in data]


def create_task(task_data: TaskCreate) -> TaskResponse:
    with get_db_session() as db:
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            user_id=task_data.user_id,
            assigned_to=task_data.assigned_to,
            board_id=task_data.board_id,
            due_date=task_data.due_date,
        )

        db.add(db_task)
        db.flush()
        db.refresh(db_task)

        return TaskResponse.model_validate(db_task)


def update_task(task_id: int, task_data: TaskUpdate) -> Optional[TaskResponse]:
    with get_db_session() as db:
        db_task = db.query(Task).filter(Task.id == task_id).first()

        if not db_task:
            raise ValueError(f"Task with ID {task_id} not found!")

        if task_data.title is not None:
            db_task.title = task_data.title
        if task_data.description is not None:
            db_task.description = task_data.description
        if task_data.status is not None:
            db_task.status = task_data.status
        if task_data.priority is not None:
            db_task.priority = task_data.priority
        if task_data.assigned_to is not None:
            db_task.assigned_to = task_data.assigned_to
        if task_data.due_date is not None:
            db_task.due_date = task_data.due_date

        db_task.updated_at = db.func.now()
        db.flush()
        db.refresh(db_task)

        return TaskResponse.model_validate(db_task)


def delete_task(task_id: int) -> bool:
    with get_db_session() as db:
        db_task = db.query(Task).filter(Task.id == task_id).first()

        if not db_task:
            raise ValueError(f"Task with ID {task_id} not found!")

        db.delete(db_task)
        db.flush()
        return True
