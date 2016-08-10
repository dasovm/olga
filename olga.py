import sys
import datetime
sys.path.insert(0, './modules')
import data_receiver as dr
import stock_analyzer as sa
import export_data as ed
import import_data as id
import transaction_handler as th

"""
Main class
"""

# Change to todays date in stable
date = datetime.datetime.now().date() - datetime.timedelta(days=1)
# date = datetime.datetime.now().date()


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
        prediction = sa.predict(X, y, last_day_data, symbol)
        th.update_stock_transactions(symbol, prediction, date, last_day_data)
        print(str(stock_count) + ' stocks left.')
        print '----------\n'
        # break


if __name__ == '__main__':
    main()
