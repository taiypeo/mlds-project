import json
import logging
import os

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

ERROR_TEXT = "Failed to send a request to the backend. Please try again later"
HAS_USER_RATED = "has_user_rated"
BACKEND = "backend"
RATING_PREFIX = "rating_"
MIN_RATING = 1
MAX_RATING = 5
CLUSTER_PREFIX = "cluster_"


class Backend:
    def __init__(self, fqdn: str) -> None:
        self.url = f"http://{fqdn}"

    def rate(self, rating: int) -> requests.Response:
        return requests.post(f"{self.url}/rating?rating={rating}")

    def get_rating(self) -> requests.Response:
        return requests.get(f"{self.url}/rating")

    def paper_stats(self) -> requests.Response:
        return requests.get(f"{self.url}/paper-stats")

    def random_papers(self, cluster: int, count: int = 5) -> requests.Response:
        return requests.get(f"{self.url}/random-papers?cluster={cluster}&count={count}")


def build_emoji_number(n: int) -> str:
    emoji_digits = [
        "0️⃣",
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣",
    ]
    if n == 0:
        return emoji_digits[0]

    result = []
    while n > 0:
        result.append(emoji_digits[n % 10])
        n //= 10

    result.reverse()
    return "".join(result)


async def post_init(application: Application, backend_fqdn: str) -> None:
    application.bot_data[BACKEND] = Backend(backend_fqdn)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="MLDS paper analysis project bot. Type /help for commands list.",
    )


async def get_random_papers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = context.bot_data[BACKEND].paper_stats()
    if response.status_code != 200:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=ERROR_TEXT
        )
        return

    response_json = json.loads(response.text)
    descriptions = [
        (
            int(cluster["index"]),
            build_emoji_number(int(cluster["index"])) + " - " + cluster["description"],
        )
        for cluster in response_json["clusters"]
    ]
    descriptions.sort()

    keyboard = [
        [
            InlineKeyboardButton(
                description,
                callback_data=CLUSTER_PREFIX + str(i),
            ),
        ]
        for i, description in descriptions
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please choose a cluster:",
        reply_markup=reply_markup,
    )


async def show_papers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    cluster = int(query.data[len(CLUSTER_PREFIX) :])
    response = context.bot_data[BACKEND].random_papers(cluster)
    if response.status_code != 200:
        text = ERROR_TEXT
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    else:
        response_json = json.loads(response.text)
        intro = f"{len(response_json)} random papers from cluster #{cluster}:"
        await query.edit_message_text(text=intro)
        for i, paper in enumerate(response_json):
            msg = f"{i + 1}. {paper['title']}, {paper['year']}\n\n{paper['abstract']}\n\n{paper['url']}"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


async def get_paper_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = context.bot_data[BACKEND].paper_stats()
    if response.status_code != 200:
        text = ERROR_TEXT
    else:
        response_json = json.loads(response.text)
        text = f"Total papers: {response_json['total_papers']}\n\n" + "\n".join(
            [
                f"Cluster #{cluster['index']} size: {cluster['size']} "
                f"({float(cluster['percentage_of_total']):.2f}%)"
                for cluster in response_json["clusters"]
            ]
        )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def get_avg_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = context.bot_data[BACKEND].get_rating()
    if response.status_code != 200:
        text = ERROR_TEXT
    else:
        rating = float(response.text)
        if rating == 0.0:
            text = "Nobody has rated the bot yet!"
        else:
            text = f"Current average bot rating: {rating:.2f}"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def rate_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton(
                build_emoji_number(i), callback_data=RATING_PREFIX + str(i)
            )
            for i in range(MIN_RATING, MAX_RATING + 1)
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please choose:",
        reply_markup=reply_markup,
    )


async def save_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if HAS_USER_RATED in context.user_data and context.user_data[HAS_USER_RATED]:
        text = f"You have already rated the bot!"
    else:
        rating = int(query.data[len(RATING_PREFIX) :])
        response = context.bot_data[BACKEND].rate(rating)
        if response.status_code != 200:
            text = ERROR_TEXT
        else:
            text = f"Set your rating to {rating}!"
            context.user_data[HAS_USER_RATED] = True

    await query.edit_message_text(text=text)


async def get_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    HELP_TEXT = """
/start -- start the bot
/help -- show this message
/get_random_papers -- get random papers from a cluster
/get_paper_stats -- get statistics about the papers
/rate_bot -- rate the bot
/get_avg_rating -- get the average rating of the bot
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP_TEXT)


if __name__ == "__main__":
    token = os.environ["TELEGRAM_TOKEN"]
    backend_fqdn = os.environ["BACKEND_FQDN"]
    application = (
        ApplicationBuilder()
        .token(token)
        .post_init(lambda app: post_init(app, backend_fqdn))
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_avg_rating", get_avg_rating))
    application.add_handler(CommandHandler("rate_bot", rate_bot))
    application.add_handler(
        CallbackQueryHandler(save_rating, pattern="^" + RATING_PREFIX)
    )
    application.add_handler(CommandHandler("get_random_papers", get_random_papers))
    application.add_handler(
        CallbackQueryHandler(show_papers, pattern="^" + CLUSTER_PREFIX)
    )
    application.add_handler(CommandHandler("get_paper_stats", get_paper_stats))
    application.add_handler(CommandHandler("help", get_help))

    application.run_polling()
