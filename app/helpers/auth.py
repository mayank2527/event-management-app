import os
import jwt
from datetime import datetime, timedelta
from app.helpers.base_crud import BaseCrud

from dotenv import load_dotenv, find_dotenv
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.helpers.common import get_db

load_dotenv(find_dotenv())


class Auth:
    hasher = CryptContext(schemes=["bcrypt"])
    secret = os.environ["APP_SECRET_STRING"]
    security = HTTPBearer()

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, username):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=30),
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": username,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "access_token":
                return payload["sub"]
            raise HTTPException(
                status_code=401, detail="Scope for the token is invalid"
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def encode_refresh_token(self, username):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, hours=10),
            "iat": datetime.utcnow(),
            "scope": "refresh_token",
            "sub": username,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "refresh_token":
                username = payload["sub"]
                new_token = self.encode_token(username)
                return new_token
            raise HTTPException(status_code=401, detail="Invalid scope for token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    def has_admin_access(
        self,
        credentials: HTTPAuthorizationCredentials = Security(security),
        session: Session = Depends(get_db),
    ):

        token = credentials.credentials
        try:
            username = self.decode_token(token)
            db_user = session.query(User).filter(User.username == username).first()
            if not db_user.is_admin:
                raise HTTPException(status_code=401, detail="Admin required")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def has_login(
        self,
        credentials: HTTPAuthorizationCredentials = Security(security),
    ):

        token = credentials.credentials
        try:
            self.decode_token(token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
