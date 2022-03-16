from datetime import datetime
from pydantic import BaseModel


class BookingCreateSchema(BaseModel):
    booked_by: int
    event_id: int
    no_of_tickets: int

    class Config:
        orm_mode = True


class BookingSchema(BookingCreateSchema):
    id: int
