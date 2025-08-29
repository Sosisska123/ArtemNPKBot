from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from db.database import Database

from settings import config

from cachetools import TTLCache

from utils.phrases import ErrorPhrases


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, session: async_sessionmaker[AsyncSession], ttl: int = 5):
        self.config = config
        self.session = session
        self.ttl = ttl
        self.user_timeouts = TTLCache(maxsize=10000, ttl=ttl)
        self.notified_users = TTLCache(maxsize=10000, ttl=ttl)
        super().__init__()

    async def __call__(self, handler, event, data):
        event_user = data.get("event_from_user")

        if not event_user:
            return await handler(event, data)

        user = event_user.id

        async with self.session() as session:
            db = Database(session=session)
            data["db"] = db

            # попуск админов
            if user in self.config.admins:
                return await handler(event, data)

            if user in self.user_timeouts:
                if user not in self.notified_users:
                    await event.answer(ErrorPhrases.flood_warning(self.ttl))

                    self.notified_users[user] = None

                return None

            self.user_timeouts[user] = None

            return await handler(event, data)
