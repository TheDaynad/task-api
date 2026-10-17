from fastapi import FastAPI
from app.api.users import user_router
from app.api.tasks import task_router



app = FastAPI()


app.include_router(user_router)
app.include_router(task_router)



