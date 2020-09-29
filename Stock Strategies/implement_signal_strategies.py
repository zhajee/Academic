#implement_signal_strategies.py
'''The module that implements the signal strategies. They are implemented as classes.'''

import implement_indicators
import download_information


class true_range_signal:

	def buy_or_sell(self, date, data, date_range, indicator, buy_threshold, sell_threshold, i):
		'''Determines whether to return a buy or sell signal based on whether the true range as a percentage 
		(given as indicator) is above or below the buy or sell thresholds given. Returns the result in a list.'''
		signal = ''
		signal_two = ''
		previous_index = date_range.index(date) - 1
		p_close = (data["Time Series (Daily)"][date_range[previous_index]]["4. close"])
		if indicator == '':
			return ['', '']
		else:
			#BUY SIGNAL
			if buy_threshold[0] == '>':
				if indicator > buy_threshold[1:]:
					signal = 'BUY'
			else:
				if indicator < buy_threshold[1:]:
					signal = 'BUY'

			#SELL SIGNAL
			if sell_threshold[0] == '>':
				if indicator > sell_threshold[1:]:
					signal_two = 'SELL'

			else:
				if indicator < sell_threshold[1:]:
					signal_two = 'SELL'

			l = [signal, signal_two]
			return l

class simple_moving_average_signal:

	def buy_or_sell(self, date, data, date_range, indicator, buy_threshold, sell_threshold, i):
		'''Determines if the date's closing price crosses over the simple moving average (given as parameter), 
		generating a buy signal. Determines if the date's closing price crosses below the simple moving average,
		generating a sell signal. Returns result as a list.'''
		signal = ''
		signal_two = ''
		previous_index = date_range.index(date) - 1
		close = data["Time Series (Daily)"][date]["4. close"]
		p_close = (data["Time Series (Daily)"][date_range[previous_index]]["4. close"])
		p_indicator = i[i.index(indicator)-1]
		if indicator == '':
			return ['', '']
		elif (i[date_range.index(date)-1]) == '':
			return ['', '']
		else:
			if close > indicator and p_close < p_indicator:
				signal = 'BUY'
			elif close < indicator and p_close > p_indicator:
				signal_two = 'SELL'
			else:
				signal = ''
				signal_two = ''

			l = [signal, signal_two]
			return l

class simple_moving_average_signal_volume:

	def buy_or_sell(self, date, data, date_range, indicator, buy_threshold, sell_threshold, i):
		'''Determines if the date's volume crosses over the simple moving average (given as parameter), 
		generating a buy signal. Determines if the date's volume crosses below the simple moving average,
		generating a sell signal. Returns result as a list.'''
		signal = ''
		signal_two = ''
		previous_index = date_range.index(date) - 1
		close = data["Time Series (Daily)"][date]["5. volume"]
		p_close = (data["Time Series (Daily)"][date_range[previous_index]]["5. volume"])
		p_indicator = i[i.index(indicator)-1]
		if indicator == '':
			return ['', '']
		elif (i[date_range.index(date)-1]) == '':
			return ['', '']
		else:
			if close > indicator and p_close < indicator:
				signal = 'BUY'
			elif close < indicator and p_close > indicator: 
				signal_two = 'SELL'
			else:
				signal = '\t'
				signal_two = '\t'

			l = [signal, signal_two]
			return l

class directional_signal:

	def buy_or_sell(self, date, data, date_range, indicator, buy_threshold, sell_threshold, i):
		'''Determines if the directional indicator of the closing price has crossed above the buy threshold, generating a buy signal.
		Determines if the directional indicator has crossed below the sell threshold, generating a sell signal.
		Returns result as a list.'''
		p_indicator = i[((date_range.index(date))-1)]

		if indicator > int(buy_threshold) and not (p_indicator > int(buy_threshold)):
			signal = 'BUY'
		else:
			signal = ''
		if indicator < int(sell_threshold) and (p_indicator >= int(sell_threshold)): 
			signal_two = 'SELL'
		else:
			signal_two = ''

		l = [signal, signal_two]
		return l

class directional_signal_volume:

	def buy_or_sell(self, date, data, date_range, indicator, buy_threshold, sell_threshold, i):
		'''Determines if the directional indicator of the volume has crossed above the buy threshold, generating a buy signal.
		Determines if the directional indicator has crossed below the sell threshold, generating a sell signal.
		Returns result as a list.'''
		p_indicator = i[((date_range.index(date))-1)]
		if indicator > int(buy_threshold) and not (p_indicator > int(buy_threshold)):
			signal = 'BUY'
		else:
			signal = ''
		if indicator < int(sell_threshold) and (p_indicator >= int(sell_threshold)): 
			signal_two = 'SELL'
		else:
			signal_two = ''

		l = [signal, signal_two]
		return l
