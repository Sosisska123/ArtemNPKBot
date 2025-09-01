from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from models.user import Base, User
from models.schedule import Schedule, ScheduleType

from typing import Optional
import logging
import datetime

log = logging.getLogger(__name__)


async def init_db(engine):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # УДАЛИТЬ
        # !!!!!!!!!!!!!!!!!!!! todo
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

    async def get_all_users_from_group(
        self, group: str, ignore_notification=False
    ) -> list[User]:
        try:
            if ignore_notification:
                result = await self.session.execute(
                    select(User).where(User.group == group)
                )
            else:
                result = await self.session.execute(
                    select(User).where(User.group == group, User.notification_state)
                )

            return result.scalars().all()
        except SQLAlchemyError as e:
            log.error(e)
            return None

    # schedule methods

    async def get_schedule(self, group: str, date: datetime.date) -> Optional[Schedule]:
        """Get schedule for a specific date. Looks for modified schedule first, then regular."""
        try:
            # сначала чекает измену в расписании
            result = await self.session.execute(
                select(Schedule).where(
                    Schedule.group == group,
                    Schedule.date == date,
                    Schedule.schedule_type == ScheduleType.MODIFIED.value,
                )
            )
            schedule = result.scalar_one_or_none()

            # If no modified schedule found, look for regular schedule
            if not schedule:
                result = await self.session.execute(
                    select(Schedule).where(
                        Schedule.group == group,
                        Schedule.date == date,
                        Schedule.schedule_type == "regular",
                    )
                )
                schedule = result.scalar_one_or_none()

            return schedule
        except SQLAlchemyError as e:
            log.error(e)
            return None

    async def get_tomorrow_schedule(self, group: str) -> Optional[Schedule]:
        """Get tomorrow's schedule, prioritizing modified over regular."""
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        return await self.get_schedule(group, tomorrow)

    async def get_today_schedule(self, group: str) -> Optional[Schedule]:
        """Get today's schedule, prioritizing modified over regular."""
        today = datetime.date.today()
        return await self.get_schedule(group, today)

    async def save_schedule(
        self, group: str, date: datetime.date, url: str, schedule_type: str
    ) -> Schedule:
        """Save a schedule for a group on a specific date."""
        try:
            # Create new schedule
            schedule = Schedule(
                group=group, date=date, url=url, schedule_type=schedule_type
            )

            self.session.add(schedule)
            await self.session.commit()
            await self.session.refresh(schedule)
            return schedule
        except SQLAlchemyError as e:
            log.error(e)
            await self.session.rollback()
            return None

    async def update_tomorrow_schedule(self, group: str, url: str) -> Schedule:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        return await self.save_schedule(group, tomorrow, url, "modified")
