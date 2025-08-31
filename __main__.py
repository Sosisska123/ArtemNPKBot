import asyncio
import datetime
import logging

from aiogram import Dispatcher

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.default import router as default_router
from handlers.group_selection import router as group_selection_router
from handlers.admin import router as admin_router

from db.database import Database, init_db, engine

from middlewares.throttling import ThrottlingMiddleware

from schemas.vk_group import KNNVkGroup, NPKVkGroup

from sqlalchemy.ext.asyncio import async_sessionmaker

from utils.mailing_handler import send_to_admin
from vk.vk_requests import VkRequests
from bot_file import bot
from settings import config

dp = Dispatcher()
scheduler = AsyncIOScheduler()


logging.basicConfig(
    level=logging.INFO,
    datefmt="%H:%M:%S",
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)


async def start() -> None:
    async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
    await init_db()

    dp.include_routers(
        default_router,
        group_selection_router,
        admin_router,
    )

    dp.message.middleware(
        ThrottlingMiddleware(session=async_session, ttl=config.ttl_default)
    )
    dp.callback_query.middleware(
        ThrottlingMiddleware(session=async_session, ttl=config.ttl_default)
    )

    # снизу хуита уже

    db = Database(session=async_session)

    npk_group = NPKVkGroup(
        domain=config.vk.group_domains[0],
        group_name_shortcut="нпк",
        start_post_offset=1,
        return_file_type="photo",
    )
    knn_group = KNNVkGroup(
        domain=config.vk.group_domains[1],
        group_name_shortcut="кнн",
        start_post_offset=0,
        return_file_type="doc",
    )

    vk_requests = VkRequests(
        group_schemas=[npk_group, knn_group],
        api_vk_token=config.vk.access_token.get_secret_value(),
        api_ver=config.vk.version,
    )

    # Schedule the daily job at 8:00 AM to start the parsing scheduler
    scheduler.add_job(
        func=start_parsing_scheduler,
        trigger="cron",
        timezone=datetime.timezone(datetime.timedelta(hours=3)),
        hour=9,
        next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=10),
        id="daily_scheduler",
        args=[vk_requests, db],
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


async def start_parsing_scheduler(vk: VkRequests, db: Database):
    """скедулер который запускает скедулер который парсит вквквк every 5 minets"""

    if scheduler.get_job("parsing_job"):
        logging.info(scheduler.get_job("parsing_job"))
        scheduler.remove_job("parsing_job", jobstore=None)

    scheduler.add_job(
        func=parse_job,
        trigger="interval",
        minutes=5,
        id="parsing_job",
        next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=10),
        args=[vk, db],
        max_instances=1,
        coalesce=True,
    )

    scheduler.print_jobs()

    logging.info("Parsing scheduler started at %s AM", datetime.datetime.now())


async def parse_job(vk: VkRequests, db: Database):
    """он уже парсит вк и стопает када чето получает"""
    try:
        result = await vk.check_last_post()

        if result and len(result) > 0:
            # stop🫸
            try:
                scheduler.remove_job("parsing_job", jobstore=None)

                for group in result.values():
                    await send_to_admin(
                        bot=bot,
                        group=group.group_name_shortcut,
                        file_type=group.return_file_type,
                        files=group.files_url,
                    )

                scheduler.print_jobs()

            except Exception as e:
                logging.exception("%s | Job might already be removed", e)

            # Process the result further if needed
            logging.info("PARSING SEXSESSFULL | RESULT: %s", len(result))

    except Exception as e:
        logging.error(f"Error in parse_job: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        logging.info("================ Бот запущен ================")
        asyncio.run(start())
    except KeyboardInterrupt:
        # scheduler.shutdown()
        # await bot.session.close()
        logging.info("================ Бот остановлен ================")
    except Exception as e:
        logging.error(f"Ошибка {e}", exc_info=True)
