from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    VARCHAR,
)
from sqlalchemy import func
from sqlalchemy.orm import relationship

from database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class User(BaseModel):
    """
    User Model
    """

    __tablename__ = "user"

    name = Column(String(100), nullable=False)
    username = Column(VARCHAR(30), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, nullable=False)


class Event(BaseModel):
    """
    Event's data created by admin user.
    """

    __tablename__ = "event"

    created_by = relationship("User")
    user_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String(100), nullable=False)
    summary = Column(String(300), nullable=True)
    max_available_tickets = Column(Integer, nullable=False)
    ticket_price = Column(Float, nullable=False)
    window_open_time = Column(DateTime)
    window_close_time = Column(DateTime)
    is_closed = Column(Boolean, nullable=False)
    bookings = relationship("Booking", cascade="all,delete", backref="ticket")

    def get_available_tickets(self) -> int:
        booked_tickets = 0
        for booking in self.bookings:
            booked_tickets += booking.no_of_tickets
        return self.max_available_tickets - booked_tickets


class Booking(BaseModel):
    """
    This model store event's ticket booked by users.
    """

    __tablename__ = "ticket"

    user = relationship("User")
    booked_by = Column(Integer, ForeignKey("user.id"))
    event = relationship("Event")
    event_id = Column(Integer, ForeignKey("event.id"))
    no_of_tickets = Column(Integer, nullable=False)
