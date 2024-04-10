import requests as rq
from bs4 import BeautifulSoup
import pandas as pd
from decimal import Decimal
 
units = {
    'T': int(1e12),
    'B': int(1e9),
    'M': int(1e6),
    'K': int(1e3)
}

URL = 'https://companiesmarketcap.com/%s/marketcap/'
OUTPUT_UNIT = 'M'
OUTPUT_DIR = 'udataset/market_cap.csv'

names = {
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

def convert_market_cap_value(input: str) -> str:
    # Extract unit and numeric value
    unit = input[-1]
    str_market_cap = input[1:-2]
    
    # Convert to raw unit value
    value = Decimal(str_market_cap) * units[unit]
    
    # Convert to output unit
    return str(value / units[OUTPUT_UNIT])
    
def get_data(ticker):
    # Make a response to the website
    response = rq.get(URL % names[ticker])

    # Get the soup
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    
    # Store data for the current ticker
    data = []
    for row in table.find_all('tr'):
        # Find all cells on the row
        cells = row.find_all('td')
        
        # Check if empty row
        if not cells:
            continue
        
        # Extract values
        texts = [cell.text.strip() for cell in cells]
        year = texts[0]
        market_cap = texts[1]
        
        # Convert market cap to a standard unit
        market_cap = convert_market_cap_value(market_cap)
        
        # Add to output list 
        data.append([year, ticker, market_cap])
    
    # Return data
    return data

if __name__ == '__main__':
    
    # List of all data
    data = []
    
    # Fetch market cap data for all companies in ticker dict
    for ticker in names.keys():
        print(ticker)
        data += get_data(ticker)
        
    # Convert to DataFrame and output to csv
    df = pd.DataFrame(data, columns=['year', 'ticker', 'market_cap_' + OUTPUT_UNIT])
    df.to_csv(OUTPUT_DIR, index=False)