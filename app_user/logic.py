from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from app_user.models import User, Base, StatusEnum
from logs import setup_logger

load_dotenv()

info_logger = setup_logger('logic', 'INFO')
warning_logger = setup_logger('logic', 'WARNING')

FIRST = int(os.getenv('FIRST'))
SECOND = int(os.getenv('SECOND'))
THIRD = int(os.getenv('THIRD'))

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_time_list():
    now = datetime.utcnow().replace(second=0, microsecond=0)
    return {
        1: now - timedelta(minutes=FIRST),
        2: now - timedelta(minutes=FIRST + SECOND),
        3: now - timedelta(minutes=FIRST + SECOND + THIRD)
    }


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
            info_logger.info(f"Create user {user_id}")
            await session.commit()


async def get_users(num):
    session = async_session()
    time_ranges = await get_time_list()
    target_time = time_ranges[num]
    try:
        async with session.begin():
            stmt = select(User).where(func.date_trunc('minute', User.created_at) == target_time,
                                      User.status == StatusEnum.alive)
            result = await session.execute(stmt)
            users = result.scalars().all()
            return [user.id for user in users]
    except Exception as err:
        warning_logger.error(f"get_users error - {err}")
    finally:
        await session.close()


async def update_user_status(user_id: int, new_status: StatusEnum):
    async with async_session() as session:
        async with session.begin():
            # Получение пользователя по ID
            user = await session.get(User, user_id)
            if user:
                user.status = new_status
                user.status_updated_at = datetime.utcnow()

                info_logger.info(f"Update user {user_id} status {new_status}")
                await session.commit()
