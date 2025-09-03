from aiogram import Router, F
from aiogram import types

from db.database import Database
from filters.is_admin import IsAdmin
from utils.phrases import AdminPhrases


router = Router()


@router.callback_query(F.data.is_(AdminPhrases.approve_schdule_command), IsAdmin())
async def admin_accept_schedule_command(
    callback: types.CallbackQuery, db: Database
) -> None:
    pass


@router.callback_query(F.data.is_(AdminPhrases.reject_schdule_command), IsAdmin())
async def admin_reject_schedule_command(
    callback: types.CallbackQuery, db: Database
) -> None:
    pass


@router.callback_query(F.data.is_(AdminPhrases.edit_schdule_command), IsAdmin())
async def admin_edit_schedule_command(
    callback: types.CallbackQuery, db: Database
) -> None:
    pass
