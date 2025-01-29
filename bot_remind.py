import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from config import API_TOKEN
from func import get_time_from_string
from func import get_text_from_string
from db import insert_into_table_user
from db import insert_into_table_remind
"""example_bot"""

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Привет👋 \n"
                        "Создавайте напоминания на сегодня 📅 , "
                        "планируйте дела 📝 и получайте уведомление 🔔 прямо в Telegram.\n"
                        "Отправьте текстовое сообщение с указанием текста 🧾 и времени ⏰ напоминания!")

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    username = message.from_user.username
    date_time = datetime.today()

    insert_into_table_user(user_id, user_name, user_surname, username, date_time)


@dp.message_handler()
async def remind(message: types.Message):
    try:
        time_user = get_time_from_string(message.text)
        date_time_user_remind = datetime.combine(datetime.now(), time_user)
        user_sms = get_text_from_string(message.text)
        now = datetime.now()
        timedelta_1 = (date_time_user_remind - now).total_seconds()

        if date_time_user_remind > now:
            await message.reply(f"Хорошо! я напомню: {user_sms} ⏳")
            await asyncio.sleep(timedelta_1)
            await message.reply(f"📌 Вы просили напомнить: {user_sms}")
        else:
            await message.reply(f"❗️Укажите время для напоминания после "
                                f"{now.time().replace(microsecond=0)} и до {"24:00:00"}")

        user_id = message.from_user.id
        text_remind = message.text
        date_time = datetime.today()
        insert_into_table_remind(user_id, text_remind, date_time)

    except ValueError:
        await message.reply(f"❗️Вы не указали время для напоминания❗\n"
                            f"Отправьте текстовое сообщение с указанием текста 🧾 и времени ⏰ напоминания!")
    except TypeError:
        await message.reply(f"❗️Вы не указали время для напоминания❗\n"
                            f"Отправьте текстовое сообщение с указанием текста 🧾 и времени ⏰ напоминания!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)