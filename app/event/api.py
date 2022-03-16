from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.event.schema import EventCreateSchema, EventSchema
from app.helpers.base_crud import BaseCrud
from app.helpers.common import get_db
from models import Event

event_router = APIRouter()


@cbv(event_router)
class EventCBV:
    """
    Event API view class.
    """

    session: Session = Depends(get_db)
    event_crud = BaseCrud(Event)

    @event_router.get("/", response_model=List[EventSchema])
    def get_events(self, offset: int = 0, limit: int = 100):
        events = self.event_crud.read_all(self.session, offset, limit)
        return events

    @event_router.get("/{event_id}", response_model=EventSchema)
    def get_event(self, event_id: int):
        event = self.event_crud.read(self.session, event_id)
        if event is None:
            raise HTTPException(
                status_code=404, detail=f"event with id {event_id} not found."
            )
        return event

    @event_router.post("/", response_model=EventSchema)
    def create_event(self, schema: EventCreateSchema):
        event = self.event_crud.create(self.session, schema)
        return event

    @event_router.put("/{event_id}", response_model=EventSchema)
    def update_event(self, event_id: int, schema: EventCreateSchema):
        event = self.event_crud.read(self.session, event_id)
        if event is None:
            raise HTTPException(
                status_code=404, detail=f"event with id {event_id} not found."
            )
        event = self.event_crud.update(self.session, event, schema)
        return event

    @event_router.delete("/{event_id}")
    def delete_event(self, event_id: int) -> JSONResponse:
        event = self.event_crud.read(self.session, event_id)
        if event is None:
            raise HTTPException(
                status_code=404, detail=f"event with id {event_id} not found."
            )
        self.event_crud.delete(self.session, event)
        return JSONResponse({"success": True})
