import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from db.database import Database

from filters.is_admin import IsAdmin
from keyboards.admin import main_admin_panel

from models.schedule import ScheduleType
from models.temp_prikol import prikol

from utils.date_utils import get_tomorrow_date
from utils.mailing_handler import send_new_post_to_admin
from utils.phrases import AdminPhrases, ErrorPhrases
from utils.states import LoadScheduleFsm

from vk.vk_schedule import stop_parsing_jobs

from services.schedule import save_ring_schedule


router = Router()
log = logging.getLogger(__name__)


# create admin menu, command variant
@router.message(Command("admin"), IsAdmin())
async def admin_panel_command(message: Message) -> None:
    await message.reply(
        "admin",
        reply_markup=main_admin_panel(),
    )


# region LOAD SCHEDULE


@router.message(Command(AdminPhrases.command_add_schedule), IsAdmin())
@router.message(
    F.text.startswith(AdminPhrases.load_schedule_command),
    IsAdmin(),
)
async def load_schedule_select_group_command(
    message: Message, state: FSMContext, command: CommandObject
):
    await state.set_state(LoadScheduleFsm.load_file)

    args = command.args.split()

    group = args[0].lower()
    load_type = args[1].lower()

    if group not in ["нпк", "кнн"]:
        await message.answer(ErrorPhrases.group_not_found())
        return

    await message.answer(AdminPhrases.load_schedule_text())

    await state.update_data(group=group)
    await state.update_data(type=load_type)


@router.message(
    IsAdmin(),
    LoadScheduleFsm.load_file,
)
async def load_schedule_load_file(message: Message, db: Database, state: FSMContext):
    data = await state.get_data()

    group = data.get("group")
    type = data.get("type")

    if type == "file":
        # TEMPORARY UNAVAIBLE
        await message.reply("⚠️ TEMPORARY UNAVAIBLE try URL instead")
        await state.clear()
        return

        if group == "нпк" and message.photo is not None:
            files = message.photo
            file_type = "photo"

        elif group == "кнн" and message.document is not None:
            files = message.document
            file_type = "doc"

        else:
            await message.reply(ErrorPhrases.wrong_file_type())
            await state.clear()
            return
    else:
        files = message.text
        file_type = "photo" if group == "нпк" else "doc"

    await state.clear()

    await send_new_post_to_admin(
        bot=message.bot,
        group=group,
        file_type=file_type,
        files=files,
        db=db,
    )


# endregion


# region ADD RING SCHEDULE


@router.message(Command(AdminPhrases.command_add_ring_schedule), IsAdmin())
async def admin_add_ring_schedule_command(
    message: Message, state: FSMContext, command: CommandObject
) -> None:
    await state.set_state(LoadScheduleFsm.load_rings)
    # todo group, load_type check

    args = command.args.split()

    sch_type = args[2].lower()

    await state.update_data(sch_type=sch_type)

    await message.answer(AdminPhrases.load_schedule_text())


@router.message(
    IsAdmin(),
    LoadScheduleFsm.load_rings,
)
async def admin_add_ring_schedule_load_command(
    message: Message, db: Database, state: FSMContext
) -> None:
    url = message.text
    data = await state.get_data()
    sch_type = data.get("sch_type")

    if sch_type == "def":
        await save_ring_schedule(
            db, "нпк", get_tomorrow_date(), url, ScheduleType.DEFAULT_RING.value
        )

    elif sch_type == "reg":
        await save_ring_schedule(db, "нпк", get_tomorrow_date(), url)

    else:
        await message.reply(ErrorPhrases.invalid(), reply_markup=main_admin_panel())
        return

    await message.answer("✅ rings schedule added", reply_markup=main_admin_panel())
    await state.clear()


# endregion


@router.message(Command(AdminPhrases.command_prikol), IsAdmin())
async def admin_prikol_command(message: Message) -> None:
    prikol.is_prikol_activated = not prikol.is_prikol_activated

    if prikol.is_prikol_activated:
        await message.answer("✅ Прикол активирован")
    else:
        await message.answer("❌ Прикол деактивирован")


@router.message(Command(AdminPhrases.command_list_var), IsAdmin())
async def admin_var_list_command(message: Message) -> None:
    pass


@router.message(Command(AdminPhrases.command_set_var), IsAdmin())
async def admin_set_var_command(message: Message) -> None:
    pass


@router.message(Command(AdminPhrases.command_clear_jobs), IsAdmin())
async def admin_clear_jobs_command(message: Message) -> None:
    stop_parsing_jobs()

    await message.answer("✅ jobs cleared")


@router.message(Command(AdminPhrases.command_list), IsAdmin())
async def admin_list_command(message: Message) -> None:
    await message.reply(AdminPhrases.comands_list())


@router.message(Command(AdminPhrases.command_add_user), IsAdmin())
async def admin_add_user_command(
    message: Message,
    command: CommandObject,
    db: Database,
) -> None:
    # /add_user [ID] [GROUP] [username]
    args = command.args.split()

    if len(args) != 2:
        await message.reply(ErrorPhrases.length_error())
        return

    try:
        await db.create_user(
            args[0].lower(),
            args[2],
            args[1].lower(),
        )
        await message.answer("✅ user added", reply_markup=main_admin_panel())

    except TypeError as e:
        await message.reply(ErrorPhrases.invalid())
        log.error(e)
        return
