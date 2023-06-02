import telebot
from cfg import *
from spellchecker import SpellChecker

# Создаем экземпляр бота и указываем токен
bot = telebot.TeleBot(token)

# Создаем экземпляр SpellChecker
spell = SpellChecker(language=lang)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот-проверяльщик орфографии. Просто отправь мне текст, и я исправлю твои ошибки!"
                                      "\nТакже можешь воспользоваться командой /help для просмотра всех моих возможностей!")


@bot.message_handler(commands=['help'])
def send(message):
    bot.send_message(message.chat.id, "Чтобы проверить правильность написания предложения напиши \n/spellcheck <предложение с ошибкой>"
                                      "\n\nЧтобы проверить правильность написания конкретного "
                                      "слова и посмотреть на возможные исправления напиши \n /check_word <слово с ошибкой>")


@bot.message_handler(commands=['check_word'])
def word_check(message):
    text = message.text[11:]
    for word in spell.candidates(text):
        bot.reply_to(message, f"Возможный вариант правильного написания: {word}")


# Обработчик команды /spellcheck
@bot.message_handler(commands=['spellcheck'])
def spellcheck(message):
    # Получаем текст сообщения от пользователя
    text = message.text[11:]  # Убираем "/spellcheck " из начала сообщения

    mistakes = spell.unknown(text.split())
    for mistake in mistakes:
        bot.reply_to(message, f'Ошибка: "{mistake}" \nПравильное написание: {spell.correction(mistake)}')


# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def echo(message):
    # Отвечаем пользователю с тем же текстом
    bot.reply_to(message, message.text)


# Запускаем бота
bot.polling()
