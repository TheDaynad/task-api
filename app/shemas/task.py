from pydantic import BaseModel,ConfigDict

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False
    user_id: int

class TaskResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id : int
    title: str
    description: str | None
    is_completed: bool

class TaskUpdate(BaseModel):
    title: str
    description: str | None
    is_completed: bool


class TaskPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None

