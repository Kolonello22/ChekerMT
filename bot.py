    import telebot
    from deep_translator import GoogleTranslator, YandexTranslator  # Импортируем нужные классы
    import logging
    import traceback

    # --- Настройки ---
    TELEGRAM_TOKEN = "7998402721:AAFak8x1S9pgQfXIXz8DM6X_6IJKbbPD-Bk"
    YANDEX_API_KEY = "YOUR_YANDEX_API_KEY" # Получите API ключ от Yandex Cloud
    YANDEX_LANG = 'ru'

    # --- Логирование ---
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # --- Инициализация ---
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    google_translator = GoogleTranslator(source='auto', target='ru') # Указываем язык по умолчанию
    yandex_translator = YandexTranslator(api_key=YANDEX_API_KEY, source='auto', target='ru')

    # --- Функции ---

    def translate_with_google(text, target_language='ru'):
        """Переводит текст с помощью Google Translate."""
        try:
            translation = google_translator.translate(text, target=target_language)
            return translation
        except Exception as e:
            logging.error(f"Ошибка Google Translate: {e}\n{traceback.format_exc()}")
            return f"Ошибка Google Translate: {e}.  Попробуйте позже."

    def translate_with_yandex(text):
        """Переводит текст с помощью Yandex Translate."""
        try:
            translation = yandex_translator.translate(text)  # Параметр lang больше не нужен
            return translation
        except Exception as e:
            logging.error(f"Ошибка Yandex Translate: {e}\n{traceback.format_exc()}")
            return f"Ошибка Yandex Translate: {e}. Попробуйте позже."

    # --- Обработчики команд ---

    @bot.message_handler(commands=["start", "help"])
    def send_welcome(message):
        """Обработчик команд /start и /help."""
        bot.reply_to(message, "Привет! Я бот, который сравнивает переводы Google Translate и Yandex Translate.\n"
                                 "Просто отправь мне текст, и я покажу тебе оба перевода.\n\n"
                                 "Для перевода на определенный язык через Google, используйте команду /google [язык] [текст]. Например: /google en Hello\n"
                                 "Язык нужно указывать в формате ISO 639-1 (например, en, fr, de, es).\n"
                                 "Для использования Yandex Translator потребуется API-ключ от Yandex Cloud.\n"
                                 "Для помощи используйте команду /help")

    @bot.message_handler(commands=["google"])
    def translate_google_command(message):
        """Обработчик команды /google для перевода на определенный язык."""
        try:
            parts = message.text.split(maxsplit=2)
            if len(parts) < 3:
                bot.reply_to(message, "Неправильный формат команды. Используйте: /google [язык] [текст]. Например: /google en Hello")
                return

            target_language = parts[1].lower()
            text = parts[2]
            translation = translate_with_google(text, target_language)
            bot.reply_to(message, f"Google Translate ({target_language}):\n{translation}")

        except Exception as e:
            logging.error(f"Ошибка в команде /google: {e}\n{traceback.format_exc()}")
            bot.reply_to(message, f"Произошла ошибка при обработке команды /google: {e}. Проверьте правильность введенных данных.")

    # --- Обработчик всех текстовых сообщений ---

    @bot.message_handler(func=lambda message: True)
    def translate_message(message):
        """Обработчик всех текстовых сообщений для перевода."""
        text = message.text

        try:
            google_translation = translate_with_google(text)
        except Exception as e:
            google_translation = f"Ошибка Google Translate: {e}. Попробуйте позже."
        try:
            yandex_translation = translate_with_yandex(text)
        except Exception as e:
            yandex_translation = f"Ошибка Yandex Translate: {e}. Попробуйте позже."

        response = (f"Текст: {text}\n\n"
                    f"Google Translate (ru):\n{google_translation}\n\n"
                    f"Yandex Translate (ru):\n{yandex_translation}")

        bot.reply_to(message, response)

    # --- Запуск бота ---
    if __name__ == '__main__':
        logging.info("Бот запущен...")
        try:
            bot.infinity_polling()
        except Exception as e:
            logging.critical(f"Бот упал с ошибкой: {e}\n{traceback.format_exc()}")