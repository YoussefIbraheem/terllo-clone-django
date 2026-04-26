from pydantic import BaseModel, Field
from datetime import datetime

class EventCreate(BaseModel):
    service: str = Field(...)
    action: str = Field(...)
    user_id: str = Field(...)
    details: str = Field(...)


class EventResponse(BaseModel):

    id: str
    service: str = Field(...)
    action: str = Field(...)
    user_id: str = Field(...)
    details: str = Field(...)
    timestamp: datetime
    
class EventsStats(BaseModel):
    pass