import sys
import pandas as pd
sys.path.insert(0, './modules')
import data_receiver as dr
import export_data as ed

"""
Main class
"""

ticker = 'CLA-B.ST'


def main():
	df = dr.get_stock_data(ticker)
	ed.export_to_csv(df, ticker)

if __name__ == '__main__':
	main()
