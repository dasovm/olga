import sys
sys.path.insert(0, './modules')
import data_receiver as dr
import stock_analyzer as sa
import export_data as ed
import import_data as id

"""
Main class
"""

ticker = 'AAK.ST'


def main():
    symbols = id.get_symbol_list()
    stock_count = len(symbols.splitlines())

    for symbol in symbols.splitlines():
        df = dr.get_stock_data(symbol + '.ST')
        ed.export_to_csv(df, symbol + '.ST')
        stock_count -= 1
        X, y = sa.build_data_set(sa.get_data_set_from_csv(symbol + '.ST'))
        sa.analyzis(X, y)
        print(str(stock_count) + ' stocks left.')
        print '----------\n'
        break


if __name__ == '__main__':
    main()
