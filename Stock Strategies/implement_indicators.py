#implement_indicators.py
'''The module that implements the indicators. They are implemented as classes.'''

import download_information
from datetime import datetime

class true_range_indicator:
	def buy_or_sell(self, date, data, date_range, n):
		'''Determines range of prices for current date, extending it if necessary based on the previous day's close.
		Returns as a percentage of previous day's closing price.'''
		high = float(data["Time Series (Daily)"][date]["2. high"])
		low = float(data["Time Series (Daily)"][date]["3. low"])
		r = high - low
		if date != date_range[0]:
			previous_index = date_range.index(date) - 1
			previous_close = float(data["Time Series (Daily)"][date_range[previous_index]]["4. close"])
			if previous_close > high:
				r = previous_close - low
			elif previous_close < low:
				r = high - previous_close
			t_range = '%.4f'%((r/previous_close)*100)
			return t_range

class simple_moving_average:

	def buy_or_sell(self, date, data, date_range, n):
		'''Given the user-chosen N as a parameter, returns the average value of the closing prices for N days'''
		total = 0

		if date_range.index(date) >= int(n)-1:
			for x in range(int(n)):
				total = total + float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x)]]["4. close"])
			return '%.4f'%(float(total / int(n)))

class simple_moving_average_volume:

	def buy_or_sell(self, date, data, date_range, n):
		'''Given the user-chosen N as a parameter, returns the average value of the number of shares traded (volume) for N days'''

		total = 0

		if date_range.index(date) >= int(n)-1:
			for x in range(int(n)):
				total = total + float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x)]]["5. volume"])
			return '%.4f'%(float(total / int(n)))

class directional_indicator:

	def buy_or_sell(self, date, data, date_range, n):
		'''Calculates the number of days the closing price went up or down from the previous day through incrementing count_up
		or count_down. Returns the difference of these two numbers. If the date index is below the given N, calculates 
		those numbers for whatever prices are available before that index.'''
		count_up = 0
		count_down = 0
		if date_range.index(date) == 0:
			return 0
		elif date_range.index(date) <= int(n)-1:
			for x in range(date_range.index(date)):
				if float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x)]]["4. close"]) > float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x-1)]]["4. close"]):
					count_up += 1
				elif float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x)]]["4. close"]) < float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x-1)]]["4. close"]):
					count_down += 1
			return count_up-count_down
		else:
			for x in range(int(n)):
				if float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x)]]["4. close"]) > float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x-1)]]["4. close"]):
					count_up += 1
				elif float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x)]]["4. close"]) < float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x-1)]]["4. close"]):
					count_down += 1
		return count_up-count_down

class directional_indicator_volume:

	def buy_or_sell(self, date, data, date_range, n):
		'''Calculates the number of days the volume went up or down from the previous day through incrementing count_up
		or count_down. Returns the difference of these two numbers. If the date index is below the given N, calculates 
		those numbers for whatever prices are available before that index.'''
		count_up = 0
		count_down = 0
		if date_range.index(date) == 0:
			return 0
		elif date_range.index(date) <= int(n)-1:
			for x in range(date_range.index(date)):
				if float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x)]]["5. volume"]) > float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x-1)]]["5. volume"]):
					count_up += 1
				elif float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x)]]["5. volume"]) < float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x-1)]]["5. volume"]):
					count_down += 1
			return count_up-count_down
		else:
			for x in range(int(n)):
				if float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x)]]["5. volume"]) > float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x-1)]]["5. volume"]):
					count_up += 1
				elif float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x)]]["5. volume"]) < float(data["Time Series (Daily)"][date_range[(date_range.index(date)-x-1)]]["5. volume"]):
					count_down += 1
		return count_up-count_down
