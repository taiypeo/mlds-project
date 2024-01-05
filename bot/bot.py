import logging
import sys

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

RATINGS_SUM = "ratings_sum"
RATINGS_NUM = "ratings_num"
LAST_RATING = "last_rating"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def get_avg_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if RATINGS_NUM not in context.bot_data or RATINGS_SUM not in context.bot_data:
        text = "Nobody has rated the bot yet!"
    else:
        avg_rating = context.bot_data[RATINGS_SUM] / context.bot_data[RATINGS_NUM]
        text = f"Current average bot rating: {avg_rating}"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def rate_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ERROR_TEXT = "Invalid command format. Use /rate_bot <NUMBER 1-5>"

    if len(context.args) != 1:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=ERROR_TEXT
        )
        return

    try:
        rating = int(context.args[0])
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=ERROR_TEXT
        )
        return

    if rating < 1 or rating > 5:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=ERROR_TEXT
        )

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

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


if __name__ == "__main__":
    token = sys.argv[1]
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_avg_rating", get_avg_rating))
    application.add_handler(CommandHandler("rate_bot", rate_bot))

    application.run_polling()
