import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from gist_api import load_data, save_data

BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to the World Cup Tournament Bot!")

# /players
async def players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_data()
    if not db["players"]:
        await update.message.reply_text("No players registered yet.")
        return
    msg = "\n".join([
        f"• {data['name']} ({data.get('pes_name', '-')}) | Group {data.get('group', '-')}" 
        for data in db["players"].values()
    ])
    await update.message.reply_text("🎮 Registered Players:\n" + msg)

# /register <PES Name>
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    pes_name = " ".join(context.args) if context.args else "-"
    db = load_data()

    db["players"][str(user.id)] = {
        "name": user.first_name,
        "pes_name": pes_name,
        "group": None,
        "points": 0,
        "status": "group"
    }
    save_data(db)
    await update.message.reply_text("✅ Registered successfully!")

# Setup bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("players", players))
app.add_handler(CommandHandler("register", register))

if __name__ == "__main__":
    app.run_polling()
