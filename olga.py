import sys
sys.path.insert(0, './modules')
import data_receiver as dr

"""
Main class
"""


def main():
	print dr.get_stock_data('AZA.ST')

if __name__ == '__main__':
	main()
