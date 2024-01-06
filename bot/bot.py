import logging
import sys

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

RATINGS_SUM = "ratings_sum"
RATINGS_NUM = "ratings_num"
LAST_RATING = "last_rating"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="MLDS paper analysis project bot. Type /help for commands list.",
    )


async def get_avg_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if RATINGS_NUM not in context.bot_data or RATINGS_SUM not in context.bot_data:
        text = "Nobody has rated the bot yet!"
    else:
        avg_rating = context.bot_data[RATINGS_SUM] / context.bot_data[RATINGS_NUM]
        text = f"Current average bot rating: {avg_rating}"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def rate_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("1️⃣", callback_data="1"),
            InlineKeyboardButton("2️⃣", callback_data="2"),
            InlineKeyboardButton("3️⃣", callback_data="3"),
            InlineKeyboardButton("4️⃣", callback_data="4"),
            InlineKeyboardButton("5️⃣", callback_data="5"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please choose:",
        reply_markup=reply_markup,
    )


async def save_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    rating = int(query.data)
    if LAST_RATING in context.user_data:
        text = f"Updated your rating to {rating}!"
        context.bot_data[RATINGS_SUM] -= context.user_data[LAST_RATING]
        context.bot_data[RATINGS_SUM] += rating
    else:
        text = f"Set your rating to {rating}!"
        if RATINGS_SUM in context.bot_data:
            context.bot_data[RATINGS_SUM] += rating
        else:
            context.bot_data[RATINGS_SUM] = rating

        if RATINGS_NUM in context.bot_data:
            context.bot_data[RATINGS_NUM] += 1
        else:
            context.bot_data[RATINGS_NUM] = 1

    context.user_data[LAST_RATING] = rating

    await query.edit_message_text(text=text)


async def get_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    HELP_TEXT = """
/start -- start the bot
/help -- show this message
/rate_bot <NUMBER 1-5> -- rate the bot
/get_avg_rating -- get the average rating of the bot
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP_TEXT)


if __name__ == "__main__":
    token = sys.argv[1]
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_avg_rating", get_avg_rating))
    application.add_handler(CommandHandler("rate_bot", rate_bot))
    application.add_handler(CallbackQueryHandler(save_rating))
    application.add_handler(CommandHandler("help", get_help))

    application.run_polling()
