import logging
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.types.input_paid_media_photo import InputPaidMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder

from db.database import Database
from keyboards.admin import manage_new_schedule
from keyboards.default import under_post_keyboard

from models.schedule import ScheduleType
from models.temp_prikol import prikol
from models.user import User
from settings import config
from utils.date_utils import get_tomorrow_date
from utils.phrases import ErrorPhrases, Phrases

logger = logging.getLogger(__name__)


async def send_files_to_users(
    message: str,
    bot: Bot,
    users: list[User],
    file_type: str = None,
    files: list[str] = None,
    reply_keyboard: InlineKeyboardMarkup = None,
):
    """общий метод чтобы отправить сообщение всем пользователям

    Args:
        files (list[str], optional): если пустой, отправляется прост текст. Defaults to None.
    """

    if files is None:
        for user in users:
            await bot.send_message(
                chat_id=user.tg_id,
                text=message,
                reply_markup=reply_keyboard,
            )
        return

    many_files = are_there_many_files(files)

    if many_files:
        media_group = MediaGroupBuilder(caption=message)
        add_media = (
            media_group.add_document if file_type == "doc" else media_group.add_photo
        )
        for file in files:
            add_media(file)

    for user in users:
        if many_files:
            await bot.send_media_group(user.tg_id, media_group.build())
            return

        if file_type == "doc":
            await bot.send_document(
                caption=message,
                chat_id=user.tg_id,
                document=files,
                reply_markup=reply_keyboard,
            )

        elif file_type == "photo":
            await bot.send_photo(
                caption=message,
                chat_id=user.tg_id,
                photo=files,
                reply_markup=reply_keyboard,
            )
        else:
            logger.error("Unknown file type")


async def post_schedule_in_group(
    bot: Bot,
    db: Database,
    group: str,
    file_type: str,
    files: list[str],
    ignore_notification: bool = False,
):
    """
    шаблон на основе mail_everyone_in_group()

    Args:
        ignore_notification (bool, optional): похуй на отключение рассылки. Defaults to False.

    """

    users = await db.get_all_users_from_group(group, ignore_notification)

    if not users:
        logger.error("There are no users in group %s", group)

    if prikol.is_prikol_activated:
        await send_paid_files_to_users(
            bot=bot,
            user=users,
            file=files,
        )
        return

    await send_files_to_users(
        message=Phrases.schedule_text(get_tomorrow_date()),
        bot=bot,
        users=users,
        file_type=file_type,
        files=files,
        reply_keyboard=under_post_keyboard(),
    )


async def send_rings_to_user(
    bot: Bot,
    user: User,
    rings_type: str,
    file_type: str,
    files: list[str] | str,
):
    if user.group == "кнн":
        bot.send_message(
            chat_id=user.tg_id,
            text=Phrases.rings_knn(),
        )

    rings_date = (
        get_tomorrow_date()
        if rings_type == ScheduleType.RING.value
        else ScheduleType.DEFAULT_RING.value
    )

    await send_files_to_users(
        message=Phrases.schedule_text(rings_date),
        bot=bot,
        users=[user],
        file_type=file_type,
        files=files,
        reply_keyboard=under_post_keyboard(),
    )


async def send_schedule_to_user(
    bot: Bot,
    user: User,
    file_type: str,
    files: list[str] | str,
    date: str | None = None,
):
    await send_files_to_users(
        message=Phrases.schedule_text(get_tomorrow_date() if date is None else date),
        bot=bot,
        users=[user],
        file_type=file_type,
        files=files,
        reply_keyboard=under_post_keyboard(),
    )


# admin - - -


async def send_new_post_to_admin(
    bot: Bot, group: str, file_type: str, files: list[str] | str, db: Database
):
    many_files = are_there_many_files(files)

    # vremenno todo ⚠️⚠️⚠️ temp todo
    if file_type == "photo":
        if (
            len(files) == 5
        ):  # 5 - vmeste s ring schedyle todo ring checking:: ring | 1 course | 2c | 3c | ...
            files = files[2]
            many_files = False

        elif many_files:
            files = files[1]  # 1 - второй по счету т.е. 2 курс
            many_files = False

        elif many_files:  # пока что так, чтобы ничего не ломалось
            files = files[0]
            many_files = False

    try:
        temp_schedule = await db.save_temp_schedule(group, file_type, files)

        if not temp_schedule:
            logger.error(ErrorPhrases.something_went_wrong())
            return

        temp_schedule_id = temp_schedule.id
    except Exception as e:
        logger.error(f"Error saving temp schedule: {e}")
        return

    if many_files:
        media_group = MediaGroupBuilder(caption=group)
        add_media = (
            media_group.add_document if file_type == "doc" else media_group.add_photo
        )
        for file in files:
            add_media(file)

    for admin in config.admins:
        if many_files:
            await bot.send_media_group(admin, media_group.build())

            await bot.send_message(
                chat_id=admin,
                text=group,
                reply_markup=manage_new_schedule(temp_schedule_id),
            )

            return

        if file_type == "doc":
            await bot.send_document(
                caption=group,
                chat_id=admin,
                document=files,
                reply_markup=manage_new_schedule(temp_schedule_id),
            )

        elif file_type == "photo":
            await bot.send_photo(
                caption=group,
                chat_id=admin,
                photo=files,
                reply_markup=manage_new_schedule(temp_schedule_id),
            )


async def send_paid_files_to_users(
    bot: Bot, user: User | list[User], file: str, date: str = None
):
    """only photos"""
    photos = InputPaidMediaPhoto(media=file)
    stars_count = 10

    if isinstance(user, list):
        for u in user:
            await bot.send_paid_media(
                u.tg_id,
                stars_count,
                [photos],
                caption=Phrases.schedule_text(
                    get_tomorrow_date() if date is None else date
                ),
                reply_markup=under_post_keyboard(),
            )
        return

    await bot.send_paid_media(
        user.tg_id,
        stars_count,
        [photos],
        caption=Phrases.schedule_text(get_tomorrow_date() if date is None else date),
        reply_markup=under_post_keyboard(),
    )


async def send_report_to_admin(bot: Bot, report: str):
    for admin in config.admins:
        await bot.send_message(chat_id=admin, text=f"⚠️ {report}")


def are_there_many_files(files: list[str]) -> bool:
    if isinstance(files, str):
        return False

    elif isinstance(files, list) and len(files) == 1:
        return False

    return len(files) > 1
