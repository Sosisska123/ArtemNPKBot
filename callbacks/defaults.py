from aiogram import Router, F
from aiogram import types

from db.database import Database
from utils.phrases import ButtonPhrases, Phrases


router = Router()


@router.callback_query(F.data.startswith(ButtonPhrases.turn_off_notifications_command))
async def turn_off_notifications_query(
    callback: types.CallbackQuery, db: Database
) -> None:
    tg_id = callback.from_user.id
    is_turned_on = await db.get_notification_state(tg_id)

    if is_turned_on:
        await db.update_notification_state(tg_id, False)
        await callback.answer(Phrases.notifications_off(), show_alert=True)
    else:
        await callback.answer(Phrases.notifications_already_off(), show_alert=True)
