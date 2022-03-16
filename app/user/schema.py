from pydantic import BaseModel


class UserLoginModel(BaseModel):
    username: str
    password: str


class UserResponseModel(BaseModel):
    name: str
    username: str
    is_admin: bool

    class Config:
        orm_mode = True


class UserSignupRequestModel(BaseModel):
    name: str
    username: str
    password: str
    is_admin: bool = False

    class Config:
        orm_mode = True
