import asyncio
import logging

from aiogram import Dispatcher

from handlers.default import router as default_router
from handlers.group_selection import router as group_selection_router
from handlers.admin import router as admin_router

from db.database import init_db
from utils.db_dependency import DBDependency

from middlewares.throttling import ThrottlingMiddleware

from vk import vk_schedule as vk_schedule
from vk.schemas.vk_group import KNNVkGroup, NPKVkGroup
from vk.vk_requests import VkRequests

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
    )

    dp.message.middleware(
        ThrottlingMiddleware(session=async_session, ttl=config.ttl_default)
    )
    dp.callback_query.middleware(
        ThrottlingMiddleware(session=async_session, ttl=config.ttl_default)
    )

    # снизу хуита уже

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

    # vk_schedule.create_scheduler(vk_requests, db)

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
