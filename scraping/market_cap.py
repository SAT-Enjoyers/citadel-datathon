from datetime import datetime
import json
import re
import requests as rq
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://companiesmarketcap.com/%s/marketcap/'
OUTPUT_DIR = 'udataset/market_cap.csv'
START_YEAR = 2000
END_YEAR = 2024

NAMES = {
    "QSR": "rbi",
    "ALG": "alamo-group",
    "SBUX": "starbucks",
    "CAG": "conagra-brands",
    "HRL": "hormel-foods",
    "DPZ": "dominos-pizza",
    "CMG": "chipotle-mexican-grill",
    "DRI": "darden-restaurants",
    "GIS": "general-mills",
    "TSCO": "tractor-supply",
    "MCD": "mcdonald",
    "PPC": "pilgrims",
    "VMI": "valmont-industries",
    "YUM": "yum",
    "SAP": "sap",
    "HSY": "hershey-company",
    "ADM": "archer-daniels-midland",
    "TSN": "tyson-foods",
    "AGCO": "agco",
    "KDP": "keurig-dr-pepper",
    "PEP": "pepsico",
    "CNHI": "cnh-industrial",
    "MNST": "monster-beverage",
    "WEN": "wendys-company",
    "DE": "deere-company",
    "CAT": "caterpillar",
    "COKE": "coca-cola-consolidated",
}


def get_data(ticker):
    # Make a response to the website and get the soup
    response = rq.get(URL % NAMES[ticker])
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the underlying data in the html script tag
    script_tag = soup.find('script', string=re.compile(r'data = \['))
    data_string = re.search(r'data = (\[.*?\]);', script_tag.string).group(1)

    # Parse the string as JSON to convert to a Python list
    raw_data = json.loads(data_string)

    data = []
    for item in raw_data:
        # Convert timestamp to date and format it
        date = datetime.fromtimestamp(item['d'])

        # Check year of data point
        if not START_YEAR <= date.year <= END_YEAR:
            continue

        # Format date for output
        year_month = f"{date.year}-{str(date.month).rjust(2,'0')}"

        # Only include the first value of each month
        if data and year_month == data[-1][0]:
            continue

        # Extract market cap
        market_cap = int(item['m']) * 100_000

        data.append([year_month, ticker, market_cap])

    return data


if __name__ == '__main__':
    # List of all data
    data = []

    # Fetch market cap data for all companies in ticker dict
    for ticker in NAMES.keys():
        print(ticker)
        data += get_data(ticker)

    # Convert to DataFrame and output to csv
    df = pd.DataFrame(data, columns=['YearMonth', 'Ticker', 'MarketCap'])
    df.to_csv(OUTPUT_DIR, index=False)
