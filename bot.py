import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

waiting = []
pairs = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 /find رو بزن")

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user in pairs:
        await update.message.reply_text("در حال چت هستی")
        return

    if waiting:
        partner = waiting.pop(0)
        pairs[user] = partner
        pairs[partner] = user

        await context.bot.send_message(user, "مخاطب پیدا شد 👌")
        await context.bot.send_message(partner, "مخاطب پیدا شد 👌")
    else:
        waiting.append(user)
        await update.message.reply_text("در حال جستجو...")

async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    if user in pairs:
        partner = pairs[user]
        await context.bot.send_message(partner, update.message.text)

def main():
    token = os.environ["BOT_TOKEN"]
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("find", find))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, relay))

    app.run_polling()

main()
