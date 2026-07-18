from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
import config
import llm_consensus
import alpaca_options

STATE_SELECT = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Multi-LLM Options Bot Ready!\nUse /cycle")

async def run_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signals = llm_consensus.get_consensus_signals()
    if not signals:
        await update.message.reply_text("No high-confidence signals.")
        return
    
    context.user_data["signals"] = signals
    text = "High Confidence Signals:\n\n"
    for i, s in enumerate(signals, 1):
        text += f"{i}. {s['ticker']} → {s['signal']} ({s['confidence']}%) {s.get('reasoning','')}\n"
    text += "\nReply: <number> <stake>\nExample: 3 100"
    await update.message.reply_text(text)
    return STATE_SELECT

async def handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        parts = update.message.text.strip().split()
        num = int(parts[0])
        stake = int(parts[1]) if len(parts) > 1 else config.DEFAULT_STAKE
        selected = context.user_data["signals"][:num]
        for s in selected:
            alpaca_options.execute_option_trade(s, stake)
        await update.message.reply_text(f"Executed {len(selected)} trades with ${stake} each.")
    except:
        await update.message.reply_text("Invalid. Use: number stake")
    return ConversationHandler.END

def main():
    app = Application.builder().token(config.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("cycle", run_cycle)],
        states={STATE_SELECT: [MessageHandler(filters.TEXT & \~filters.COMMAND, handle_selection)]},
        fallbacks=[]
    )
    app.add_handler(conv_handler)
    
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
