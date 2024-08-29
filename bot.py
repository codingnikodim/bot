from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Определяем этапы
ORG_NAME, FROM_WHO, MAMMOTH_NAME, MAMMOTH_PHONE, MAMMOTH_AGE, ADD_INFO, FSB_ADDRESS, LAST_SMS_TIME = range(8)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Передать мамонта 🦣", callback_data='start_transfer')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'start_transfer':
        context.user_data['stage'] = ORG_NAME
        # Получаем @username пользователя
        user = query.from_user
        context.user_data['username'] = user.username if user.username else "Не указан"
        await query.message.reply_text('Пожалуйста, введите название организации:')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    stage = context.user_data.get('stage')

    if stage == ORG_NAME:
        context.user_data['org_name'] = update.message.text
        context.user_data['stage'] = FROM_WHO
        await update.message.reply_text('От кого писал:')
    
    elif stage == FROM_WHO:
        context.user_data['from_who'] = update.message.text
        context.user_data['stage'] = MAMMOTH_NAME
        await update.message.reply_text('ФИО мамонта:')
    
    elif stage == MAMMOTH_NAME:
        context.user_data['mammoth_name'] = update.message.text
        context.user_data['stage'] = MAMMOTH_PHONE
        await update.message.reply_text('Номер телефона мамонта:')
    
    elif stage == MAMMOTH_PHONE:
        context.user_data['mammoth_phone'] = update.message.text
        context.user_data['stage'] = MAMMOTH_AGE
        await update.message.reply_text('Возраст мамонта:')
    
    elif stage == MAMMOTH_AGE:
        context.user_data['mammoth_age'] = update.message.text
        context.user_data['stage'] = ADD_INFO
        await update.message.reply_text('Дополнительная информация:')
    
    elif stage == ADD_INFO:
        context.user_data['add_info'] = update.message.text
        context.user_data['stage'] = FSB_ADDRESS
        await update.message.reply_text('Адрес ФСБ:')
    
    elif stage == FSB_ADDRESS:
        context.user_data['fsb_address'] = update.message.text
        context.user_data['stage'] = LAST_SMS_TIME
        await update.message.reply_text('Время последнего SMS:')
    
    elif stage == LAST_SMS_TIME:
        context.user_data['last_sms_time'] = update.message.text

        # Формируем сообщение с собранной информацией
        user_data = context.user_data
        message = (
            f"Никнейм передающего: @{user_data['username']}\n"
            f"Название организации: {user_data['org_name']}\n"
            f"От кого писал: {user_data['from_who']}\n"
            f"ФИО мамонта: {user_data['mammoth_name']}\n"
            f"Номер телефона мамонта: {user_data['mammoth_phone']}\n"
            f"Возраст мамонта: {user_data['mammoth_age']}\n"
            f"Дополнительная информация: {user_data['add_info']}\n"
            f"Адрес ФСБ: {user_data['fsb_address']}\n"
            f"Время последнего SMS: {user_data['last_sms_time']}"
        )

        # Отправляем сообщение в группу
        group_id = '-1002214198825'  # Замените на ID вашей группы
        await context.bot.send_message(chat_id=group_id, text=message)

        # Отправляем сообщение с кнопкой для нового процесса
        keyboard = [
            [InlineKeyboardButton("Передать мамонта 🦣", callback_data='start_transfer')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Информация отправлена в группу. Выберите действие:', reply_markup=reply_markup)

        # Завершаем диалог
        context.user_data['stage'] = None

def main() -> None:
    application = Application.builder().token('7423678252:AAFQOtnKoDwDfQquhpSPe0oyX5MTwl8fCuI').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern='start_transfer'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()





















