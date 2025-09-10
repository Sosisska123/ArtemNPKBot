import datetime
from typing import Optional

from db.database import Database
from models.schedule import Schedule, ScheduleType


# todo кэширование
# todo оповещение


async def get_schedule(
    db: Database, group: str, date: datetime.date
) -> Optional[Schedule]:
    return await db.get_schedule(group, date)


async def get_tomorrow_schedule(db: Database, group: str) -> Optional[Schedule]:
    return await db.get_tomorrow_schedule(group)


async def get_today_schedule(db: Database, group: str) -> Optional[Schedule]:
    return await db.get_today_schedule(group)


async def get_default_ring_schedule(db: Database, group: str) -> Optional[Schedule]:
    return await db.get_ring_schedule(group, ScheduleType.DEFAULT_RING.value)


async def get_ring_schedule(db: Database, group: str) -> list[Optional[Schedule], str]:
    """вернет дефолт еси нету новых этих"""
    ring_type = ScheduleType.RING.value
    schedule = await db.get_ring_schedule(group, ScheduleType.RING.value)

    if not schedule:
        schedule = await db.get_ring_schedule(group, ScheduleType.DEFAULT_RING.value)
        ring_type = ScheduleType.DEFAULT_RING.value

    return schedule, ring_type


async def save_schedule(
    db: Database,
    group: str,
    date: str,
    url: str,
) -> Optional[Schedule]:
    return await db.save_schedule(group, date, url, ScheduleType.REGULAR.value)


async def save_ring_schedule(
    db: Database,
    group: str,
    date: str,
    url: str,
    type: ScheduleType = ScheduleType.RING.value,
) -> Optional[Schedule]:
    return await db.save_ring_schedule(group, date, url, type)


async def update_today_schedule(
    db: Database, group: str, url: str
) -> Optional[Schedule]:
    return await db.update_today_schedule(group, url)


async def update_tomorrow_schedule(
    db: Database, group: str, url: str
) -> Optional[Schedule]:
    return await db.update_tomorrow_schedule(group, url)


async def update_ring_schedule(
    db: Database, group: str, url: str
) -> Optional[Schedule]:
    return await db.update_ring_schedule(group, url)


async def update_default_ring_schedule(
    db: Database,
    group: str,
    url: str,
) -> Optional[Schedule]:
    return await db.update_ring_schedule(group, url, ScheduleType.DEFAULT_RING.value)
