import sys
import pandas as pd
sys.path.insert(0, './modules')
import data_receiver as dr

"""
Main class
"""

ticker = 'AZA.ST'


def main():
	df = dr.get_stock_data(ticker)
	df.to_csv(ticker + '.csv')
	print(str(len(df.index)) + " rows of data has been saved to: " + ticker + '.csv')

if __name__ == '__main__':
	main()
