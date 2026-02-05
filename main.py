import requests
import time
import os
from telegram import Bot

# ===== AYARLAR =====
TOKEN = os.getenv("8375136572:AAGeZAaukMwqzf2KvO-TNDc65j9FSWm7fsY")
CHANNEL = "@marketsignal_live"

SPONSOR_TEXT = "🤝 Sponsor: YourBrand | Reklam & işbirliği için DM"
BINANCE_TEXT = "💳 VIP & Destek: Binance Pay | USDT / BNB kabul edilir"

bot = Bot(token=TOKEN)

def get_fx():
    fx_url = "https://api.exchangerate-api.com/v4/latest/USD"
    fx_data = requests.get(fx_url).json()

    usd_try = round(fx_data["rates"]["TRY"], 2)
    eur_try = round(usd_try / fx_data["rates"]["EUR"], 2)

    return usd_try, eur_try

def get_btc():
    btc_url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    btc_data = requests.get(btc_url).json()
    return round(float(btc_data["price"]), 2)

def get_gold(usd_try):
    # ONS Altın (USD)
    gold_url = "https://api.binance.com/api/v3/ticker/price?symbol=XAUUSDT"
    gold_data = requests.get(gold_url).json()
    ons_usd = round(float(gold_data["price"]), 2)

    # Gram Altın (TRY) = ONS * USD/TRY / 31.1
    gram_try = round((ons_usd * usd_try) / 31.1, 2)

    return ons_usd, gram_try

last_state = ""

while True:
    try:
        usd, eur = get_fx()
        btc = get_btc()
        ons, gram = get_gold(usd)

        state = f"{usd}-{eur}-{btc}-{ons}-{gram}"
        if state != last_state:
            msg = (
                f"📊 MarketSignal Live\n\n"
                f"💵 USD/TRY: {usd} ₺\n"
                f"💶 EUR/TRY: {eur} ₺\n"
                f"₿ BTC/USDT: {btc}\n"
                f"🟡 ONS Gold: {ons} $\n"
                f"🟡 Gram Gold: {gram} ₺\n\n"
                f"{SPONSOR_TEXT}\n"
                f"{BINANCE_TEXT}"
            )
            bot.send_message(chat_id=CHANNEL, text=msg)
            last_state = state

        time.sleep(60)

    except Exception as e:
        time.sleep(60)
        
