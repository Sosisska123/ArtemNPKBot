import logging
from aiogram import Router
from aiogram.filters import Command, CommandObject

from aiogram.types import Message

from keyboards.defaults import user_panel
from utils.phrases import ErrorPhrases, Phrases
from utils.groups_list import avaible_groups

from db.database import Database

log = logging.getLogger(__name__)

router = Router()


@router.message(Command("group"))
async def select_group(message: Message, command: CommandObject, db: Database) -> None:
    if await db.get_user(message.from_user.id):
        await message.answer(Phrases.already_registered())
        return

    try:
        if command.args in avaible_groups:
            await db.create_user(
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                command.args,
            )
            await message.answer(Phrases.success(), reply_markup=user_panel())
        else:
            await message.answer(ErrorPhrases.group_not_found())
            return
    except TypeError:
        await message.reply(ErrorPhrases.invalid())
        return
