from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum
from . import Base


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text(1000), nullable=True, index=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO.value)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM.value)
    due_date = Column(DateTime(timezone=True),nullable=False)

    user_id = Column(String(255), nullable=False, index=True)
    assigned_to = Column(String(255), nullable=False, index=True)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    board = relationship("Board",back_populates="tasks")
