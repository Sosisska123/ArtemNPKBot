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
        # success = await db.update_notification_state(tg_id, False)
        success = True  # todo их нельзя включить
        if success:
            await callback.answer(Phrases.notifications_off(), show_alert=True)
        else:
            await callback.answer(
                "❌ Ошибка при отключении уведомлений", show_alert=True
            )
    else:
        await callback.answer(Phrases.notifications_already_off(), show_alert=True)


@router.callback_query(F.data.startswith(ButtonPhrases.turn_on_notifications_command))
async def turn_on_notifications_query(
    callback: types.CallbackQuery, db: Database
) -> None:
    tg_id = callback.from_user.id
    is_turned_on = await db.get_notification_state(tg_id)

    if not is_turned_on:
        success = await db.update_notification_state(tg_id, True)
        if success:
            await callback.answer(Phrases.notifications_on(), show_alert=True)
        else:
            await callback.answer(
                "❌ Ошибка при включении уведомлений", show_alert=True
            )
    else:
        await callback.answer("✅ Уведомления уже включены", show_alert=True)
