from flask import Flask, render_template
import pandas as pd
import os
import re

app = Flask(__name__)

CSV_FILE = os.path.join("data", "crypto_prices.csv")


def clean_number(value):
    """
    Convert values like:
    $67,500
    67,500
    +5.25%
    -2.10%
    into float values.
    """

    if value is None:
        return 0.0

    value = str(value).strip()

    # Remove $, %, commas and other symbols
    value = value.replace("$", "")
    value = value.replace(",", "")
    value = value.replace("%", "")

    # Keep only numbers, decimal point and minus sign
    match = re.search(r"-?\d+(\.\d+)?", value)

    if match:
        try:
            return float(match.group())
        except ValueError:
            return 0.0

    return 0.0


def load_crypto_data():

    if not os.path.exists(CSV_FILE):
        return []

    try:

        df = pd.read_csv(CSV_FILE)

        if df.empty:
            return []

        # Convert dataframe to records
        records = df.to_dict(orient="records")

        coins = []

        for coin in records:

            # -----------------------------
            # NAME
            # -----------------------------

            name = coin.get("Name", "")

            if pd.isna(name):
                name = "Unknown"

            name = str(name)

            # -----------------------------
            # SYMBOL
            # -----------------------------

            symbol = coin.get("Symbol", "")

            if pd.isna(symbol):
                symbol = ""

            symbol = str(symbol)

            # -----------------------------
            # RANK
            # -----------------------------

            rank = coin.get("Rank", "")

            try:
                rank = int(float(rank))
            except:
                rank = len(coins) + 1

            # -----------------------------
            # PRICE
            # -----------------------------

            price_raw = coin.get(
                "Price",
                coin.get("Price (USD)", 0)
            )

            price_value = clean_number(price_raw)

            # -----------------------------
            # 24H CHANGE
            # -----------------------------

            change_raw = coin.get(
                "24h Change",
                coin.get("24h Change (%)", 0)
            )

            change_value = clean_number(change_raw)

            # -----------------------------
            # MARKET CAP
            # -----------------------------

            market_cap_raw = coin.get(
                "Market Cap",
                coin.get("Market Cap (USD)", 0)
            )

            market_cap_value = clean_number(
                market_cap_raw
            )

            # -----------------------------
            # VOLUME
            # -----------------------------

            volume_raw = coin.get(
                "Volume 24h",
                coin.get("Volume 24h (USD)", 0)
            )

            volume_value = clean_number(
                volume_raw
            )

            # -----------------------------
            # FORMAT PRICE
            # -----------------------------

            if price_value >= 1:
                price_display = f"${price_value:,.2f}"
            else:
                price_display = f"${price_value:.6f}"

            # -----------------------------
            # FORMAT CHANGE
            # -----------------------------

            if change_value > 0:
                change_display = f"+{change_value:.2f}%"
                change_class = "positive"

            elif change_value < 0:
                change_display = f"{change_value:.2f}%"
                change_class = "negative"

            else:
                change_display = "0.00%"
                change_class = "neutral"

            # -----------------------------
            # FORMAT MARKET CAP
            # -----------------------------

            if market_cap_value >= 1_000_000_000_000:
                market_cap_display = (
                    f"${market_cap_value / 1_000_000_000_000:.2f}T"
                )

            elif market_cap_value >= 1_000_000_000:
                market_cap_display = (
                    f"${market_cap_value / 1_000_000_000:.2f}B"
                )

            elif market_cap_value >= 1_000_000:
                market_cap_display = (
                    f"${market_cap_value / 1_000_000:.2f}M"
                )

            else:
                market_cap_display = (
                    f"${market_cap_value:,.0f}"
                )

            # -----------------------------
            # FORMAT VOLUME
            # -----------------------------

            if volume_value >= 1_000_000_000:
                volume_display = (
                    f"${volume_value / 1_000_000_000:.2f}B"
                )

            elif volume_value >= 1_000_000:
                volume_display = (
                    f"${volume_value / 1_000_000:.2f}M"
                )

            else:
                volume_display = (
                    f"${volume_value:,.0f}"
                )

            # -----------------------------
            # FINAL COIN OBJECT
            # -----------------------------

            coins.append({
                "rank": rank,
                "name": name,
                "symbol": symbol,
                "price": price_display,
                "price_value": price_value,
                "change": change_display,
                "change_value": change_value,
                "change_class": change_class,
                "market_cap": market_cap_display,
                "volume": volume_display
            })

        return coins

    except Exception as e:

        print("Error loading crypto data:")
        print(e)

        return []


@app.route("/")
def home():

    coins = load_crypto_data()

    # -----------------------------
    # MARKET STATISTICS
    # -----------------------------

    total_coins = len(coins)

    gainers = [
        coin for coin in coins
        if coin["change_value"] > 0
    ]

    losers = [
        coin for coin in coins
        if coin["change_value"] < 0
    ]

    # Highest gain
    top_gainer = None

    if gainers:
        top_gainer = max(
            gainers,
            key=lambda x: x["change_value"]
        )

    # Highest loss
    top_loser = None

    if losers:
        top_loser = min(
            losers,
            key=lambda x: x["change_value"]
        )

    return render_template(
        "index.html",
        coins=coins,
        total_coins=total_coins,
        top_gainer=top_gainer,
        top_loser=top_loser
    )


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )