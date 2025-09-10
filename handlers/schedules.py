import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from db.database import Database

from utils.mailing_handler import (
    send_rings_to_user,
    send_schedule_to_user,
)
from utils.phrases import ButtonPhrases, Phrases

from services.schedule import (
    get_today_schedule,
    get_ring_schedule,
)


router = Router()
log = logging.getLogger(__name__)


@router.message(F.text.startswith(ButtonPhrases.lessons_command_panel))
@router.message(Command(ButtonPhrases.lessons_command))
async def get_schedule_command(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)

    schedule = await db.get_tomorrow_schedule(user.group)

    if schedule is not None:
        await send_schedule_to_user(
            message.bot,
            user,
            schedule.file_type,
            [schedule.url],
        )
    else:
        await message.answer(Phrases.no_schedule_text())


@router.message(F.text.startswith_(ButtonPhrases.today_command_panel))
@router.message(Command(ButtonPhrases.today_command))
async def get_today_schedule_command(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)

    schedule = await get_today_schedule(db, user.group)
    if schedule:
        await send_schedule_to_user(
            message.bot,
            user,
            schedule.file_type,
            [schedule.url],
            date=schedule.date,
        )
    else:
        await message.answer(Phrases.no_schedule_text())


@router.message(F.text.startswith(ButtonPhrases.rings_command_panel))
@router.message(Command(ButtonPhrases.rings_command))
async def get_rings_schedule_command(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)

    schedule, ring_type = await get_ring_schedule(db, user.group)

    if schedule:
        await send_rings_to_user(
            message.bot,
            user,
            ring_type,
            schedule.file_type,
            [schedule.url],
        )
    else:
        await message.answer(Phrases.no_schedule_text())
