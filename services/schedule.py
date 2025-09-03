import datetime
from typing import Optional

from db.database import Database
from models.schedule import Schedule, ScheduleType


# todo кэширование


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


async def get_ring_schedule(db: Database, group: str) -> Optional[Schedule]:
    schedule = await db.get_ring_schedule(group, ScheduleType.RING.value)

    if not schedule:
        schedule = await db.get_ring_schedule(group, ScheduleType.DEFAULT_RING.value)

    return schedule


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
    pass


async def save_schedule(
    db: Database,
    group: str,
    date: datetime.date,
    url: str,
) -> Optional[Schedule]:
    pass


async def save_ring_schedule(
    db: Database,
    group: str,
    url: str,
) -> Optional[Schedule]:
    pass
