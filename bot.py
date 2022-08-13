import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dictionary import get_info

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


with open('token.txt', 'r') as f:
    TOKEN = f.read()

async def start(update, context):
    userName = update.effective_user
    await update.message.reply_text(f"Hello {userName.first_name}! Welcome to Dictionary Bot! ")

async def help(update, context):
    await update.message.reply_text("""
    The following commands are available:
    
    /start -> Welcome Message
    /help -> This Message
    """)


async def process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text 
    message = get_info(text)
    await update.message.reply_text(message)



def main() -> None:
    """start the bot"""
    application = Application.builder().token(TOKEN.strip()).build()
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process))

    application.run_polling()

if __name__ == "__main__":
    main()