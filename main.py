from weather import get_weather, analyze_weather
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
from datetime import timedelta

# Завантажуємо токен із файлу .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт! Я твій погодний бот! 🌤\n"
        "Скоро я зможу показувати погоду та давати рекомендації."
    )


# Запуск бота

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        weather = get_weather()
        recommendations = analyze_weather(weather)

        message = (
            "🌤 Погода у Кропивницькому\n\n"
            f"🌡 Температура: {weather['temperature']} °C\n"
            f"💧 Опади: {weather['precipitation']} мм\n"
            f"💨 Вітер: {weather['wind']} км/год\n\n"
            f"📋 Рекомендації:\n{recommendations}"
        )

        await update.message.reply_text(message)

    except Exception as e:
        print(f"Помилка отримання погоди: {e}")
        await update.message.reply_text(
            "❌ Не вдалося отримати погоду. Спробуйте пізніше."
        )
    
# Автоматичне надсилання погоди
async def auto_weather(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id

    try:
        weather = get_weather()
        recommendation = analyze_weather(weather)

        message = (
            "🔔 Автоматичне оновлення погоди\n\n"
            "📍 Кропивницький\n"
            f"🌡 Температура: {weather['temperature']} °C\n"
            f"💧 Опади: {weather['precipitation']} мм\n"
            f"💨 Вітер: {weather['wind']} км/год\n\n"
            f"📋 Рекомендація:\n{recommendation}"
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text=message
        )

    except Exception as error:
        print(f"Помилка автоматичного оновлення: {error}")

# Команда підписки на автоматичну погоду
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Видаляємо попередню підписку, якщо вона існує
    old_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in old_jobs:
        job.schedule_removal()

    # Автоматичне оновлення кожні 5 хвилин
    context.job_queue.run_repeating(
        auto_weather,
        interval=300,
        first=5,
        chat_id=chat_id,
        name=str(chat_id)
    )

    await update.message.reply_text(
        "✅ Автоматичне оновлення погоди увімкнено!\n"
        "🔔 Повідомлення приходитимуть кожні 5 хвилин."
    )

def main():
    if not TOKEN:
        raise ValueError("Токен не знайдено у файлі .env")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("subscribe", subscribe))

    print("🤖 Бот запущений!")
    app.run_polling()


if __name__ == "__main__":
    main()