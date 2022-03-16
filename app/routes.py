from fastapi import APIRouter, Depends

from app.helpers.auth import Auth
from app.user.api import user_router
from app.event.api import event_router
from app.booking.api import booking_router

router = APIRouter()
auth = Auth()


router.include_router(user_router, prefix="/user", tags=["Auth"])
router.include_router(
    event_router,
    prefix="/event",
    tags=["Event"],
    dependencies=[Depends(auth.has_admin_access)],
)
router.include_router(
    booking_router,
    prefix="/booking",
    tags=["Booking"],
    dependencies=[Depends(auth.has_login)],
)
