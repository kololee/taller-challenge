from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session, select
import asyncio
import logging
from app.core.config import settings
from app.models.projects import Project
from app.models.tasks import Task
from app.models.auth import User

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
                await conn.run_sync(SQLModel.metadata.create_all)
                logger.info("Database tables created successfully")
            
            # Create admin user after tables are created - I use a separate connection
            await create_admin_user()
            logger.info("Database initialization completed successfully")
            return
        except Exception as e:
            logger.error(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("All database connection attempts failed")
                raise


async def create_admin_user() -> None:
    """Create the default admin user."""
    try:
        from app.services.auth import AuthService

        await asyncio.sleep(1)
        
        # Use synchronous session for user creation
        from sqlalchemy import create_engine
        sync_url = settings.DATABASE_URL
        if 'postgresql+asyncpg://' in sync_url:
            sync_url = sync_url.replace('postgresql+asyncpg://', 'postgresql://')
        elif '+asyncpg' in sync_url:
            sync_url = sync_url.replace('+asyncpg', '')
        
        logger.info(f"Creating admin user with database URL: {sync_url[:50]}...")
        sync_engine = create_engine(sync_url)
        
        with Session(sync_engine) as session:
            existing_user = session.exec(
                select(User).where(User.username == "admin")
            ).first()
            
            if existing_user:
                logger.info(f"Admin user already exists: {existing_user.username}")
                return

            hashed_password = AuthService.hash_password("1234")
            admin_user = User(
                username="admin",
                hashed_password=hashed_password
            )
            
            session.add(admin_user)
            session.commit()
            session.refresh(admin_user)
            
            logger.info(f"Admin user created successfully: {admin_user.username} (ID: {admin_user.id})")
    except Exception as e:
        logger.error(f"Failed to create admin user: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        pass


async def get_db():
    """Dependency to get database session."""
    async with sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)() as session:
        yield session