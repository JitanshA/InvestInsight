import yfinance as yf

# Define the ticker symbol
ticker_symbol = 'AAPL'

# Get the stock data
ticker_data = yf.Ticker(ticker_symbol)

# Define the time period
start_date = '2010-01-01'
end_date = '2023-06-01'

# Fetch the historical data
historical_data = ticker_data.history(start=start_date, end=end_date)

# Print the data
print(historical_data)



