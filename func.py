from datetime import datetime, time, timedelta
import re

def get_time_from_string(message_user: str):
    """Функция принимает строку и возвращает время из строки в формате datetime"""
    try:
        pattern1 = r"\d{2}\W\d{2}"
        pattern2 = r"[\W]"
        time_remind_user = re.findall(pattern1, message_user)
        time_remind_user_str = str(time_remind_user).replace(" ", "").replace("'", "").replace("[", "").replace("]", "")
        separator_message_user = str(re.findall(pattern2, time_remind_user_str)).replace("'", "").replace("[","").replace("]", "")
        time_remind_user_copy = time_remind_user_str.replace(separator_message_user, ":")
        time_user_remind = datetime.strptime(str(time_remind_user_copy), f"%H:%M").time()
        return time_user_remind
    except ValueError:
        return "Пожалуйста, ведите время для напоминания"


def get_text_from_string(message_user: str):
    """Функция принимает строку и возвращает строку, заменяя время, указанное пользователем,
    на дату и время в формате datetime"""
    try:
        pattern1 = r"\d{2}\W\d{2}"

        time_remind_user = re.findall(pattern1, message_user)
        time_remind_user_str = str(time_remind_user).replace(" ", "").replace("'", "").replace("[", "").replace("]", "")
        date_time_user_remind = get_time_from_string(message_user)
        message_user_sms = message_user.replace(time_remind_user_str, str(date_time_user_remind))

        return f"{message_user_sms}"
    except ValueError:
        return "Пожалуйста, ведите время для напоминания"


