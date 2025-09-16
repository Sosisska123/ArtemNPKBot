import datetime
from aiogram import Bot
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import logging

from db.database import Database
from services.schedule import save_schedule
from utils.date_utils import get_tomorrow_date


from utils.mailing_handler import post_schedule_in_group


logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
id_prefix = "send_new_post_to_group_"


async def scheduled_new_post_to_admin(
    bot: Bot, db: Database, temp_id: int, msg: Message
):
    temp_schedule = await db.get_temp_schedule(temp_id)

    if not temp_schedule:
        logger.error("not temp_schedule error")
        await msg.delete()
        return

    await save_schedule(
        db=db,
        group=temp_schedule.group,
        date=get_tomorrow_date(),
        url=temp_schedule.files_url,
        file_type=temp_schedule.file_type,
    )

    await db.delete_temp_schedule(temp_id)

    await post_schedule_in_group(
        bot=bot,
        db=db,
        group=temp_schedule.group,
        file_type=temp_schedule.file_type,
        files=temp_schedule.files_url,
    )

    await msg.delete()


def create_job(bot: Bot, db: Database, temp_id: int, msg: Message):
    scheduler.add_job(
        func=scheduled_new_post_to_admin,
        trigger="cron",
        timezone=datetime.timezone(datetime.timedelta(hours=3)),
        next_run_time=datetime.datetime.now() + datetime.timedelta(minutes=5),
        id=id_prefix + str(temp_id),
        args=[bot, db, temp_id, msg],
        max_instances=1,
        coalesce=True,
    )


def remove_job(temp_id: int):
    jobs = scheduler.get_jobs()
    for job in jobs:
        if job.id.startswith(id_prefix + str(temp_id)):
            scheduler.remove_job(job.id)
