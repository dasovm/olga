import pandas as pd
import numpy as np
from datetime import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import backtrader.indicators as bti
import stock_indicators as sti
import date_util

"""
Class for receiving data from yahoo finance
Should not be runnable from terminal, only from olga.py
"""

start_time = datetime(2000, 01, 01)
end_time = datetime.now().date()


def get_stock_data(stock_symbol):
	# Receive stock info
	df = web.DataReader(stock_symbol, 'yahoo', start_time, end_time)
	df['Date'] = df.index
	df['Day of week'] = date_util.get_weekday_from_serie(df['Date'])
	df['Month'] = date_util.get_month_from_serie(df['Date'])

	# Remove days when OMXS is closed ('Volume == 0')
	df = df[df.Volume != 0]
	df = df.drop('High', 1).drop('Low', 1).drop('Open', 1).drop('Close', 1)
	# df['MA'] = pd.rolling_mean(df['Adj Close'], 50)
	prices = df['Adj Close']
	df['RSI'] = sti.rsi(prices)
	return df.tail(50)

# delta_mas = []
# len12 = len(sti.sma(df['Adj Close'], 12))
# len26 = len(sti.sma(df['Adj Close'], 26))
# print('12: ' + str(len12) + ", 26: " + str(len26))
# for i in range(len(sti.sma(df['Adj Close'], 26))):
# 	ma12 = sti.sma(df['Adj Close'], 12)[len12 - i - 1]
# 	ma26 = sti.sma(df['Adj Close'], 26)[len26 - i - 1]
# 	delta_mas.append(ma12 - ma26)
# delta_mas.reverse()
