from utils.date_utils import get_formatted_time

FILE_NAME = "log.txt"


def write_usage_log(username: str, user_id: int, action: str, time: str) -> None:
    """
    Записывает лог использования в файл.

    Args:
        username: Имя пользователя
        user_id: ID пользователя
        action: Действие, которое было выполнено
        time: Временная метка
    """

    formatted_time = get_formatted_time(time)

    try:
        with open(FILE_NAME, "a", encoding="utf-8") as file:
            # 'a' (append) вместо 'w', чтобы не перезаписывать предыдущие логи
            file.write(f"{username} {user_id} {action} {formatted_time}\n")
    except IOError as e:
        print(f"Ошибка при записи в лог-файл: {e}")
