import sys
sys.path.insert(0, './modules')
import data_receiver as dr
import export_data as ed
import import_data as id

"""
Main class
"""

ticker = 'AOI.ST'


def main():
	stock_count = 0
	symbols = id.get_symbol_list()
	for i in symbols.splitlines():
		stock_count += 1
	for symbol in symbols.splitlines():
		print ''
		df = dr.get_stock_data(symbol + '.ST')
		ed.export_to_csv(df, symbol + '.ST')
		stock_count -= 1
		print(str(stock_count) + ' stocks left.')
		print '----------'

if __name__ == '__main__':
	main()
