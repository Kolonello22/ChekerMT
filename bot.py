from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
import asyncio

# Ваш токен от BotFather
API_TOKEN = "7998402721:AAFak8x1S9pgQfXIXz8DM6X_6IJKbbPD-Bk"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создание клавиатуры
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Google Переводчик"), KeyboardButton(text="Яндекс переводчик")],
        [KeyboardButton(text="DeepL")]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@dp.message(F.text == "/start")
async def send_welcome(message: Message):
    await message.answer(
        "Привет! Я помогу наглядно сравнить результаты нескольких систем машинного перевода. Выберите какие сравнить:",
        reply_markup=keyboard
    )

# Обработчик нажатий на кнопки
@dp.message(F.text.in_({"Google Переводчик", "Яндекс переводчик", "DeepL"}))
async def recommend_books(message: Message):
    level = message.text
    if level == "Google Переводчик":
        books = "1. Яндекс Переводчик\n2. DeepL"
    elif level == "Яндекс переводчик":
        books = "1. Google Переводчик\n2. DeepL"
    else:  # DeepL
        books = "1. Google Переводчик\n2. Яндекс Переводчик"

    await message.answer(f"Язык для сравнения с {level}:\n{books}")

# Главная функция для запуска бота
async def main():
    # Регистрация обработчиков
    dp.message.register(send_welcome, F.text == "/start")
    dp.message.register(recommend_books, F.text.in_({"Beginner", "Intermediate", "Advanced"}))

    # Удаление старого webhook и запуск polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
