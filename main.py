import pandas as pd
import requests

def get_volatility_data(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d&limit=365"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close'] = df['Close'].astype(float)
    df['Close'] = df['Close'].rolling(window=50).mean()
    df['return'] = df['Close'].pct_change()
    df['volatility'] = df['return'].rolling(window=50).std() * (252**0.5)
    df['symbol'] = symbol
    return df

def main():
    df_btc = get_volatility_data("BTCUSDT")
    df_eth = get_volatility_data("ETHUSDT")
    df = pd.concat([df_btc, df_eth])
    df = df.dropna()
    df.to_excel("Projet_otho.xlsx", index=False)

if __name__ == '__main__':
    main()

