import yfinance as yf
import pandas as pd

def compute_macd(df):
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

# Read tickers
with open("ticker.txt") as f:
    tickers = [line.strip().upper() for line in f]

results = []

for ticker in tickers:
    data = yf.download(ticker, period="6mo", auto_adjust=True, progress=False)
    if data.empty:
        continue
    
    data['MACD'], data['Signal'] = compute_macd(data)
    data.dropna(inplace=True)

    # Check last ~5 days for a crossover
    recent = data.tail(6)  # last 6 includes potential crossover yesterday
    cross_up = False
    for i in range(1, len(recent)):
        prev_macd = recent['MACD'].iloc[i-1]
        prev_signal = recent['Signal'].iloc[i-1]
        macd = recent['MACD'].iloc[i]
        signal = recent['Signal'].iloc[i]

        # Bullish crossover: MACD crosses above Signal
        if prev_macd <= prev_signal and macd > signal:
            cross_up = True
            break

    if cross_up:
        results.append(ticker)

print("Stocks with bullish MACD crossover in last ~5 days:")
for s in results:
    print(s)

