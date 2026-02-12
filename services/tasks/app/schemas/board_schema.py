from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime


class BoardBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Board Name")
    description: Optional[str] = Field(None, description="Board Description")
    project_id:str = Field(...,description="Parent Project")
    columns: List[str] = Field(default=["ToDO","InProgress","Done"])


class BoardCreate(BoardBase):
    pass


class BoardUpdate(BoardBase):
    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Board Name"
    )
    description: Optional[str] = Field(None, description="Board Description")

    model_config = ConfigDict(from_attributes=True)


class BoardResponse(BoardBase):
    id: int = Field(..., description="Board ID")
    created_at: datetime = Field(..., description="Board Creation Date and Time")
    updated_at: Optional[datetime] = Field(
        ..., description="Board Updating Date and Time"
    )