import logging
import sys

import pandas as pd
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

RATINGS_SUM = "ratings_sum"
RATINGS_NUM = "ratings_num"
LAST_RATING = "last_rating"
DATA = "df"
RATING_PREFIX = "rating_"
CLUSTER_PREFIX = "cluster_"


def format_random_papers(df: pd.DataFrame, cluster: int, count: int = 5) -> list[str]:
    df = (
        df[df["cluster"] == cluster]
        .sample(n=count, replace=False)
        .reset_index(drop=True)
    )
    descriptions = []
    for i, row in df.iterrows():
        semantic_scholar_url = f"https://www.semanticscholar.org/paper/{row['paperId']}"
        descriptions.append(
            f"{i + 1}. {row['title']}, {row['year']}\n\n{row['abstract']}\n\n{semantic_scholar_url}"
        )

    return descriptions


async def post_init(application: Application, csv_path: str) -> None:
    application.bot_data[DATA] = pd.read_csv(csv_path)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="MLDS paper analysis project bot. Type /help for commands list.",
    )


async def get_random_papers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton(
                "0️⃣ - model study? new architectures?",
                callback_data=CLUSTER_PREFIX + "0",
            ),
        ],
        [
            InlineKeyboardButton(
                "1️⃣ - object detection, image segmentation -- downstream/real world tasks",
                callback_data=CLUSTER_PREFIX + "1",
            ),
        ],
        [
            InlineKeyboardButton("2️⃣ - ?", callback_data=CLUSTER_PREFIX + "2"),
        ],
        [
            InlineKeyboardButton(
                "3️⃣ - generative image/3D models, diffusion models",
                callback_data=CLUSTER_PREFIX + "3",
            ),
        ],
        [
            InlineKeyboardButton(
                "4️⃣ - applications?", callback_data=CLUSTER_PREFIX + "4"
            ),
        ],
        [
            InlineKeyboardButton(
                "5️⃣ - graphs/clustering/...?", callback_data=CLUSTER_PREFIX + "5"
            ),
        ],
        [
            InlineKeyboardButton(
                "6️⃣ - transformers, attention (LLMs, ViT, ...)",
                callback_data=CLUSTER_PREFIX + "6",
            ),
        ],
        [
            InlineKeyboardButton("7️⃣ - LLMs", callback_data=CLUSTER_PREFIX + "7"),
        ],
        [
            InlineKeyboardButton(
                "8️⃣ - reinforcement learning, uncertainty estimation",
                callback_data=CLUSTER_PREFIX + "8",
            ),
        ],
        [
            InlineKeyboardButton(
                "9️⃣ - applications?", callback_data=CLUSTER_PREFIX + "9"
            ),
        ],
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

    messages = format_random_papers(df=context.bot_data[DATA], cluster=cluster)
    intro = f"{len(messages)} random papers from cluster #{cluster}:"
    await query.edit_message_text(text=intro)
    for msg in messages:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


async def get_paper_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    df: pd.DataFrame = context.bot_data[DATA]
    text = f"Total papers: {len(df)}\n\n" + "\n".join(
        [
            f"Cluster #{i} size: {count} ({count / len(df) * 100.:.2f}%)"
            for i, count in df["cluster"].value_counts().sort_index().items()
        ]
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def get_avg_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if RATINGS_NUM not in context.bot_data or RATINGS_SUM not in context.bot_data:
        text = "Nobody has rated the bot yet!"
    else:
        avg_rating = context.bot_data[RATINGS_SUM] / context.bot_data[RATINGS_NUM]
        text = f"Current average bot rating: {avg_rating:.2f}"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def rate_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("1️⃣", callback_data=RATING_PREFIX + "1"),
            InlineKeyboardButton("2️⃣", callback_data=RATING_PREFIX + "2"),
            InlineKeyboardButton("3️⃣", callback_data=RATING_PREFIX + "3"),
            InlineKeyboardButton("4️⃣", callback_data=RATING_PREFIX + "4"),
            InlineKeyboardButton("5️⃣", callback_data=RATING_PREFIX + "5"),
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

    rating = int(query.data[len(RATING_PREFIX) :])
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
    if len(sys.argv) != 3:
        raise ValueError("Usage: python bot.py <TELEGRAM_TOKEN> <CLUSTERED_DATA_PATH>")

    token = sys.argv[1]
    data_path = sys.argv[2]
    application = (
        ApplicationBuilder()
        .token(token)
        .post_init(lambda app: post_init(app, data_path))
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
