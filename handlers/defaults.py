from aiogram import Router
from aiogram.filters import Command

from aiogram.types import Message

from db.database import Database

from keyboards.default import main_user_panel
from keyboards.setup_ui import set_bot_commands
from utils.phrases import Phrases

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, db: Database) -> None:
    if not await db.get_user(message.from_user.id):
        await message.answer(Phrases.first_greeting())
    else:
        await message.answer(Phrases.start(), reply_markup=main_user_panel())
        await set_bot_commands(message.bot)
