import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

from myfunctions import execute_this


@execute_this
def main():

	data = pd.read_csv('../usage_files/load_output.csv')
	r_usage = pd.read_csv('../usage_files/resource_usage.csv')

	data.columns = data.columns.str.strip()
	r_usage.columns = r_usage.columns.str.strip()


	# data['Date & Time'] = pd.to_datetime(data['Date & Time'])
	# data["Availability"] = data["OKAY"] / (data["OKAY"] + data["Failed"])

	# col = "Availability"

	# plt.figure(figsize=(10, 6))
	# sns.lineplot(data=data, x='Date & Time', y=col)
	# sns.pointplot(data=data, x='Date & Time', y='Trans Rate')
	# sns.barplot(data=data, x='Date & Time', y=col)
	# plt.title(f'{col} Over Time')
	# plt.xticks(rotation=45)
	# fig_manager = plt.get_current_fig_manager()
	# fig_manager.set_window_title(f'{col} over time')
	# plt.show()

	# r_usage['Date & Time'] = pd.to_datetime(data['Date & Time'])

	col = "n_replica"

	plt.figure(figsize=(10, 6))
	sns.lineplot(data=r_usage, x='time', y=col)

	# ax = plt.gca()
	# ax.xaxis.set_major_locator(mdates.SecondLocator(interval=25))

	# sns.pointplot(data=r_usage, x='Date & Time', y='Trans Rate')
	# sns.barplot(data=r_usage, x='Date & Time', y=col)
	plt.title(f'{col} Over Time')
	plt.xticks(rotation=45)
	fig_manager = plt.get_current_fig_manager()
	fig_manager.set_window_title(f'{col} over time')
	plt.show()
