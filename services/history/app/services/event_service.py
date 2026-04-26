from app.models.event import Event
from app.schemas.event_schema import EventCreate, EventsStats, EventResponse
from typing import Optional

async def get_events(
    service: Optional[str] = None,
    user_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    query = Event.find()

    if service:
        query.find(Event.service == service)
    if user_id:
        query.find(Event.user_id == user_id)

    events = await query.sort(-Event.timestamp).skip(offset).limit(limit).to_list()

    return [EventResponse(**event) for event in events]


async def get_event_by_id(event_id:str):

    event = await Event.get(event_id)

    if not event:
        return None

    return EventResponse(event.model_dump())
