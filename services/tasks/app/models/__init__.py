from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from .board import Board
from .project import Project
from .task import Task