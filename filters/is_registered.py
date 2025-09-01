from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from utils.db_dependency import DBDependency
from db.database import Database
from utils.phrases import Phrases


class IsRegistered(BaseFilter):
    async def __call__(
        self, event: Message | CallbackQuery, db_dependency: DBDependency
    ) -> bool:
        async with db_dependency.db_session() as session:
            db = Database(session=session)
            user = await db.get_user(event.from_user.id)

            # If user is not registered, send a message
            if not user:
                if isinstance(event, Message):
                    await event.answer(Phrases.registration_required())
                elif isinstance(event, CallbackQuery):
                    await event.answer(Phrases.registration_required(), show_alert=True)
                return False

            return True
