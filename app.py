from telebot import types, TeleBot
from telebot.types import Message

from get_config_value import get_config_value

TOKEN = get_config_value('DEFAULT', 'BotToken', 'Введите токен бота: ')
channel_to_subscribe_username = '@pesel_fact'
url_to_subscribe = 'https://t.me/webtwgtest_bot'
url_to_subscribe_promo = 'https://t.me/pesel_fact'
web_app_url = 'https://poki.com/ru'
bot = TeleBot(TOKEN)


def check_subscription(bot_to_check: TeleBot, message: Message) -> bool:
    user_id = message.from_user.id
    chat_member = bot_to_check.get_chat_member(channel_to_subscribe_username, user_id)
    if chat_member.status == 'left':
        keyboard = create_pre_webapp_keyboard()
        bot_to_check.send_message(message.chat.id,
                                  f"Вы должны подписаться на канал {channel_to_subscribe_username} для доступа к боту.",
                                  reply_markup=keyboard)
        return False
    return True


def create_pre_webapp_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    button_start = types.KeyboardButton(text="/start")
    keyboard.add(button_start)
    return keyboard


def create_webapp_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    webapp_game = types.WebAppInfo(web_app_url)

    button_play = types.KeyboardButton(text="Начать играть!", web_app=webapp_game)
    button_share = types.KeyboardButton(text="Поделиться с друзьями!")
    button_subscribe = types.KeyboardButton(text="Подпишись")

    keyboard.add(button_play)
    keyboard.add(button_share)
    keyboard.add(button_subscribe)

    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    if not check_subscription(bot, message):
        return
    text = 'Привет, я бот для проверки Telegram Webapps!'
    keyboard = create_webapp_keyboard()
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Подпишись')
def subscribe(message):
    if not check_subscription(bot, message):
        return
    bot.send_message(message.chat.id,
                     f"Подпишитесь на наш канал, чтобы получать интересные факты каждый день! {url_to_subscribe_promo}")


@bot.message_handler(func=lambda message: message.text == 'Поделиться с друзьями!')
def subscribe(message):
    if not check_subscription(bot, message):
        return
    bot.send_message(message.chat.id,
                     f"Подпишитесь, и играй в мобильные игры прямо в телеграм! {url_to_subscribe}")


@bot.message_handler(content_types=['text'])
def echo(message):
    if not check_subscription(bot, message):
        return
    keyboard = create_webapp_keyboard()
    text = (
        'Неизвестная команда! '
        'Вы отправили сообщение напрямую в чат бота, или структура меню была изменена Админом. '
        'Не отправляйте прямых сообщений боту или обновите Меню, нажав /start')
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=keyboard)


if __name__ == '__main__':
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(e)
