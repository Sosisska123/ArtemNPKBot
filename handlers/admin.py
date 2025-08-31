from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db.database import Database

from filters.is_admin import IsAdmin
from keyboards.admin import get_admin_panel
from utils.phrases import AdminPhrases

router = Router()


@router.message(Command("admin"), IsAdmin())
async def admin_panel_command(message: Message, db: Database) -> None:
    await message.reply(
        AdminPhrases.admin_panel(
            await db.get_user_count(),
            await db.get_last_check_time_npk(),
            await db.get_last_check_time_knn(),
        ),
        reply_markup=get_admin_panel(),
    )
