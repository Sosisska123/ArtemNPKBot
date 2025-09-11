from aiogram import Router, F
from aiogram import types

from db.database import Database
from services.schedule import get_ring_schedule
from utils.mailing_handler import send_rings_to_user
from utils.phrases import ButtonPhrases, Phrases


router = Router()


@router.callback_query(F.data.startswith(ButtonPhrases.rings_command_panel))
async def get_ring_schedule_command(
    callback: types.CallbackQuery, db: Database
) -> None:
    user = await db.get_user(callback.from_user.id)

    schedule, ring_type = await get_ring_schedule(db, user.group)

    if schedule:
        await send_rings_to_user(
            callback.bot,
            user,
            ring_type,
            schedule.file_type,
            [schedule.url],
        )
    else:
        await callback.message.answer(Phrases.no_schedule_text())
