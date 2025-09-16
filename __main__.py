import asyncio
import logging

from aiogram import Dispatcher


from handlers.group_selection import router as group_selection_router
from handlers.schedules import router as schedules_router
from handlers.defaults import router as default_router
from handlers.admin import router as admin_router

from callbacks.schedules import router as schedules_callback_router
from callbacks.defaults import router as default_callback_router
from callbacks.admin import router as admin_callback_router

from db.database import init_db
from utils.db_dependency import DBDependency

from middlewares.throttling import ThrottlingMiddleware

from vk import vk_schedule as vk_schedule
from vk.vk_schedule import npk_vk_requests, knn_vk_requests

from bot_file import bot
from settings import config

from tests.handlers_tests import router as test_router


dp = Dispatcher()


logging.basicConfig(
    level=logging.INFO,
    datefmt="%H:%M:%S",
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)


async def start() -> None:
    # Initialize database dependency
    db_dependency = DBDependency()
    async_session = db_dependency.db_session

    # Initialize database
    await init_db(db_dependency._engine)

    dp.include_routers(
        default_router,
        group_selection_router,
        admin_router,
        test_router,
        schedules_router,
        default_callback_router,
        admin_callback_router,
        schedules_callback_router,
    )

    # Add throttling middleware after registration middleware
    dp.message.middleware(
        ThrottlingMiddleware(session=async_session, ttl=config.ttl_default)
    )
    dp.callback_query.middleware(
        ThrottlingMiddleware(session=async_session, ttl=config.ttl_default)
    )

    vk_schedule.create_scheduler(
        npk_vk_requests, knn_vk_requests, db_dependency=db_dependency
    )

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


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
