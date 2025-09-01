import logging
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.media_group import MediaGroupBuilder

from db.database import Database
from keyboards.admin import manage_new_schedule
from settings import config

logger = logging.getLogger(__name__)


async def mail_everyone_in_group(
    message: str,
    bot: Bot,
    db: Database,
    group: str,
    reply_keyboard: InlineKeyboardMarkup = None,
    push_to_all: bool = False,
):
    """_summary_

    Args:
        push_to_all (bool, optional): похуй на отключение рассылки. Defaults to False.
    """

    logger.info("MEIG WORKED")

    if push_to_all:
        pass
    else:
        pass

    pass


async def post_schedule_in_group(
    bot: Bot,
    db: Database,
    group: str,
    file_type: str,
    files: list[str],
    push_to_all: bool = False,
):
    """
    шаблон на основе mail_everyone_in_group()
    """

    pass


# admin - - -


async def send_new_post_to_admin(
    bot: Bot, group: str, file_type: str, files: list[str] | str
):
    if isinstance(files, str):
        files = [files]

    many_files = len(files) > 1
    logger.info("files %s ", files)

    if many_files:
        media_group = MediaGroupBuilder(caption=group)
        add_media = (
            media_group.add_document if file_type == "doc" else media_group.add_photo
        )
        for file in files:
            add_media(file)

    for admin in config.admins:
        if many_files:
            messages = await bot.send_media_group(admin, media_group.build())
            msg_id = messages[0].message_id
            await bot.send_message(
                chat_id=admin, text=group, reply_markup=manage_new_schedule(msg_id)
            )

            return

        if file_type == "doc":
            message = await bot.send_document(
                caption=group,
                chat_id=admin,
                document=files[0],
            )
            msg_id = message.message_id
            await bot.edit_message_reply_markup(
                chat_id=admin,
                message_id=msg_id,
                reply_markup=manage_new_schedule(msg_id),
            )
        elif file_type == "photo":
            message = await bot.send_photo(
                caption=group,
                chat_id=admin,
                photo=files[0],
            )
            msg_id = message.message_id
            await bot.edit_message_reply_markup(
                chat_id=admin,
                message_id=msg_id,
                reply_markup=manage_new_schedule(msg_id),
            )


async def send_report_to_admin(bot: Bot, report: str):
    for admin in config.admins:
        await bot.send_message(chat_id=admin, text=f"⚠️ {report}")
