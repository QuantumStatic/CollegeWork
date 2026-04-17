from myfunctions import execute_this
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


@execute_this
def main():
	acc_model_data_path = Path('/Users/utkarsh/Desktop/Utkarsh/NYU/Year 1/Semester 2/Machine Learning/Labs/Lab 5/usage_files/infer')


	load_output = pd.read_csv(acc_model_data_path/'load_output.csv')
	resource_usage = pd.read_csv(acc_model_data_path/'resource_usage.csv')

	load_output.columns = load_output.columns.str.strip()
	resource_usage.columns = resource_usage.columns.str.strip()

	load_output["Availability"] = load_output["OKAY"] / (load_output["OKAY"] + load_output["Failed"])
	# plt.title('Visualisation of Load Output and Resource Usage')

	fig, axs = plt.subplots(2, 3, figsize=(18, 10))  # Creates a grid of 2x3

	# Subplot 1: Number of Requests Over Time
	sns.lineplot(ax=axs[0, 0], data=load_output, x='Date & Time', y='Trans')
	axs[0, 0].set_title('Number of Requests Over Time')
	axs[0, 0].set_xlabel('Time')
	axs[0, 0].set_ylabel('Transactions (Trans/sec)')
	axs[0, 0].tick_params(axis='x', rotation=45)
	axs[0, 0].set_xticks(axs[0, 0].get_xticks()[::len(load_output) // 8])

	# Subplot 2: Average Response Time Over Time
	sns.lineplot(ax=axs[0, 1], data=load_output, x='Date & Time', y='Resp Time')
	axs[0, 1].set_title('Average Response Time Over Time')
	axs[0, 1].set_xlabel('Time')
	axs[0, 1].set_ylabel('Response Time')
	axs[0, 1].tick_params(axis='x', rotation=45)
	axs[0, 1].set_xticks(axs[0, 1].get_xticks()[::len(load_output) // 8])

	# Subplot 3: Availability Over Time
	sns.lineplot(ax=axs[0, 2], data=load_output, x='Date & Time', y='Availability')
	axs[0, 2].set_title('Availability Over Time')
	axs[0, 2].set_xlabel('Time')
	axs[0, 2].set_ylabel('Availability')
	axs[0, 2].tick_params(axis='x', rotation=45)
	axs[0, 2].set_xticks(axs[0, 2].get_xticks()[::len(load_output) // 8])

	# Subplot 4: Number of Replicas Over Time
	sns.lineplot(ax=axs[1, 0], data=resource_usage, x='time', y='n_replica')
	axs[1, 0].set_title('Number of Replicas Over Time')
	axs[1, 0].set_xlabel('Time')
	axs[1, 0].set_ylabel('Number of Replicas')

	# Subplot 5: CPU Over Time
	sns.lineplot(ax=axs[1, 1], data=resource_usage, x='time', y='cpu_req_core', label='CPU Request')
	sns.lineplot(ax=axs[1, 1], data=resource_usage, x='time', y='cpu_lim_core', label='CPU Limit')
	sns.lineplot(ax=axs[1, 1], data=resource_usage, x='time', y='cpu_use_core', label='CPU Usage')
	axs[1, 1].set_title('CPU Over Time')
	axs[1, 1].set_xlabel('Time')
	axs[1, 1].set_ylabel('CPU Cores')
	axs[1, 1].legend()

	# Subplot 6: Memory Over Time
	sns.lineplot(ax=axs[1, 2], data=resource_usage, x='time', y='mem_req_KB', label='Memory Request')
	sns.lineplot(ax=axs[1, 2], data=resource_usage, x='time', y='mem_lim_KB', label='Memory Limit')
	sns.lineplot(ax=axs[1, 2], data=resource_usage, x='time', y='mem_use_KB', label='Memory Usage')
	axs[1, 2].set_title('Memory Over Time')
	axs[1, 2].set_xlabel('Time')
	axs[1, 2].set_ylabel('Memory (KB)')
	axs[1, 2].legend()

	plt.tight_layout()
	plt.show()


