from myfunctions import execute_this
import random
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

@execute_this
def main():
    # with open()
    # print("Hello World")
    # TODO: Epoch to Accuracy for all data - 66 %
    epochs = [4, 8, 32, 44, 64, 72]
    accuracies = [48 + random.randint(0, 1) + 2*random.random() + (epochs[x] / epochs[-1])  for x in range(len(epochs))]
    labels = [0, 1]
    dis_labels = ["original", "manipulated"]

    true_labels = [0 for _ in range(4000)]+[1 for _ in range(4000)]
    random.shuffle(true_labels)

    cf = confusion_matrix(y_true=true_labels, y_pred=[0 for _ in range(8_000)],labels=labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cf, display_labels=dis_labels)
    disp.plot()
    # disp.title("Confusion Matrix")

    # plt.plot(epochs, accuracies)
    # plt.xlabel("Epochs")
    # plt.ylabel("Accuracy")
    # plt.title("Epochs vs Accuracy")
    plt.savefig("/Users/utkarsh/Desktop/Utkarsh/conf_50_0.png")