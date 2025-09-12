from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update

from models.user import Base, User
from models.schedule import Schedule, ScheduleType
from models.temp_schedule import TempSchedule

from typing import Optional
import logging
import datetime

from utils.date_utils import get_today_date, get_tomorrow_date

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

    async def create_user(self, user_id: int, username: str, group: str) -> User:
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
                await self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            log.error(e)
            await self.session.rollback()
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
    async def save_schedule(
        self,
        group: str,
        date: str,
        url: str,
        file_type: str,
        schedule_type: str = ScheduleType.REGULAR.value,
    ) -> Schedule:
        """Common method for saving schedule


        Args:
            group (str): Group name
            date (str): Schedule date
            url (str): Schedule URL (VK)
            file_type (str): Used for bot proper file sending. One of: 'photo' | 'doc'.
            schedule_type (str, optional): Type of schedule, can be modified or regular. Modified type has more priority. Defaults to ScheduleType.REGULAR.value.

        Returns:
            Schedule: The new schedule object
        """
        try:
            if file_type not in ("photo", "doc"):
                raise ValueError("file_type must be 'photo' or 'doc'")

            schedule = Schedule(
                group=group,
                url=url,
                date=date,
                schedule_type=schedule_type,
                file_type=file_type,
            )

            self.session.add(schedule)
            await self.session.commit()
            return schedule
        except SQLAlchemyError as e:
            log.error(e)
            await self.session.rollback()
            return None

    async def get_schedule(self, group: str, date: datetime.date) -> Optional[Schedule]:
        """Common method for getting schedule. Returns the modified schedule if it exists

        Args:
            group (str): group name
            date (datetime.date): date of the schedule

        Returns:
            Optional[Schedule]: Schedule if found, otherwise None
        """

        try:
            # сначала чекает измену  в расписании
            result = await self.session.execute(
                select(Schedule).where(
                    Schedule.group == group,
                    Schedule.date == date,
                    Schedule.schedule_type == ScheduleType.MODIFIED.value,
                )
            )
            schedule = result.scalar_one_or_none()

            if not schedule:
                result = await self.session.execute(
                    select(Schedule).where(
                        Schedule.group == group,
                        Schedule.date == date,
                        Schedule.schedule_type == ScheduleType.REGULAR.value,
                    )
                )
                schedule = result.scalar_one_or_none()

            return schedule
        except SQLAlchemyError as e:
            log.error(e)
            return None

    async def get_tomorrow_schedule(self, group: str) -> Optional[Schedule]:
        """Shortcut for get_schedule(group, get_tomorrow_date())

        Args:
            group (str): group name

        Returns:
            Optional[Schedule]: The new schedule object
        """

        return await self.get_schedule(group, get_tomorrow_date())

    async def get_today_schedule(self, group: str) -> Optional[Schedule]:
        """Shortcut for get_schedule(group, get_today_date())

        Args:
            group (str): group name

        Returns:
            Optional[Schedule]: The new schedule object
        """

        return await self.get_schedule(group, get_today_date())

    async def update_schedule(self, group: str, date: str, url: str) -> Schedule:
        """Updates `URL` of the certain schedule. The new `URL` must match to the `file_type` of its schedule


        Args:
            group (str): The group of the schedule that needs to be updated
            date (str): The date of the schedule that needs to be updated
            url (str): URL Link to the new schedule


        Returns:
            Schedule: The updated schedule object
        """
        try:
            result = await self.session.execute(
                update(Schedule)
                .where(
                    Schedule.group == group,
                    Schedule.date == date,
                    Schedule.schedule_type.in_(
                        [ScheduleType.REGULAR.value, ScheduleType.MODIFIED.value]
                    ),
                )
                .values(
                    url=url,
                    schedule_type=ScheduleType.MODIFIED.value,
                )
            )

            await self.session.commit()
            return result
        except SQLAlchemyError as e:
            log.error(e)
            await self.session.rollback()
            return None

    # - - - rings

    async def get_ring_schedule(
        self, group: str, type: ScheduleType = ScheduleType.DEFAULT_RING.value
    ) -> Optional[Schedule]:
        try:
            if type == ScheduleType.RING.value:
                result = await self.session.execute(
                    select(Schedule).where(
                        Schedule.group == group,
                        Schedule.schedule_type == type,
                        Schedule.date == get_tomorrow_date(),
                    )
                )
            else:
                result = await self.session.execute(
                    select(Schedule).where(
                        Schedule.group == group,
                        Schedule.schedule_type == type,
                    )
                )

            schedule = result.scalar()

            return schedule

        except SQLAlchemyError as e:
            log.error(e)
            return None

    async def save_ring_schedule(
        self,
        group: str,
        date: str,
        url: str,
        type: ScheduleType = ScheduleType.RING.value,
    ) -> Schedule:
        await self.save_schedule(group, date, url, type)

    async def update_ring_schedule(
        self,
        group: str,
        url: str,
    ) -> Schedule:
        return await self.save_schedule(
            group, get_today_date(), url, ScheduleType.RING.value
        )

    # - - - schedule До проверки

    async def save_temp_schedule(
        self, group: str, file_type: str, files_url: str
    ) -> TempSchedule:
        try:
            temp_schedule = TempSchedule(
                group=group,
                file_type=file_type,
                files_url=files_url,  # todo чтобы хрнаить списком нужно json.dumps(files_url) и какой-то мусор чтобы список был
            )

            self.session.add(temp_schedule)
            await self.session.commit()
            # Remove refresh to avoid issues with closed session
            # await self.session.refresh(temp_schedule)

            return temp_schedule
        except SQLAlchemyError as e:
            log.error(e)

            if not self.session.in_transaction():
                await self.session.rollback()
            return None

    async def get_temp_schedule(self, temp_id: int) -> Optional[TempSchedule]:
        try:
            result = await self.session.execute(
                select(TempSchedule).where(TempSchedule.id == temp_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            log.error(e)
            return None

    async def delete_temp_schedule(self, temp_id: int) -> bool:
        try:
            temp_schedule = await self.get_temp_schedule(temp_id)

            if temp_schedule:
                await self.session.delete(temp_schedule)

                await self.session.commit()

                return True
            return False
        except SQLAlchemyError as e:
            log.error(e)

            if not self.session.in_transaction():
                await self.session.rollback()
            return False

    async def clear_temp_schedules(self) -> bool:
        try:
            await self.session.execute(TempSchedule.__table__.delete())

            await self.session.commit()

            return True
        except SQLAlchemyError as e:
            log.error(e)
            await self.session.rollback()
            return False
