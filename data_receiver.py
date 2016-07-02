import pandas as pd
import numpy as np
from datetime import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import backtrader.indicators as bti
import stock_indicators as sti

""" 
Class for receiving data from yahoo finance
Should not be runnable from terminal, only from olga.py
"""

style.use('ggplot')

start_time = datetime(2000, 01, 01)
end_time = datetime.now().date()

#	Receive stock info
df = web.DataReader('AZA.ST', 'yahoo', start_time, end_time)

#	Remove days when OMXS is closed ('Volume == 0')
df = df[df.Volume != 0]
#adj_close = df['Adj Close']

# plt.plot(sti.moving_avarages(df['Adj Close'], 12))
# plt.show()

print(df.tail(14))
delta_mas = []
len12 = len(sti.sma(df['Adj Close'], 12))
len26 = len(sti.sma(df['Adj Close'], 26))
print('12: ' + str(len12) + ", 26: " + str(len26))
for i in range(len(sti.sma(df['Adj Close'], 26))):
	ma12 = sti.sma(df['Adj Close'], 12)[len12 - i - 1]
	ma26 = sti.sma(df['Adj Close'], 26)[len26 - i - 1]
	delta_mas.append(ma12 - ma26)
delta_mas.reverse()
