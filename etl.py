import requests
import pandas as pd
import sqlite3
from datetime import datetime

# ---- EXTRACT ----
def extract_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,solana",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # throws an error if the request failed
    return response.json()

# ---- TRANSFORM ----
def transform_prices(raw_data):
    rows = []
    timestamp = datetime.now().isoformat()
    for coin, price_info in raw_data.items():
        rows.append({
            "coin": coin,
            "price_usd": price_info["usd"],
            "timestamp": timestamp
        })
    return pd.DataFrame(rows)

# ---- LOAD ----
def load_to_db(df, db_name="crypto_prices.db"):
    conn = sqlite3.connect(db_name)
    df.to_sql("prices", conn, if_exists="append", index=False)
    conn.close()

# ---- RUN THE PIPELINE ----
if __name__ == "__main__":
    print("Extracting data...")
    raw = extract_prices()

    print("Transforming data...")
    df = transform_prices(raw)
    print(df)

    print("Loading into database...")
    load_to_db(df)

    print("Done! Check crypto_prices.db")