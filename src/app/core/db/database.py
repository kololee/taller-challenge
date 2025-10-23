from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
import asyncio
import logging
from app.core.config import settings
from app.models.projects import Project
from app.models.tasks import Task

logger = logging.getLogger(__name__)


async_database_url = settings.DATABASE_URL

engine: AsyncEngine = create_async_engine(
    async_database_url,
    echo=settings.DEBUG,
    future=True
)

async def initialize_database() -> None:
    """Initialize the database connection and create tables with retry logic."""
    max_retries = 5
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})")
            async with engine.begin() as conn:
                # Create all tables defined in SQLModel
                await conn.run_sync(SQLModel.metadata.create_all)
                logger.info("Database initialized successfully")
                return
        except Exception as e:
            logger.error(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("All database connection attempts failed")
                raise


async def get_db():
    """Dependency to get database session."""
    async with sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)() as session:
        yield session