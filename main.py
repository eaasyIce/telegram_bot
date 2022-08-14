import logging
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, ContextTypes, MessageHandler, Filters
from dictionary import get_info
from flask import Flask, request
import os
import http
from werkzeug.wrappers import Response


with open('token.txt', 'r') as f:
    TOKEN = f.read()

app = Flask(__name__)

def start(update, context):
    userName = update.effective_user
    update.message.reply_text(f"Hello {userName.first_name}! Welcome to Dictionary Bot! ")

def process(update: Update, context) -> None:
    text = update.message.text 
    message = get_info(text)
    update.message.reply_text(message)

bot = Bot(token=TOKEN.strip())
dispatcher = Dispatcher(bot=bot, update_queue=None)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process))


@app.post("/")
def index() -> Response:
    dispatcher.process_update(
        Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT