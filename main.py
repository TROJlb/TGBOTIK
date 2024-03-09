import telebot
from telebot import types

bot = telebot.TeleBot("7007202701:AAE3r48wpu2Pm2QecQSjY-Q4GcHXQnh24E4")


# Словарь для хранения имени и праздника для каждого пользователя
user_data = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Введи имя, кого будем поздравлять:")
    bot.register_next_step_handler(message, ask_name)


def ask_name(message):
    global user_data  # Объявляем переменную как глобальную
    user_id = message.from_user.id
    user_data[user_id] = {'id': user_id, 'name': message.text}
    bot.send_message(message.chat.id, "Теперь введи праздник:")
    bot.register_next_step_handler(message, ask_holiday)


def ask_holiday(message):
    global user_data  # Объявляем переменную как глобальную
    user_id = message.from_user.id
    user_data[user_id]['holiday'] = message.text
    # Формируем текст для вывода информации о пользователе
    user_info_text = f"Имя: {user_data[user_id]['name']}\nПраздник: {user_data[user_id]['holiday']}"
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    generate_button = types.KeyboardButton("Сгенерировать поздравление")
    edit_button = types.KeyboardButton("Изменить имя и праздник")
    keyboard.add(generate_button, edit_button)
    bot.send_message(message.chat.id, user_info_text, reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global user_data  # Объявляем переменную как глобальную
    user_id = message.from_user.id
    if user_id in user_data:
        if message.text == "Сгенерировать поздравление":
            generate_congratulation(message)
        elif message.text == "Изменить имя и праздник":
            del user_data[user_id]  # Удаляем данные о пользователе
            bot.send_message(message.chat.id, "Введи своё имя заново:")
            bot.register_next_step_handler(message, ask_name)
    else:
        bot.send_message(message.chat.id, "Сначала введите имя и праздник.")


def generate_congratulation(message):
    global user_data  # Объявляем переменную как глобальную
    user_id = message.from_user.id
    user = user_data[user_id]
    bot.send_message(message.chat.id, f"{user['name']}, отдыхай братишка")

bot.polling()