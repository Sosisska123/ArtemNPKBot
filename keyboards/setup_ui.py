from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from utils.phrases import ButtonPhrases


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(
            command=ButtonPhrases.lessons_command,
            description=ButtonPhrases.lessons_command_desc,
        ),
        BotCommand(
            command=ButtonPhrases.today_command,
            description=ButtonPhrases.today_command_desc,
        ),
        BotCommand(
            command=ButtonPhrases.homework_command,
            description=ButtonPhrases.homework_command_desc,
        ),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
