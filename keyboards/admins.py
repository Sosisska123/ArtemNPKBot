from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.phrases import AdminPhrases


def get_admin_panel() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=AdminPhrases.check_npk_command,
                    callback_data=AdminPhrases.check_npk_command,
                ),
                InlineKeyboardButton(
                    text=AdminPhrases.check_knn_command,
                    callback_data=AdminPhrases.check_knn_command,
                ),
            ],
        ]
    )
