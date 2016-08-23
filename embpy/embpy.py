"""
A set of functions for embedding a pandas series.

By nick cortale

TODO:
The combine function is weird and needs to be rewritten
"""
import pandas as pd
import embpy.utilities as ut


class embed:
	"""Creates features, targets, and comparitive values for
	time series forecasting"""

	def __init__(self,series):
		"""
		Takes a pandas series and embeds it in n dimensional space.
		It is sensitive to times. Makes a copy of the dataframe and returns a new dataframe

		Parameters
		----------
		series : pandas series
		"""

		self.series = series.copy()

	def feature_calc(self, lags, freq=None):
		"""
		Calculates the features (aka lag values) of the time series.

		Parameters
		----------
		lags : list of lag values
		freq : string for dealing with time series. see pandas.shift for more.
		"""

		self.features = pd.DataFrame(self.series)
		self.features.columns=['00']

		for lag in lags:

			col_name = str(lag).zfill(2) #leading zero

			shifted = self.series.shift(periods=lag, freq=freq)

			self.features[col_name] = shifted

	def target_calc(self, distances, freq=None):
		"""
		Calculates the targets (aka future time series values).

		Parameters
		----------
		distances : how far to predict out in time
		freq : string for dealing with time series. see pandas.shift for more.
		"""

		for i,dist in enumerate(distances):

			if i==0: #create the target dataframe
				c_name = str(dist).zfill(2)
				self.targets = pd.DataFrame(self.series.shift(-dist,freq))
				self.targets.columns=[c_name]

			else:
				c_name = str(dist).zfill(2)
				self.targets[c_name] = self.series.shift(-dist,freq)


	def compare_calc(self,distances,freq=None):
		"""
		This is the same thing as the lag values. Except it is used to evaluate
		predictions. For example, some useful comparitive values are:
			0 : persistance, use todays value for tomorrows forecast
			6 : One week ago, it is actually 7 days ago from your forecast value
			364 : One year ago, same as the week forecast

		An example to grab the persistance, one week ago, and one year ago:
			compare_calc([0,6,364], freq='d')
		"""


		for i,dist in enumerate(distances):

			if i==0: #create the target dataframe
				c_name = str(dist).zfill(2)
				self.compare = pd.DataFrame(self.series.shift(dist, freq))
				self.compare.columns=[c_name]

			else:
				c_name = str(dist).zfill(2)
				self.compare[c_name] = self.series.shift(dist, freq)


	def combine(self):
		"""
		Combines the available dataframes into one dataframe and gives them
		a nice multiIndex for efficiently grabbing features or targets.
		"""

		#give features a mutliIndex
		try:
			f_cols = ut.make_multi_index(self.features.columns,'features')
			self.features.columns = f_cols
		except:
			pass

		#give target a multiIndex
		try:
			t_cols = ut.make_multi_index(self.targets.columns,'targets')
			self.targets.columns = t_cols
		except:
			pass

		#give compare a multiIndex
		try:
			c_cols = ut.make_multi_index(self.compare.columns,'compare')
			self.compare.columns = c_cols
		except:
			pass

		#finally innerjoin these bad boys
		try:
			self.X = self.features.join(self.targets)
			self.X = self.X.join(self.compare)
		except:
			self.X = self.X = self.features.join(self.targets)
