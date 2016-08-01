import sys
import pandas as pd
sys.path.insert(0, './modules')
import data_receiver as dr

"""
Main class
"""

ticker = 'AZA.ST'


def main():
	print("Crunshin' dem " + ticker + ' data for yah...')
	df = dr.get_stock_data(ticker)
	df.to_csv(ticker + '.csv')
	print('Finish.')

if __name__ == '__main__':
	main()
