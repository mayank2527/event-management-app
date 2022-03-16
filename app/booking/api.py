from multiprocessing import Event
from typing import List
from app.event.api import EventCBV

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.booking.schema import BookingCreateSchema, BookingSchema
from app.helpers.base_crud import BaseCrud
from app.helpers.common import get_db
from models import Booking, Event

booking_router = APIRouter()


@cbv(booking_router)
class BookingCBV:
    """
    Booking API view class.
    """

    session: Session = Depends(get_db)
    booking_crud = BaseCrud(Booking)
    event_crud = BaseCrud(Event)

    @booking_router.get("/", response_model=List[BookingSchema])
    def get_bookings(self, offset: int = 0, limit: int = 100):
        bookings = self.booking_crud.read_all(self.session, offset, limit)
        return bookings

    @booking_router.get("/{booking_id}", response_model=BookingSchema)
    def get_booking(self, booking_id: int):
        booking = self.booking_crud.read(self.session, booking_id)
        if booking is None:
            raise HTTPException(
                status_code=404, detail=f"booking with id {booking_id} not found."
            )
        return booking

    @booking_router.post("/", response_model=BookingSchema)
    def create_booking(self, schema: BookingCreateSchema):
        event: Event = self.event_crud.read(self.session, schema.event_id)
        print(event)
        if event and (event.get_available_tickets() - schema.no_of_tickets) >= 0:
            booking = self.booking_crud.create(self.session, schema)
            return booking
        raise HTTPException(status_code=400, detail="Tickets not available")

    @booking_router.put("/{booking_id}", response_model=BookingSchema)
    def update_booking(self, booking_id: int, schema: BookingCreateSchema):
        booking = self.booking_crud.read(self.session, booking_id)
        if booking is None:
            raise HTTPException(
                status_code=404, detail=f"booking with id {booking_id} not found."
            )
        booking = self.booking_crud.update(self.session, booking, schema)
        return booking

    @booking_router.delete("/{booking_id}")
    def delete_booking(self, booking_id: int) -> JSONResponse:
        booking = self.booking_crud.read(self.session, booking_id)
        if booking is None:
            raise HTTPException(
                status_code=404, detail=f"booking with id {booking_id} not found."
            )
        self.booking_crud.delete(self.session, booking)
        return JSONResponse({"success": True})
