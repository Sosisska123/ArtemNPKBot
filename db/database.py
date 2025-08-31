from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from models.user import Base, User

from settings import config
from typing import Optional
import logging

log = logging.getLogger(__name__)

engine = create_async_engine(url=config.db_url)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # УДАЛИТЬ !!!!!!!!!!!!!!!!!!!! todo
        await conn.run_sync(Base.metadata.create_all)


class Database:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, user_id: int) -> Optional[User]:
        try:
            result = await self.session.execute(
                select(User).where(User.tg_id == user_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            log.error(e)
            return None

    async def create_user(
        self, user_id: int, username: str, name: str, group: str
    ) -> User:
        try:
            user = User(tg_id=user_id, username=username, group=group)
            self.session.add(user)
            await self.session.commit()
            return user
        except SQLAlchemyError as e:
            log.error(e)
            return None

    async def get_notification_state(self, user_id: int) -> Optional[str]:
        try:
            user = await self.get_user(user_id)
            if user:
                return user.notification_state
            return None
        except SQLAlchemyError as e:
            log.error(e)
            return None

    async def update_notification_state(
        self, user_id: int, notification_state: bool
    ) -> bool:
        try:
            user = await self.get_user(user_id)
            if user:
                user.notification_state = notification_state
            return True
        except SQLAlchemyError as e:
            log.error(e)
            return False
