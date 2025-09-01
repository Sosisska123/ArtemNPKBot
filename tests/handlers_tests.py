from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from db.database import Database
from filters.is_admin import IsAdmin
from utils.mailing_handler import post_schedule_in_group

router = Router()


# MAILING TEST | MULTIPLE PHOTO
@router.message(Command("rt_mp"), IsAdmin())
async def run_test_mp_command(message: Message, db: Database) -> None:
    await post_schedule_in_group(
        message.bot,
        db,
        "нпк",
        "photo",
        [
            "https://sun9-47.userapi.com/s/v1/if2/khEWBUoIIj_p91m0r1JgjmgabDJFx80QOKQoy579DuAdU31lsFWTeQXbJ5twYKqZ3tpaIqXQlTD_cIDJMJAC_kFV.jpg?quality=95&as=32x17,48x25,72x38,108x56,160x84,240x125,360x188,480x251&from=bu&cs=480x0",
            "https://sun9-73.userapi.com/s/v1/ig2/eRW2_swGxcoC1-PAXvl1L6snPfKo1gX1HyfLcjvZItcZsSDyUXVdEv7wVU2mM1Ya6jIb2ysXtbK5XZB9dKLE0fz_.jpg?quality=95&as=32x43,48x65,72x98,108x146,160x217,240x326,360x488,435x590&from=bu&cs=435x0",
            "https://sun9-22.userapi.com/s/v1/ig2/zmNC72a6XeSJeeDAKDK7fC7syyVIkkSX6eKWxWrgwz090qUFAPhit9f9pspEfWjzPOYp6fXJj1XtQ9FvgcFWhAhX.jpg?quality=95&as=32x32,48x48,72x72,108x108,160x160,192x192&from=bu&cs=192x0",
        ],
    )


# MAILING TEST | SINGLE PHOTO
@router.message(Command("rt_sp"), IsAdmin())
async def run_test_sp_command(message: Message, db: Database) -> None:
    await post_schedule_in_group(
        message.bot,
        db,
        "нпк",
        "photo",
        [
            "https://sun9-47.userapi.com/s/v1/if2/khEWBUoIIj_p91m0r1JgjmgabDJFx80QOKQoy579DuAdU31lsFWTeQXbJ5twYKqZ3tpaIqXQlTD_cIDJMJAC_kFV.jpg?quality=95&as=32x17,48x25,72x38,108x56,160x84,240x125,360x188,480x251&from=bu&cs=480x0"
        ],
    )
