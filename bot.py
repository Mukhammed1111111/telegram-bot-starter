import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from qrcode import make as make_qr

# Получаем переменные из окружения
TOKEN = os.getenv("TOKEN")
OWNER_NAME = os.getenv("OWNER_NAME")
MBANK_NUMBER = os.getenv("MBANK_NUMBER")

# Генерация QR-кода (один раз при запуске)
qr_data = f"Mbank: {MBANK_NUMBER}\nИмя: {OWNER_NAME}"
qr_image = make_qr(qr_data)
qr_image_path = "mbank_qr.png"
qr_image.save(qr_image_path)

# Обработка фото от курьера
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    reply_text = (
        "Спасибо, отчёт получен!\n\n"
        "*Переведи 30% от суммы на реквизиты:*\n"
        f"`Mbank:` *{MBANK_NUMBER}*\n"
        f"`Имя:` *{OWNER_NAME}*\n\n"
        "Ниже — QR-код для оплаты:"
    )

    # Отправляем сообщение с реквизитами
    await context.bot.send_message(
        chat_id=chat_id,
        text=reply_text,
        parse_mode="Markdown"
    )

    # Отправляем QR-код
    with open(qr_image_path, "rb") as qr_file:
        await context.bot.send_photo(chat_id=chat_id, photo=InputFile(qr_file))

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
