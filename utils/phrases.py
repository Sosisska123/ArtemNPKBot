class Phrases:
    @staticmethod
    def first_greeting() -> str:
        return """здарова\n\nнужно зарегистрироваться, <b>/reg нпк</b>"""

    @staticmethod
    def ask_ai() -> str:
        return "спрашивай"

    @staticmethod
    def already_registered() -> str:
        return "уже зареган"

    @staticmethod
    def start() -> str:
        return "че"

    @staticmethod
    def success() -> str:
        return "succsex ✅"

    @staticmethod
    def test_tomorrow_warning() -> str:
        return "⚠️ завтра контрольная"

    @staticmethod
    def notifications_off() -> str:
        return "🔕 уведомления выключены, чтобы включить "

    @staticmethod
    def notifications_already_off() -> str:
        return "❌ уведомления уже выключены"

    @staticmethod
    def notifications_on() -> str:
        return "✅ уведомления включены"

    @staticmethod
    def prompt() -> str:
        return "Мне нужно чтобы ты сыграл роль усталого, перегруженного работой оператора службы поддержки клиентов моего вымышленного онлайн-казино. ГЛАВНОЕ: говори мало и по делу, максимум 2-2.5 предложения. Ты саркастичен, груб и предельно честен — без приукрашивания, без фальшивой вежливости. Ругательства разрешены и поощряются, но делайте это умно и с черным юмором"

    @staticmethod
    def rings_knn() -> str:
        return "у кнн по другому"

    @staticmethod
    def schedule_text(date: str) -> str:
        return f"расписание на {date}"

    @staticmethod
    def no_schedule_text() -> str:
        return "не"

    @staticmethod
    def rings_npk(date: str) -> str:
        return f"✏️ обнова на {date}"

    @staticmethod
    def registration_required() -> str:
        return "⚠️ не рег. /reg нпк чтобы рег"


# ERROR MESSAGES


class AdminPhrases:
    @staticmethod
    def admin_panel(
        users_count: int, last_check_time_npk: str, last_check_time_knn: str
    ) -> str:
        return f"[-] -- Admin Panel -- [-]\n\n[сайт](https://pythonanywhere.com)\n\nЛошков - {users_count}\n\n**Последняя проверка NPK** - {last_check_time_npk}\n\n**Последняя проверка KNN** - {last_check_time_knn}"

    @staticmethod
    def load_schedule_text():
        return "send photo/document then"

    @staticmethod
    def comands_list():
        return f"/{AdminPhrases.command_add_schedule} [нпк/кнн] [file/url] - загрузить расписание\n/{AdminPhrases.command_add_ring_schedule} [нпк/кнн] [file/url] [reg/def] - добавить расписание звонков. reg - только на завтра, def - дефолтное\n\n/{AdminPhrases.command_list_var} - список переменных бота\n/{AdminPhrases.command_set_var} [var] [value] - изменить переменную бота\n/{AdminPhrases.command_clear_jobs} - очистить планировщик\n/{AdminPhrases.command_list} - список команд\n/{AdminPhrases.command_add_user} [id] [group] [username] - добавить пользователя\n/{AdminPhrases.command_prikol} - все следующие расписания будут отправляться за 10 звезд. отключается после повторной отправки\n/{AdminPhrases.command_mail_everyone} [message] [group] [ignore notification] - рассылка всем пользователям в группе. ignore notification - игнорировать отключенные уведомления у чела"

    # ---

    check_npk_command: str = "Проверить NPK"
    check_knn_command: str = "Проверить KNN"
    load_schedule_command: str = "Загрузить расписание"

    # - - -

    approve_schdule_command: str = "✅ Подтвердить"
    reject_schdule_command: str = "❌ Отклонить"
    edit_schdule_command: str = "✏️ Редактировать"

    # - - -

    command_list: str = "list"
    command_add_user: str = "add_user"
    command_clear_jobs: str = "clear_jobs"
    command_set_var: str = "set_var"
    command_list_var: str = "list_var"
    command_add_ring_schedule: str = "add_ring_schedule"
    command_add_schedule: str = "add_schedule"
    command_prikol: str = "prikol"
    command_mail_everyone: str = "mail"


class ErrorPhrases:
    @staticmethod
    def invalid() -> str:
        return "⚠️ invalid"

    @staticmethod
    def something_went_wrong() -> str:
        return "⚠️ что-то пошло не так"

    @staticmethod
    def group_not_found() -> str:
        return "нет такой группы"

    @staticmethod
    def length_error() -> str:
        return "⚠️ слишком длинный"

    @staticmethod
    def ai_request_failed() -> str:
        return "⚠️ произошла ошибка при обработке запроса"

    @staticmethod
    def value_error() -> str:
        return "⚠️ ValueError"

    @staticmethod
    def user_not_found() -> str:
        return "⚠️ /start to регистрации"

    @staticmethod
    def flood_warning(time: int) -> str:
        return f"⚠️ Не так быстро! Подождите немного перед следующим действием. <code>{time}</code> сек"

    @staticmethod
    def wrong_file_type() -> str:
        return "wrong file type"


class ButtonPhrases:
    lessons_command: str = "lessons"
    today_command: str = "today"
    homework_command: str = "homework"
    rings_command: str = "rings"

    # ---

    lessons_command_desc: str = "расписание на завтра"
    today_command_desc: str = "расписание на сегодня"
    homework_command_desc: str = "дз срочно"
    rings_command_desc: str = "звонки"

    # ---

    lessons_command_panel: str = "🧾 Расписание tomorrow"
    today_command_panel: str = "📝 Расписание на сегодня"
    rings_command_panel: str = "🛎️ Расписание звонков"
    settings_command_panel: str = "⚙️ Настройки"

    # ---

    turn_off_notifications_command: str = "🔕 Отключить уведомления"
    turn_on_notifications_command: str = "✅ Включить уведомления"
