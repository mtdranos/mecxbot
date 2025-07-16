import requests
import time
import pandas as pd

# Telegram bot bilgileri
TOKEN = "7978372621:AAEhNvZCav0gFYzcQhFqQXIIEnY93_uaF8"
CHAT_ID = "868940730"

# Gönderilecek sinyali Telegram'dan ilet
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram mesajı gönderilemedi:", e)

# MEXC API'den futures coin listesini çek
def get_futures_symbols():
    try:
        url = "https://contract.mexc.com/api/v1/contract/detail"
        response = requests.get(url)
        data = response.json()
        symbols = [item['symbol'] for item in data['data']]
        return symbols
    except Exception as e:
        print("Futures coin listesi alınamadı:", e)
        return []

# RSI hesapla
def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Coin verisini al
def get_klines(symbol):
    url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval=15m&limit=100"
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
        return df
    except Exception as e:
        print(f"{symbol} verisi alınamadı:", e)
        return None

# Sinyal kontrolü
def check_signal(symbol):
    df = get_klines(symbol)
    if df is None or len(df) < 35:
        return

    df["MA5"] = df["close"].rolling(window=5).mean()
    df["MA14"] = df["close"].rolling(window=14).mean()
    df["MA34"] = df["close"].rolling(window=34).mean()
    df["RSI"] = calculate_rsi(df)

    last = df.iloc[-1]

    if (
        last["RSI"] > 50 and
        last["close"] > last["MA5"] > last["MA14"] > last["MA34"] and
        df["close"].iloc[-2] < df["MA5"].iloc[-2]
    ):
        send_telegram_message(f"🟢 LONG Sinyali: {symbol}\nRSI: {round(last['RSI'], 2)}")

    elif (
        last["RSI"] < 50 and
        last["close"] < last["MA5"] < last["MA14"] < last["MA34"] and
        df["close"].iloc[-2] > df["MA5"].iloc[-2]
    ):
        send_telegram_message(f"🔴 SHORT Sinyali: {symbol}\nRSI: {round(last['RSI'], 2)}")

# Ana döngü
while True:
    print("Sinyal taraması başlatıldı...")
    symbols = get_futures_symbols()
    for sym in symbols:
        symbol = sym.replace("_", "").upper() + "USDT"
        check_signal(symbol)
    print("Bekleniyor (15 dk)...")
    time.sleep(900)
import requests
import time
import pandas as pd

# Telegram bot bilgileri
TOKEN = "7978372621:AAEhNvZCav0gFYzcQhFqQXIIEnY93_uaF8"
CHAT_ID = "868940730"

# Gönderilecek sinyali Telegram'dan ilet
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram mesajı gönderilemedi:", e)

# MEXC API'den futures coin listesini çek
def get_futures_symbols():
    try:
        url = "https://contract.mexc.com/api/v1/contract/detail"
        response = requests.get(url)
        data = response.json()
        symbols = [item['symbol'] for item in data['data']]
        return symbols
    except Exception as e:
        print("Futures coin listesi alınamadı:", e)
        return []

# RSI hesapla
def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Coin verisini al
def get_klines(symbol):
    url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval=15m&limit=100"
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
        return df
    except Exception as e:
        print(f"{symbol} verisi alınamadı:", e)
        return None

# Sinyal kontrolü
def check_signal(symbol):
    df = get_klines(symbol)
    if df is None or len(df) < 35:
        return

    df["MA5"] = df["close"].rolling(window=5).mean()
    df["MA14"] = df["close"].rolling(window=14).mean()
    df["MA34"] = df["close"].rolling(window=34).mean()
    df["RSI"] = calculate_rsi(df)

    last = df.iloc[-1]

    if (
        last["RSI"] > 50 and
        last["close"] > last["MA5"] > last["MA14"] > last["MA34"] and
        df["close"].iloc[-2] < df["MA5"].iloc[-2]
    ):
        send_telegram_message(f"🟢 LONG Sinyali: {symbol}\nRSI: {round(last['RSI'], 2)}")

    elif (
        last["RSI"] < 50 and
        last["close"] < last["MA5"] < last["MA14"] < last["MA34"] and
        df["close"].iloc[-2] > df["MA5"].iloc[-2]
    ):
        send_telegram_message(f"🔴 SHORT Sinyali: {symbol}\nRSI: {round(last['RSI'], 2)}")

# Ana döngü
while True:
    print("Sinyal taraması başlatıldı...")
    symbols = get_futures_symbols()
    for sym in symbols:
        symbol = sym.replace("_", "").upper() + "USDT"
        check_signal(symbol)
    print("Bekleniyor (15 dk)...")
    time.sleep(900)
