from aiogram import Router, F
from aiogram import types

from db.database import Database
from filters.is_admin import IsAdmin

from utils.date_utils import get_tomorrow_date
from utils.phrases import AdminPhrases
from utils.mailing_handler import post_schedule_in_group

from services.schedule import save_schedule


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
        return

    await post_schedule_in_group(
        bot=callback.bot,
        db=db,
        group=temp_schedule.group,
        file_type=temp_schedule.file_type,
        files=temp_schedule.files_url,
    )

    await db.delete_temp_schedule(temp_id)

    await save_schedule(
        db=db,
        group=temp_schedule.group,
        date=get_tomorrow_date(),
        url=temp_schedule.files_url,
    )

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

    await callback.message.delete()


@router.callback_query(F.data.startswith(AdminPhrases.edit_schdule_command), IsAdmin())
async def admin_edit_schedule_command(
    callback: types.CallbackQuery, db: Database
) -> None:
    temp_id = int(callback.data.split(":")[1])

    temp_schedule = await db.get_temp_schedule(temp_id)

    if not temp_schedule:
        await callback.answer("not temp_schedule")
        return

    # todo


# endregion
