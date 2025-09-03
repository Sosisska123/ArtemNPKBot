import logging
from aiogram import Router
from aiogram.filters import Command, CommandObject

from aiogram.types import Message

from keyboards.default import main_user_panel
from utils.phrases import ErrorPhrases, Phrases

from db.database import Database

log = logging.getLogger(__name__)

router = Router()


@router.message(Command("reg"))
async def select_group(message: Message, command: CommandObject, db: Database) -> None:
    if await db.get_user(message.from_user.id):
        await message.answer(Phrases.already_registered())
        return

    try:
        if command.args.lower() in [
            "нпк",
            "кнн",
        ]:  # todo заменить на реал группы. когда нибудь
            await db.create_user(
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                command.args.lower(),
            )
            await message.answer(Phrases.success(), reply_markup=main_user_panel())

            log.info("User %s registered", message.from_user.username)

        else:
            await message.answer(ErrorPhrases.group_not_found())
            return
    except TypeError as e:
        await message.reply(ErrorPhrases.invalid())
        log.error(e)
        return
    except Exception as e:
        await message.reply(ErrorPhrases.something_went_wrong())
        log.error(e)
