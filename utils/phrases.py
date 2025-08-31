class Phrases:
    @staticmethod
    def first_greeting() -> str:
        return """здарова\n\nнужно зарегистрироваться, <b>/reg (нпк)</b>"""

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


# ERROR MESSAGES


class AdminPhrases:
    @staticmethod
    def admin_panel(
        users_count: int, last_check_time_npk: str, last_check_time_knn: str
    ) -> str:
        return f"[-] -- Admin Panel -- [-]\n\n[сайт](https://pythonanywhere.com)\n\nЛошков - {users_count}\n\n**Последняя проверка NPK** - {last_check_time_npk}\n\n**Последняя проверка KNN** - {last_check_time_knn}"

    # ---

    check_npk_command: str = "Проверить NPK"
    check_knn_command: str = "Проверить KNN"
    load_schedule_command: str = "Загрузить вручную"

    # - - -

    approve_schdule_command: str = "✅ Подтвердить"
    reject_schdule_command: str = "❌ Отклонить"
    edit_schdule_command: str = "✏️ Редактировать"

    # - - -


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


class ButtonPhrases:
    schedule_command: str = "schedule"
    homework_command: str = "homework"

    schedule_command_desc: str = "расписание на сегодня"
    homework_command_desc: str = "дз срочно !"

    # ---

    today_command: str = "📝 Расписание на сегодня"
    rings_command: str = "🛎️ Расписание звонков"

    # ---

    turn_off_notifications_command: str = "🔕 Отключить уведомления"
