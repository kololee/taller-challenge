from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from app.core.config import settings


async_database_url = settings.DATABASE_URL

engine: AsyncEngine = create_async_engine(
    async_database_url,
    echo=settings.DEBUG,
    future=True
)

async def initialize_database() -> None:
    """Initialize the database connection."""
    async with engine.begin() as conn:
        # Here I could create tables or run migrations if needed
        pass