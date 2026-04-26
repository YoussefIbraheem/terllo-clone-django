from beanie import Document
from typing import Dict, Any
from datetime import datetime , timezone

class Event(Document):
    
    service: str
    action: str
    user_id: str
    details: Dict[str, Any]
    timestamp: datetime = datetime.now(timezone.utc)
    
    class Settings:
        name =  "events"
    
