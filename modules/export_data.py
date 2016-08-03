def export_to_csv(df, ticker):
	df.to_csv('./stock_data/' + ticker + '.csv')
	print(str(len(df.index)) + " rows of data has been saved to: " + ticker + '.csv')
