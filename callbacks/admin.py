from aiogram import Router, F
from aiogram import types

from db.database import Database
from filters.is_admin import IsAdmin

from utils.date_utils import get_tomorrow_date
from utils.phrases import AdminPhrases
from utils.mailing_handler import post_schedule_in_group, send_new_post_to_admin

from services.schedule import save_schedule

from utils.scheduler import remove_job
from vk.vk_schedule import npk_vk_requests, knn_vk_requests


router = Router()

# region MANAGE NEW SCHEDULE


# подтвердить и отправить свеженькое расписание в группу + сохранение в БД
@router.callback_query(
    F.data.startswith(AdminPhrases.approve_schdule_command), IsAdmin()
)
async def admin_accept_schedule_command(
    callback: types.CallbackQuery, db: Database
) -> None:
    temp_id = int(callback.data.split(":")[1])

    temp_schedule = await db.get_temp_schedule(temp_id)

    if not temp_schedule:
        await callback.answer("not temp_schedule error")
        await callback.message.delete()
        return

    await save_schedule(
        db=db,
        group=temp_schedule.group,
        date=get_tomorrow_date(),
        url=temp_schedule.files_url,
        file_type=temp_schedule.file_type,
    )

    await db.delete_temp_schedule(temp_id)
    remove_job(temp_id)

    await post_schedule_in_group(
        bot=callback.bot,
        db=db,
        group=temp_schedule.group,
        file_type=temp_schedule.file_type,
        files=temp_schedule.files_url,
    )

    await callback.message.delete()


@router.callback_query(
    F.data.startswith(AdminPhrases.approve_schdule_no_sound_command), IsAdmin()
)
async def admin_accept_schedule_no_sound_command(
    callback: types.CallbackQuery, db: Database
) -> None:
    temp_id = int(callback.data.split(":")[1])

    temp_schedule = await db.get_temp_schedule(temp_id)

    if not temp_schedule:
        await callback.answer("not temp_schedule error")
        await callback.message.delete()
        return

    await save_schedule(
        db=db,
        group=temp_schedule.group,
        date=get_tomorrow_date(),
        url=temp_schedule.files_url,
        file_type=temp_schedule.file_type,
    )

    await db.delete_temp_schedule(temp_id)
    remove_job(temp_id)

    await callback.message.delete()


# итак понятно вроде, удалить удалить и все
@router.callback_query(
    F.data.startswith(AdminPhrases.reject_schdule_command), IsAdmin()
)
async def admin_reject_schedule_command(
    callback: types.CallbackQuery, db: Database
) -> None:
    temp_id = int(callback.data.split(":")[1])

    await db.delete_temp_schedule(temp_id)
    remove_job(temp_id)

    await callback.message.delete()


@router.callback_query(F.data.startswith(AdminPhrases.edit_schdule_command), IsAdmin())
async def admin_edit_schedule_command(
    callback: types.CallbackQuery, db: Database
) -> None:
    temp_id = int(callback.data.split(":")[1])

    temp_schedule = await db.get_temp_schedule(temp_id)
    remove_job(temp_id)

    if not temp_schedule:
        await callback.answer("not temp_schedule")
        return

    # todo


# endregion

# region FETCHING FROM GROUPS


@router.callback_query(F.data.startswith(AdminPhrases.check_npk_command), IsAdmin())
async def admin_check_npk_command(callback: types.CallbackQuery, db: Database) -> None:
    # todo make shared function
    result = await npk_vk_requests.check_last_post()

    await callback.message.edit_text(
        f"🕰️ checking {npk_vk_requests.group.group_name_shortcut}..."
    )

    if result and len(result) > 0:
        await callback.message.delete()

        for group in result.values():
            await send_new_post_to_admin(
                bot=callback.bot,
                group=group.group_name_shortcut,
                file_type=group.return_file_type,
                files=group.files_url,
                db=db,
            )

    else:
        await callback.message.edit_text("⚠️ пусто. видимо уже нового расписания нет")


@router.callback_query(F.data.startswith(AdminPhrases.check_knn_command), IsAdmin())
async def admin_check_knn_command(callback: types.CallbackQuery, db: Database) -> None:
    # todo make shared function
    result = await knn_vk_requests.check_last_post()

    await callback.message.edit_text(
        f"🕰️ checking {knn_vk_requests.group.group_name_shortcut}..."
    )

    if result and len(result) > 0:
        await callback.message.delete()

        for group in result.values():
            await send_new_post_to_admin(
                bot=callback.bot,
                group=group.group_name_shortcut,
                file_type=group.return_file_type,
                files=group.files_url,
                db=db,
            )

    else:
        await callback.message.edit_text("⚠️ пусто. видимо уже нового расписания нет")


# endregion
