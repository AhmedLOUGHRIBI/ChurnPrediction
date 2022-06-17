from Utils.utils import plot_cumulative_gain
from matplotlib import pyplot as plt
from sklearn import metrics


class Evaluator:

    def show_results(self, test):

        plot_cumulative_gain(test.TARGET, test.PREDICTION)

        fpr, tpr, _ = metrics.roc_curve(test.TARGET, test.PREDICTION)
        auc = metrics.roc_auc_score(test.TARGET, test.PREDICTION)
        print('auc score: {}'.format(auc))
        plt.plot(fpr, tpr, label="auc=" + str(auc))
        plt.legend(loc=4)
        plt.show()

