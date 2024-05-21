from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from app_user.models import User, Base, StatusEnum

load_dotenv()

FIRST = int(os.getenv('FIRST'))
SECOND = int(os.getenv('SECOND'))
THIRD = int(os.getenv('THIRD'))

now = datetime.utcnow()
time_ranges = {
    1: now - timedelta(minutes=FIRST),
    2: now - timedelta(minutes=FIRST + SECOND),
    3: now - timedelta(minutes=FIRST + SECOND + THIRD)
}

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_user(user_id: int):
    async with async_session() as session:
        user = await session.get(User, user_id)
        if user is None:
            new_user = User(
                id=user_id,
                created_at=datetime.utcnow(),
                status_updated_at=datetime.utcnow()
            )
            session.add(new_user)
            await session.commit()


async def get_users(num):

    async with async_session() as session:
        stmt = select(User).where(User.created_at == time_ranges[num], User.status == StatusEnum.alive)
        result = await session.execute(stmt)
        users = result.scalars().all()
        return [user.id for user in users]


async def update_user_status(user_id: int, new_status: StatusEnum):
    async with async_session() as session:
        async with session.begin():
            # Получение пользователя по ID
            user = await session.get(User, user_id)
            if user:
                user.status = new_status
                user.status_updated_at = datetime.utcnow()
                await session.commit()