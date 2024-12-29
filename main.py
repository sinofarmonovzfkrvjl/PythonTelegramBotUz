from bot import TelegramBot
import logging

bot = TelegramBot("7596605488:AAFTbpv3_67TleOw8bm5JzSLqZCC0r9F4bY")

@bot.message_handler("/start")
def start(message):
    bot.send_message(message["chat"]["id"], "Hello, I'm a bot!")

@bot.message_handler("hello")
def say_hello(message):
    bot.send_message(message["chat"]["id"], "Hello!")

logging.basicConfig(level=logging.INFO)
bot.run()