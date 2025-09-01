from apscheduler.schedulers.asyncio import AsyncIOScheduler

import datetime
import logging

from db.database import Database
from vk.vk_requests import VkRequests

from utils.mailing_handler import send_new_post_to_admin, send_report_to_admin
from bot_file import bot


logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

daily_job_id = "daily_scheduler"
parsing_job_id = "parsing_job"


def create_scheduler(vk_requests: VkRequests, db: Database):
    """ровно в 9 утра создает скедулер который запускает скедулер

    Args:
        vk_requests (VkRequests): вк для запромов
        db (Database): дб для получения лошков
    """
    scheduler.add_job(
        func=start_parsing_scheduler,
        trigger="cron",
        timezone=datetime.timezone(datetime.timedelta(hours=3)),
        hour=9,
        next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=10),
        id=daily_job_id,
        args=[vk_requests, db],
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()


async def start_parsing_scheduler(vk: VkRequests, db: Database):
    """другой скедулер который запускает скедулер который парсит вквквк every 5 minets. чтобы начинать именно ровненько в 9 утра и не спамить запросами каждые 5 минут целые день"""

    if scheduler.get_job("parsing_job"):
        logging.info(scheduler.get_job("parsing_job"))
        scheduler.remove_job("parsing_job", jobstore=None)

    scheduler.add_job(
        func=parse_job,
        trigger="interval",
        minutes=5,
        id=parsing_job_id,
        next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=10),
        args=[vk, db],
        max_instances=1,
        coalesce=True,
    )

    scheduler.print_jobs()

    logging.info("Parsing scheduler started at %s AM", datetime.datetime.now())


async def parse_job(vk: VkRequests, db: Database):
    """a он уже парсит вк и стопает када чето получает"""
    try:
        result = await vk.check_last_post()

        if result is None:
            await send_report_to_admin(bot, "something went wrong with vk requests")

        if result and len(result) > 0:
            try:
                # stop🫸
                scheduler.remove_job(parsing_job_id, jobstore=None)

            except Exception as e:
                logging.exception("%s | Job might already be removed", e)

            for group in result.values():
                await send_new_post_to_admin(
                    bot=bot,
                    group=group.group_name_shortcut,
                    file_type=group.return_file_type,
                    files=group.files_url,
                )

            # Process the result further if needed
            logging.info("PARSING SEXSESSFULL | RESULT: %s", len(result))

        scheduler.print_jobs()

    except Exception as e:
        logging.error(f"Error in parse_job: {e}", exc_info=True)
