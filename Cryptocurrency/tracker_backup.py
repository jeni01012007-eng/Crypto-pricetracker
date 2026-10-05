import csv
import os
from datetime import datetime

import pandas as pd

# ============================================================
# PROJECT SETTINGS
# ============================================================

CSV_FOLDER = "data"
CSV_FILE = os.path.join(CSV_FOLDER, "crypto_prices.csv")


# ============================================================
# SAMPLE DATA
# Used for offline testing when internet is unavailable
# ============================================================

def get_sample_data():

    records = [
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rank": "1",
            "coin": "Bitcoin",
            "price": "$67,500",
            "change_24h": "5.25%",
            "market_cap": "$1.34T"
        },
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rank": "2",
            "coin": "Ethereum",
            "price": "$3,450",
            "change_24h": "3.15%",
            "market_cap": "$414B"
        },
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rank": "3",
            "coin": "Tether",
            "price": "$1.00",
            "change_24h": "0.05%",
            "market_cap": "$120B"
        },
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rank": "4",
            "coin": "BNB",
            "price": "$610",
            "change_24h": "6.20%",
            "market_cap": "$91B"
        },
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rank": "5",
            "coin": "Solana",
            "price": "$165",
            "change_24h": "7.45%",
            "market_cap": "$76B"
        },
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rank": "6",
            "coin": "XRP",
            "price": "$0.52",
            "change_24h": "2.80%",
            "market_cap": "$30B"
        },
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rank": "7",
            "coin": "USD Coin",
            "price": "$1.00",
            "change_24h": "0.02%",
            "market_cap": "$28B"
        },
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rank": "8",
            "coin": "Cardano",
            "price": "$0.45",
            "change_24h": "5.60%",
            "market_cap": "$16B"
        },
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rank": "9",
            "coin": "Avalanche",
            "price": "$36.50",
            "change_24h": "4.20%",
            "market_cap": "$14B"
        },
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rank": "10",
            "coin": "Dogecoin",
            "price": "$0.14",
            "change_24h": "8.10%",
            "market_cap": "$20B"
        }
    ]

    return records


# ============================================================
# SAVE DATA TO CSV
# ============================================================

def save_to_csv(records):

    if not records:
        print("\nNo data to save.")
        return

    os.makedirs(CSV_FOLDER, exist_ok=True)

    file_exists = os.path.exists(CSV_FILE)

    fieldnames = [
        "timestamp",
        "rank",
        "coin",
        "price",
        "change_24h",
        "market_cap"
    ]

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        if not file_exists:
            writer.writeheader()

        writer.writerows(records)

    print("\nData successfully saved!")
    print("CSV file:", CSV_FILE)


# ============================================================
# DISPLAY ALL DATA
# ============================================================

def display_data(records):

    if not records:
        print("\nNo cryptocurrency data found.")
        return

    dataframe = pd.DataFrame(records)

    print("\n")
    print("=" * 110)
    print("                 CRYPTOCURRENCY PRICE TRACKER")
    print("=" * 110)

    print(
        dataframe[
            [
                "rank",
                "coin",
                "price",
                "change_24h",
                "market_cap"
            ]
        ].to_string(index=False)
    )

    print("=" * 110)


# ============================================================
# FILTER COINS
# ============================================================

def filter_coins(records, minimum_change):

    filtered = []

    for record in records:

        change = record["change_24h"]

        change = change.replace("%", "")
        change = change.replace(",", "")
        change = change.strip()

        try:

            change_value = float(change)

            if change_value >= minimum_change:
                filtered.append(record)

        except ValueError:
            continue

    return filtered


# ============================================================
# DISPLAY FILTERED COINS
# ============================================================

def display_filtered_coins(records):

    print("\n")
    print("=" * 70)
    print("          COINS WITH 24-HOUR GAIN >= 5%")
    print("=" * 70)

    if not records:

        print("No coins matched the filter.")

    else:

        for record in records:

            print(
                f"{record['coin']} --> "
                f"{record['change_24h']}"
            )

    print("=" * 70)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("        CRYPTOCURRENCY PRICE TRACKER")
    print("=" * 60)

    print("\nOFFLINE TEST MODE")
    print("Internet connection is not required.")
    print("Using sample cryptocurrency data...")

    # Get sample data
    records = get_sample_data()

    # Display cryptocurrency data
    display_data(records)

    # Save data to CSV
    save_to_csv(records)

    # Filter coins with 5% or more gain
    filtered_coins = filter_coins(
        records,
        minimum_change=5
    )

    # Display filtered coins
    display_filtered_coins(filtered_coins)

    print("\nProject completed successfully!")
    print("Offline test completed successfully.")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()