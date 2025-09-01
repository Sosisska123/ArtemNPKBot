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


@router.message(Command("add_schedule"))
async def admin_add_schedule_command(message: Message) -> None:
    pass


@router.message(Command("add_default_ring_schedule"))
async def admin_add_default_ring_schedule_command(message: Message) -> None:
    pass


@router.message(Command("add_ring_schedule"))
async def admin_add_ring_schedule_command(message: Message) -> None:
    pass


@router.message(Command("get_var_list"))
async def admin_get_var_list_command(message: Message) -> None:
    pass


@router.message(Command("set_var"))
async def admin_set_var_command(message: Message) -> None:
    pass
