from aiogram import Router, F
from aiogram import types

from db.database import Database
from utils.phrases import ButtonPhrases


router = Router()


@router.callback_query(F.data.is_(ButtonPhrases.rings_command_panel))
async def get_ring_schedule_command(
    callback: types.CallbackQuery, db: Database
) -> None:
    pass
