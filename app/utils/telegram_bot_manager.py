import telebot

from dotenv import load_dotenv
import os

from app.glpi_manager.models import Ticket

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TOKEN)


def send_message(ticket: Ticket, url):
    if ticket.from_telegram:
        message = f'Заявка:\nОрганизация: {ticket.organization.name}\nИз Телеграм\nЗаголовок: {ticket.name}\nОписание: {ticket.content}'
    else:
        message = f'Заявка:\nОрганизация: {ticket.organization.name}\nНомер пользователя: {ticket.user_number}\nЗаголовок: {ticket.name}\nОписание: {ticket.content}'

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
