import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# List of cryptocurrency symbols
selected_crypto_symbols = [
    'BTC-USD', 'ETH-USD', 'XRP-USD', 'LTC-USD', 'BCH-USD', 'ADA-USD', 'DOT-USD',
    'BNB-USD', 'LINK-USD', 'XLM-USD', 'DOGE-USD', 'UNI-USD', 'AAVE-USD', 'ATOM-USD',
    'AVAX-USD', 'MATIC-USD', 'SOL-USD', 'CHR-USD', 'ALGO-USD', 'FTT-USD', 'VET-USD',
    'FIL-USD', 'TRX-USD', 'ETC-USD', 'SHIB-USD', 'EOS-USD', 'THETA-USD', 'NEO-USD',
    'DASH-USD', 'ZEC-USD'
]

# Date range: last year
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# Download data for the selected symbols at once
try:
    print("Downloading data for selected cryptocurrencies...")
    crypto_data = yf.download(
        selected_crypto_symbols,
        start=start_date.strftime('%Y-%m-%d'),
        end=end_date.strftime('%Y-%m-%d'),
        interval='1d',
        group_by='ticker',
        auto_adjust=True  # explicitly set for clarity
    )
except Exception as e:
    print(f"Error during download: {e}")
    crypto_data = pd.DataFrame()

# Reorganize data if multiple symbols
if not crypto_data.empty:
    all_crypto_data = []
    for symbol in selected_crypto_symbols:
        if symbol in crypto_data.columns.levels[0]:
            df_symbol = crypto_data[symbol].copy()
            df_symbol['Symbol'] = symbol
            all_crypto_data.append(df_symbol)
        else:
            print(f"No data for {symbol}")
    combined_df = pd.concat(all_crypto_data).reset_index()

    # Pivot data for easy analysis
    pivoted_data = combined_df.pivot_table(
        index='Date',
        columns='Symbol',
        values=['Open', 'High', 'Low', 'Close', 'Volume']
    )
    # Flatten MultiIndex columns
    pivoted_data.columns = [f"{col[1]}_{col[0]}" for col in pivoted_data.columns]
else:
    print("No data retrieved.")


# Extract unique crypto symbols based on column prefixes
selected_crypto_symbols_prefix = sorted(set(col.split('_')[0] for col in pivoted_data.columns))

# Define the standard columns to ensure order consistency
metrics = ['Open', 'High', 'Low', 'Close', 'Volume']

# Create a sorted list of column names grouped by crypto symbol
sorted_columns = [f"{crypto}_{metric}" for crypto in selected_crypto_symbols_prefix for metric in metrics]

# Check if all sorted columns exist in the DataFrame
missing_columns = [col for col in sorted_columns if col not in pivoted_data.columns]
if missing_columns:
    print(f"Warning: Missing columns {missing_columns}")

# Reorder the columns of the DataFrame (ignoring any missing columns)
existing_sorted_columns = [col for col in sorted_columns if col in pivoted_data.columns]
processed_crypto_data = pivoted_data[existing_sorted_columns]

# Sort data by date in descending order
processed_crypto_data = processed_crypto_data.sort_index(ascending=False)
