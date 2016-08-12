import datetime
import stock_analyzer as analyzer
import data_receiver as receiver
import export_data as exporter
import import_data as importer
import transaction_handler as th

"""
Main class
"""

# Should always be yesterday except for debug purpose
date = datetime.datetime.now().date() - datetime.timedelta(1)


def main():
    symbols = importer.get_symbol_list()
    stock_count = len(symbols.splitlines())

    for symbol in symbols.splitlines():
        df, last_day_data = receiver.get_stock_data(symbol + '.ST', end_time=date)
        # exporter.export_to_csv(df, symbol + '.ST')
        stock_count -= 1
        # X, y = analyzer.build_data_set(analyzer.get_data_set_from_csv(symbol + '.ST'))
        X, y = analyzer.build_data_set(df)
        # analyzer.train_and_test(X, y)
        prediction = analyzer.predict(X, y, last_day_data, symbol)
        th.update_stock_transactions(symbol, prediction, date, last_day_data)
        print(str(stock_count) + ' stocks left.')
        print '----------\n'
        # break


if __name__ == '__main__':
    main()
