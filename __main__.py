import asyncio
import logging

from aiogram import Dispatcher

from handlers.defaults import router as default_router
from handlers.group_selection import router as group_selection_router
from handlers.admins import router as admin_router

from bot_file import bot
from db.database import init_db, engine
from middlewares.throttling import ThrottlingMiddleware
from settings import config

from sqlalchemy.ext.asyncio import async_sessionmaker

from vk.vk_requests import VkRequests

dp = Dispatcher()
parser = VkRequests()


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

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


async def job():
    pass


if __name__ == "__main__":
    try:
        logging.info("================ Бот запущен ================")
        asyncio.run(start())
    except KeyboardInterrupt:
        logging.info("================ Бот остановлен ================")
    except Exception as e:
        logging.error(f"Ошибка {e}", exc_info=True)
