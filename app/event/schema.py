from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class EventCreateSchema(BaseModel):
    user_id: int
    name: str
    summary: Optional[str] = None
    max_available_tickets: int
    ticket_price: float
    window_open_time: datetime
    window_close_time: datetime
    is_closed: bool

    class Config:
        orm_mode = True


class EventSchema(EventCreateSchema):
    id: int
