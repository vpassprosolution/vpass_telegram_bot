import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

# Webhook API URL
API_SUBSCRIBE = "https://vpasstradingviewwebhook-production.up.railway.app/subscribe"
API_UNSUBSCRIBE = "https://vpasstradingviewwebhook-production.up.railway.app/unsubscribe"

# List of 7 instruments
INSTRUMENTS = ["GOLD", "BITCOIN", "ETHEREUM", "DOW JONES", "NASDAQ", "EUR/USD", "GBP/USD"]

async def show_instruments(update: Update, context: CallbackContext) -> None:
    """Display the 7 instrument selection menu."""
    keyboard = [[InlineKeyboardButton(instr, callback_data=f"select_{instr}")] for instr in INSTRUMENTS]
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_main")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("📊 *Select an Instrument:*", reply_markup=reply_markup, parse_mode="Markdown")

async def show_subscription_menu(update: Update, context: CallbackContext) -> None:
    """Show Subscribe/Unsubscribe options for selected instrument."""
    query = update.callback_query
    instrument = query.data.replace("select_", "")

    keyboard = [
        [InlineKeyboardButton(f"✅ Subscribe to {instrument}", callback_data=f"subscribe_{instrument}")],
        [InlineKeyboardButton(f"❌ Unsubscribe from {instrument}", callback_data=f"unsubscribe_{instrument}")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_instruments")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(f"🔍 *{instrument} Subscription Menu:*", reply_markup=reply_markup, parse_mode="Markdown")

async def subscribe(update: Update, context: CallbackContext) -> None:
    """Subscribe the user to the selected instrument."""
    query = update.callback_query
    instrument = query.data.replace("subscribe_", "")
    chat_id = query.from_user.id

    payload = {"chat_id": chat_id, "instrument": instrument}
    response = requests.post(API_SUBSCRIBE, json=payload)
    response_json = response.json()

    if response.status_code == 200:
        await query.message.edit_text(f"✅ You are now subscribed to {instrument} alerts!")
    else:
        await query.message.edit_text(f"❌ Subscription failed for {instrument}. Try again.")

async def unsubscribe(update: Update, context: CallbackContext) -> None:
    """Unsubscribe the user from the selected instrument."""
    query = update.callback_query
    instrument = query.data.replace("unsubscribe_", "")
    chat_id = query.from_user.id

    payload = {"chat_id": chat_id, "instrument": instrument}
    response = requests.post(API_UNSUBSCRIBE, json=payload)
    response_json = response.json()

    if response.status_code == 200:
        await query.message.edit_text(f"🚫 You have unsubscribed from {instrument} alerts.")
    else:
        await query.message.edit_text(f"❌ Unsubscription failed for {instrument}. Try again.")

async def back_to_main(update: Update, context: CallbackContext) -> None:
    """Return to the main menu."""
    from bot import main_menu
    await main_menu(update, context)

async def back_to_instruments(update: Update, context: CallbackContext) -> None:
    """Return to the instrument selection menu."""
    await show_instruments(update, context)
