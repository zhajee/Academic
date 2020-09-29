#project3.py
'''The module that implements the input and output portion of the program.'''

import download_information
import implement_indicators
import implement_signal_strategies
from pathlib import Path
from datetime import date, timedelta, datetime

def get_input() -> str:
	'''Takes in 5 lines of input from the user, and calls methods to get the apikey 
	and indicator identification, and stores all of these into a list called returning_input'''
	returning_input = []

	path_to_key = str(input()) 
	apikey = get_apikey(path_to_key) 
	symbol = input() 
	start_date = input() 
	end_date = input() 
	strategy = input() 

	indic = get_indic(strategy) 
	signal = get_signal(indic, strategy)

	returning_input.extend([apikey, symbol, start_date, end_date, strategy, indic])
	return returning_input

def get_apikey(path_to_key: Path) -> str:
	'''Takes in the path inputted by the user, reads the first line, and returns it as a string'''
	the_file = open(path_to_key, 'r')
	apikey = the_file.readline()[:-1]
	the_file.close()
	return apikey

def get_indic(strategy: str) -> str:
	'''Returns the string indicator identification taken from the strategy inputted by the user'''
	return strategy[0:2]

def get_signal(indic: str, strategy: str) -> list:
	'''Takes in the strategy and indicator identification and returns the number of days, 
	buy threshold, and sell threshold as a list'''
	input_strategy = strategy.split(' ')
	return_statement = []

	if indic == 'TR':
		buy_threshold = input_strategy[1]
		sell_threshold = input_strategy[2]
		return_statement.extend(['None', buy_threshold, sell_threshold])
		return return_statement

	if indic == 'MP' or indic == 'MV':
		number_of_days = input_strategy[1]
		return_statement.extend([number_of_days, 'None', 'None'])
		return return_statement

	if indic == 'DP' or indic == 'DV':
		number_of_days = input_strategy[1]
		buy_threshold = input_strategy[2]
		sell_threshold = input_strategy[3]

		return_statement.extend([number_of_days, buy_threshold, sell_threshold])
		return return_statement

def determine_date_range(start_date: str, end_date: str, data: dict) -> list:
	'''Uses datetime.timedelta to determine the dates in between the start and end date
	given by the user and creates a list to store these as long as they are in the API data.
	Uses a try except in case the user enters the wrong api key.'''

	try:
		start = date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2])) 
		end = date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))   

		delta = end - start       #timedelta

		date_range = []
		for i in range(delta.days + 1):
		    day = start + timedelta(days=i)
		    if ((day.isoweekday() == 6) == False) and ((day.isoweekday() == 7) == False) and str(day) in data["Time Series (Daily)"]:
		    	date_range.append(str(day))
		return date_range
	except:
		return []

def execute(data: dict, date_range: list, function, n: str) -> list:
	'''Constructs and object that calls the indicator classes and appends whatever is 
	returned into a list called indicators'''
	indicators = []
	for date in date_range:
		obj = function
		obj = obj.buy_or_sell(date, data, date_range, n)
		if obj == None:
			obj = ''
		indicators.append(obj)
	return indicators

def get_indicators(indic: str, data: dict, date_range: list, true_range_indicator: str, simple_moving_average: str, simple_moving_average_volume: str, directional_indicator: str, directional_indicator_volume: str, n: str) -> list:
	'''Based on the indicator identification, calls the execute method that calls the respective class'''

	if indic == 'TR':
		i = execute(data, date_range, true_range_indicator, n)
	elif indic == 'MP':
		i = execute(data, date_range, simple_moving_average, n)
	elif indic == 'MV':
		i = execute(data, date_range, simple_moving_average_volume, n)
	elif indic == 'DP':
		i = execute(data, date_range, directional_indicator, n)
	elif indic == 'DV':
		i = execute(data, date_range, directional_indicator_volume, n)
	return i


def execute_signals(data: dict, date_range: list, function: str, buy_threshold: str, sell_threshold: str, i: list) -> list:
	'''Takes in the data, the list of dates, the class name, buy and sell thresholds, and the list of indicators,
	and constructs an object that calls the respective signal classes'''

	signals = []
	x = 0
	for date in date_range:
		x+=1
		indicator = i[x-1]
		obj = function
		obj = obj.buy_or_sell(date, data, date_range, indicator, buy_threshold, sell_threshold, i)
		if obj == None:
			obj = ''
		signals.append(obj)
	return signals

