import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    CallbackContext
)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration - TESTING BOT (Token will be revoked later)
TOKEN = '8107135672:AAGZJSOHD4DzD5kJELcZiJXm12Ic2yqq7B0'
CHANNEL = '@your_channel'  # Replace with your channel username
GROUP = '@your_group'      # Replace with your group username
TWITTER = '@your_twitter'  # Replace with your Twitter handle

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("✅ Verify Participation", callback_data='verify')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_html(
        f"👋 Welcome {user.mention_html()} to our TEST Airdrop!\n\n"
        "📝 To participate:\n\n"
        f"1. Join our channel: {CHANNEL}\n"
        f"2. Join our group: {GROUP}\n"
        f"3. Follow us on Twitter: {TWITTER}\n\n"
        "⚠️ Note: This is a TEST bot - no actual verification will be done\n"
        "Click below when done 👇",
        reply_markup=reply_markup
    )

def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'verify':
        query.edit_message_text(
            "🪙 TEST MODE: Send any text as your Solana wallet address\n\n"
            "(Example: 5F3t3e... or anything else)"
        )
        context.user_data['awaiting_wallet'] = True

def handle_message(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('awaiting_wallet'):
        wallet = update.message.text.strip()
        # Fake SOL transfer message
        update.message.reply_text(
            f"🚀 TEST SUCCESS! 🚀\n\n"
            f"10 SOL (TEST) is on its way to:\n<code>{wallet}</code>\n\n"
            "💰 Balance will not actually change - this is a test\n"
            "📣 Thank you for participating in our airdrop test!",
            parse_mode='HTML'
        )
        context.user_data['awaiting_wallet'] = False

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    if 'RENDER' in os.environ:
        # Webhook for Render
        PORT = int(os.environ.get('PORT', 5000))
        APP_NAME = os.environ.get('APP_NAME')
        updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=f'https://{APP_NAME}.onrender.com/{TOKEN}'
        )
    else:
        # Local polling
        updater.start_polling()
        print("Bot is running in polling mode...")
        updater.idle()

if __name__ == '__main__':
    import os
    main()
