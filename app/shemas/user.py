from pydantic import BaseModel,ConfigDict

class UserCreate(BaseModel):
    username: str
    email: str
    is_active: bool = True


class UserUpdate(BaseModel):
    username: str
    email: str
    is_active: bool

class UserPatch(BaseModel):
    username: str | None = None
    email: str | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    is_active: bool

