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
        df, last_day_data = dr.get_stock_data(symbol + '.ST')
        # ed.export_to_csv(df, symbol + '.ST')
        stock_count -= 1
        # X, y = sa.build_data_set(sa.get_data_set_from_csv(symbol + '.ST'))
        X, y = sa.build_data_set(df)
        # sa.train_and_test(X, y)
        sa.predict(X, y, last_day_data, symbol)
        print(str(stock_count) + ' stocks left.')
        print '----------\n'
        # break


if __name__ == '__main__':
    main()
