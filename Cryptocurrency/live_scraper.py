import os
import time
import pandas as pd
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# COINMARKETCAP LIVE SCRAPER
# ============================================================

URL = "https://coinmarketcap.com/"

CSV_FILE = os.path.join("data", "crypto_prices.csv")


def start_browser():

    options = Options()

    # Browser opens normally
    options.add_argument("--start-maximized")

    # Reduce automation detection
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )

    options.add_experimental_option(
        "useAutomationExtension",
        False
    )

    driver = webdriver.Chrome(options=options)

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


def get_live_data():

    driver = start_browser()

    rows = []

    try:

        print("Opening CoinMarketCap...")

        driver.get(URL)

        wait = WebDriverWait(driver, 30)

        # Wait for cryptocurrency table
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table")
            )
        )

        print("CoinMarketCap loaded successfully.")

        # Give the page some time to load dynamic content
        time.sleep(5)

        table = driver.find_element(By.CSS_SELECTOR, "table")

        table_rows = table.find_elements(
            By.CSS_SELECTOR,
            "tbody tr"
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        print("\nReading live cryptocurrency data...\n")

        for row in table_rows[:10]:

            try:

                cells = row.find_elements(By.TAG_NAME, "td")

                if len(cells) < 7:
                    continue

                # Get complete row text
                texts = [
                    cell.text.strip()
                    for cell in cells
                ]

                # CoinMarketCap table structure
                rank = texts[0]

                name = ""

                # Find coin name from row
                try:

                    name_element = row.find_element(
                        By.CSS_SELECTOR,
                        "p.coin-item-name"
                    )

                    name = name_element.text.strip()

                except:

                    # Fallback
                    if len(texts) > 2:
                        name = texts[2].split("\n")[0]

                # Symbol
                symbol = ""

                try:

                    symbol_element = row.find_element(
                        By.CSS_SELECTOR,
                        "p.coin-item-symbol"
                    )

                    symbol = symbol_element.text.strip()

                except:

                    pass

                # Price
                price = ""

                try:

                    price_element = row.find_element(
                        By.CSS_SELECTOR,
                        "span"
                    )

                    # Search text containing $
                    for element in row.find_elements(
                        By.CSS_SELECTOR,
                        "span"
                    ):

                        text = element.text.strip()

                        if "$" in text:
                            price = text
                            break

                except:

                    pass

                # 24 hour change
                change_24h = ""

                try:

                    # Find percentage values
                    for element in row.find_elements(
                        By.TAG_NAME,
                        "span"
                    ):

                        text = element.text.strip()

                        if "%" in text:

                            if not change_24h:
                                change_24h = text

                except:

                    pass

                # Store record
                rows.append({
                    "Timestamp": timestamp,
                    "Rank": rank,
                    "Name": name,
                    "Symbol": symbol,
                    "Price": price,
                    "24h Change": change_24h
                })

            except Exception:

                continue

        print(
            f"Collected {len(rows)} cryptocurrency records."
        )

    except Exception as e:

        print("\nError while reading CoinMarketCap:")
        print(e)

    finally:

        driver.quit()

    return pd.DataFrame(rows)


def save_data(df):

    if df.empty:

        print("\nNo cryptocurrency data collected.")
        return

    os.makedirs("data", exist_ok=True)

    file_exists = os.path.exists(CSV_FILE)

    df.to_csv(
        CSV_FILE,
        mode="a",
        index=False,
        header=not file_exists
    )

    print(
        f"\nSaved to: {CSV_FILE}"
    )


def main():

    print("=" * 80)
    print("COINMARKETCAP LIVE CRYPTOCURRENCY TRACKER")
    print("=" * 80)

    df = get_live_data()

    if not df.empty:

        print("\n")
        print(df.to_string(index=False))

        print("\n" + "=" * 80)

        save_data(df)

    else:

        print(
            "\nCould not collect live data from CoinMarketCap."
        )


if __name__ == "__main__":

    main()