from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from utils.phrases import ButtonPhrases


def user_panel() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text=ButtonPhrases.today_command),
            KeyboardButton(text=ButtonPhrases.rings_command),
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard=buttons, resize_keyboard=True, one_time_keyboard=True
    )


def schedule_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=ButtonPhrases.rings_command,
                    callback_data=ButtonPhrases.rings_command,
                )
            ]
        ]
    )


def post_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=ButtonPhrases.turn_off_notifications_command,
                    callback_data=ButtonPhrases.turn_off_notifications_command,
                )
            ]
        ]
    )
