from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)

async_session = async_sessionmaker(bind=engine)


async def get_db():
    async with async_session() as db:
        yield db
