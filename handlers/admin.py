import logging
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from db.database import Database

from filters.is_admin import IsAdmin
from keyboards.admin import main_admin_panel
from utils.phrases import AdminPhrases, ErrorPhrases

router = Router()
log = logging.getLogger(__name__)


@router.message(Command("admin"), IsAdmin())
async def admin_panel_command(message: Message, db: Database) -> None:
    await message.reply(
        AdminPhrases.admin_panel(
            await db.get_user_count(),
            await db.get_last_check_time_npk(),
            await db.get_last_check_time_knn(),
        ),
        reply_markup=main_admin_panel(),
    )


@router.message(Command("add_schedule"), IsAdmin())
async def admin_add_schedule_command(message: Message) -> None:
    pass


@router.message(Command("add_default_ring_schedule"), IsAdmin())
async def admin_add_default_ring_schedule_command(message: Message) -> None:
    pass


@router.message(Command("add_ring_schedule"), IsAdmin())
async def admin_add_ring_schedule_command(message: Message) -> None:
    pass


@router.message(Command("var_list"), IsAdmin())
async def admin_var_list_command(message: Message) -> None:
    pass


@router.message(Command("set_var"), IsAdmin())
async def admin_set_var_command(message: Message) -> None:
    pass


@router.message(Command("add_user"), IsAdmin())
async def admin_add_user_command(
    message: Message,
    command: CommandObject,
    db: Database,
) -> None:
    # /add_user [ID] [GROUP]
    try:
        await db.create_user(
            command.args[0].lower(),
            message.from_user.username,
            message.from_user.first_name,
            command.args[1].lower(),
        )
        await message.answer(AdminPhrases.success(), reply_markup=main_admin_panel())

    except TypeError as e:
        await message.reply(ErrorPhrases.invalid())
        log.error(e)
        return
