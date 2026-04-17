from myfunctions import execute_this
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

class Model:
	"""docstring for model"""
	def __init__(self, name:str, test_accuracy:float, data_path:Path):
		self.test_accuracy = test_accuracy
		self.name = name
		self.response_time = None
		self.transaction_rate = None
		self.availability = None
		self.data_path = data_path
		self._populate()
	
	def _populate(self) -> None:
		with open(self.data_path/f"max_size_{self.data_path.parts[-1]}_half.txt", 'r', encoding="utf-8") as file:
			for line in file:
				if "Response time" in line:
					self.response_time = line.split(":")[-1].strip()
					self.response_time = float(self.response_time.split(" ")[0].strip())
				elif "Transaction rate" in line:
					self.transaction_rate = line.split(":")[-1].strip()
					self.transaction_rate = float(self.transaction_rate.split(" ")[0].strip())
				elif "Availability" in line:
					self.availability = line.split(":")[-1].strip()
					self.availability = float(self.availability.split("%")[0].strip())/100
	

@execute_this
def slide2():
	siege_result = Path("/Users/utkarsh/Desktop/Utkarsh/NYU/Year 1/Semester 2/Machine Learning/Labs/Lab 5/siege_results")
	pred_model = Model( "Predecessor's Model",0.6764, siege_result/"Pred")
	acc_model = Model("Accuracy Optimised Model",0.8832, siege_result/"Acc")
	infer_model = Model("Inference Optimised Model", 0.8769, siege_result/"Infer")

	fig, ax = plt.subplots()

	for model in (pred_model, acc_model, infer_model):
		ax.scatter(model.response_time, model.test_accuracy, label=model.name)

	ax.set_ylim(0.55, 1.1)
	ax.set_xlim(0, 3)
	ax.invert_xaxis()

	ax.grid(True, which='both')

	ax.legend()

	ax.minorticks_on()
	ax.grid(which='minor', alpha=0.2)
	ax.grid(which='major', alpha=0.5)

	x_axis = "Response Time"
	y_axis = "Test Accuracy"

	title = f"{y_axis} vs {x_axis} (Max Size Deployment)"

	ax.set_title(title)

	ax.set_xlabel(f"{x_axis} (sec)")
	ax.set_ylabel(y_axis)

	fig_manager = plt.get_current_fig_manager()
	fig_manager.set_window_title(title)

	plt.show()