def signals(indic: str, data: dict, date_range: list, true_range_signal: str, simple_moving_average_signal: str, simple_moving_average_signal_volume: str, directional_signal: str, directional_signal_volume: str, buy_threshold: str, sell_threshold: str, i: list) -> list:
	'''Takes in the indicator identification, the dictionary of data, the list of dates, all the signal classes, 
	the buy and sell thresholds, and the list of indicators. Calls execute_signals for each indicator identification
	and stores the resulting list in s, which is returned.'''

	if indic == 'TR':
		s = execute_signals(data, date_range, true_range_signal, buy_threshold, sell_threshold, i)
	elif indic == 'MP':
		s = execute_signals(data, date_range, simple_moving_average_signal, buy_threshold, sell_threshold, i)
	elif indic == 'MV':
		s = execute_signals(data, date_range, simple_moving_average_signal_volume, buy_threshold, sell_threshold, i)
	elif indic == 'DP':
		s = execute_signals(data, date_range, directional_signal, buy_threshold, sell_threshold, i)
	elif indic == 'DV':
		s = execute_signals(data, date_range, directional_signal_volume, buy_threshold, sell_threshold, i)

	return s 

def generate_s_buy(s: list):
	'''Creates a list called s_buy and appends each 'BUY' value from the list of objects 
	that is passed into the list, that is returned.'''
	s_buy = []
	for item in s:
		s_buy.append(item[0])
	return s_buy

def generate_s_sell(s: list):
	'''Creates a list called s_buy and appends each 'BUY' value from the list of objects 
	that is passed into the list, that is returned.'''
	s_sell = []
	for item in s:
		s_sell.append(item[1])
	return s_sell


def print_header() -> None:
	'''Prints the tab-delimited header.'''
	print('Date\tOpen\tHigh\tLow\tClose\tVolume\tIndicator\tBuy?\tSell?')

def print_report(indic: str, data: dict, date_range: list, i: list, s_buy: list, s_sell: list) -> None:
	'''For each date in the list of dates, prints the opening price, highest price, lowest price,
	closing price, number of shares traded (volume), the indicator, and if there was a buy or sell signal.'''

	x = 0
	for date in date_range:
		x+=1 #x is used here to increment the indicator and signal lists as they are printed for each day.
		print(date, end = '\t')
		print(data["Time Series (Daily)"][date]["1. open"], end = '\t')
		print(data["Time Series (Daily)"][date]["2. high"], end = '\t')
		print(data["Time Series (Daily)"][date]["3. low"], end = '\t')
		print(data["Time Series (Daily)"][date]["4. close"], end = '\t')
		print(data["Time Series (Daily)"][date]["5. volume"], end = '\t')
		if indic == 'DP' or indic == 'DV':
			if i[x-1] > 0:
				print('+', end='')
		print(i[x-1], end = '\t')
		print(s_buy[x-1], end = '\t')
		print(s_sell[x-1])

def print_output(indic: str, symbol: str, strategy: str, apikey: str, date_range: list, i: list, s_buy: list, s_sell: list, data: dict) -> None:
	'''Prints all the output, included the stock symbol, number of days, the strategy, header, and entire report.'''

	print(symbol)
	print(len(date_range))
	print(strategy)

	print_header()

	print_report(indic, data, date_range, i, s_buy, s_sell)

if __name__ == '__main__':
	inp = get_input()
	sig = get_signal(inp[5], inp[4])
	data = download_information.convert_to_python_obj(download_information.build_search_url(inp[0], inp[1]))
	date_range = determine_date_range(inp[2], inp[3], data)
	i = get_indicators(inp[5], data, date_range, implement_indicators.true_range_indicator(), implement_indicators.simple_moving_average(), implement_indicators.simple_moving_average_volume(), implement_indicators.directional_indicator(), implement_indicators.directional_indicator_volume(), sig[0])
	s = signals(inp[5], data, date_range, implement_signal_strategies.true_range_signal(), implement_signal_strategies.simple_moving_average_signal(), implement_signal_strategies.simple_moving_average_signal_volume(), implement_signal_strategies.directional_signal(), implement_signal_strategies.directional_signal_volume(), sig[1], sig[2], i)
	s_buy = generate_s_buy(s)
	s_sell = generate_s_sell(s)
	print_output(inp[5], inp[1], inp[4], inp[0], date_range, i, s_buy, s_sell, data)
