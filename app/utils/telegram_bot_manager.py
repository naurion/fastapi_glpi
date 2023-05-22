import telebot

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TOKEN)


def send_message(message, url):
    message = f'{message}\n{url}'
    bot.send_message(CHAT_ID, message)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Hello! I listen you)')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Your text is: ' + message.text)


if __name__ == '__main__':
    bot.polling(non_stop=True, interval=0)
