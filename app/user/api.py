import logging
from typing import List
from app.helpers.auth import Auth
from app.helpers.base_crud import BaseCrud
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.helpers.common import get_db
from app.user.schema import UserLoginModel, UserResponseModel, UserSignupRequestModel
from models import User

user_router = APIRouter()


@cbv(user_router)
class UserAuth:
    """
    API view class for user signup and login.
    """

    session: Session = Depends(get_db)
    user_crud = BaseCrud(User)
    auth_handler = Auth()
    security = HTTPBearer()

    @user_router.post("/signup", response_model=UserResponseModel)
    def signup(self, user_details: UserSignupRequestModel):
        if (
            self.session.query(User)
            .filter(User.username == user_details.username)
            .first()
            != None
        ):
            return JSONResponse({"msg": "Account already exists"}, status_code=409)
        try:
            user_details.password = self.auth_handler.encode_password(
                user_details.password
            )
            return self.user_crud.create(self.session, user_details)
        except Exception as e:
            return JSONResponse({"msg": "Failed to signup user"}, status_code=500)

    @user_router.get("/list", response_model=List[UserResponseModel])
    def list(self):
        return self.user_crud.read_all(self.session)

    @user_router.post("/login")
    def login(self, user_details: UserLoginModel):
        db_user = (
            self.session.query(User)
            .filter(User.username == user_details.username)
            .first()
        )
        if db_user is None:
            return HTTPException(status_code=401, detail="Invalid credentials")
        if not self.auth_handler.verify_password(
            user_details.password, db_user.password
        ):
            return HTTPException(status_code=401, detail="Invalid credentials")

        access_token = self.auth_handler.encode_token(db_user.username)
        refresh_token = self.auth_handler.encode_refresh_token(db_user.username)
        return {"access_token": access_token, "refresh_token": refresh_token}

    @user_router.get("/refresh_token")
    def refresh_token(
        self, credentials: HTTPAuthorizationCredentials = Security(security)
    ):
        refresh_token = credentials.credentials
        new_token = self.auth_handler.refresh_token(refresh_token)
        return {"access_token": new_token}
