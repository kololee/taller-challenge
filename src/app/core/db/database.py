from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from app.core.config import settings
from app.models.projects import Project
from app.models.tasks import Task


async_database_url = settings.DATABASE_URL

engine: AsyncEngine = create_async_engine(
    async_database_url,
    echo=settings.DEBUG,
    future=True
)

async def initialize_database() -> None:
    """Initialize the database connection and create tables."""
    async with engine.begin() as conn:
        # Create all tables defined in SQLModel
        await conn.run_sync(SQLModel.metadata.create_all)