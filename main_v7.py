import ptbot
from dotenv import load_dotenv
import os
from pytimeparse import parse


def wait(chat_id, message, bot):
    if message == "/start":
        bot.send_message(chat_id, "Бот запущен!")

    parsed_time = parse(message)
    message_id = bot.send_message(chat_id, "На сколько поставить таймер?")

    bot.create_countdown(parsed_time, notify_progress, author_id=chat_id, message_id=message_id, total_time=parsed_time, bot=bot)
    bot.create_timer(parsed_time, answer, author_id=chat_id, message=message, bot=bot)


def notify_progress(secs_left, author_id, message_id, total_time, bot):
    bot.update_message(author_id, message_id, "Осталось {} секунд\n".format(secs_left) + render_progressbar(total_time, secs_left))


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def answer(author_id, message, bot):
    bot.send_message(author_id, "Время вышло!")


def main():
    load_dotenv()
    tg_bot_token = os.getenv("TG_TOKEN")
    bot = ptbot.Bot(tg_bot_token)
    bot.reply_on_message(wait, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
