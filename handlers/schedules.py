from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from db.database import Database
from utils.mailing_handler import mail_users
from utils.phrases import ButtonPhrases, Phrases
from filters.is_registered import IsRegistered


router = Router()
# todo MIDDLEWARE КОТОРЫЙ ПЕРЕДАЕТ норм крч user и шлет нахуй не зареганово юзера


@router.message(
    Command(ButtonPhrases.lessons_command),
    F.text.is_(ButtonPhrases.lessons_command_panel),
    IsRegistered(),
)
async def get_schedule(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)

    schedule = await db.get_tomorrow_schedule(user.group)
    if schedule:
        await mail_users(
            Phrases.schedule_text(schedule.date),
            message.bot,
            [user],
            schedule.file_type,
            schedule.url,
        )
    else:
        await message.answer(Phrases.no_schedule_text)


@router.message(
    Command(ButtonPhrases.today_command),
    F.text.is_(ButtonPhrases.today_command),
    IsRegistered(),
)
async def get_tomorrow_schedule(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)

    schedule = await db.get_today_schedule(user.group)
    if schedule:
        await mail_users(
            Phrases.schedule_text(schedule.date),
            message.bot,
            [user],
            schedule.file_type,
            schedule.url,
        )
    else:
        await message.answer(Phrases.no_schedule_text)
