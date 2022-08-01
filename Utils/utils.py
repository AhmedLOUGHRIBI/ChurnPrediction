import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def list_precedent_months(yearmonth, number):
    l=[]
    for i in range(number):
        if yearmonth%100 !=1:
            l.append(yearmonth)
            yearmonth = yearmonth -1
        else:
            l.append(yearmonth)
            yearmonth = yearmonth - 89
    return l


def cumulative_gain_curve(y_true, y_score, pos_label=None):
    """This function generates the points necessary to plot the Cumulative Gain
    Note: This implementation is restricted to the binary classification task.
    Args:
        y_true (array-like, shape (n_samples)): True labels of the data.
        y_score (array-like, shape (n_samples)): Target scores, can either be
            probability estimates of the positive class, confidence values, or
            non-thresholded measure of decisions (as returned by
            decision_function on some classifiers).
        pos_label (int or str, default=None): Label considered as positive and
            others are considered negative
    Returns:
        percentages (numpy.ndarray): An array containing the X-axis values for
            plotting the Cumulative Gains chart.
        gains (numpy.ndarray): An array containing the Y-axis values for one
            curve of the Cumulative Gains chart.
    Raises:
        ValueError: If `y_true` is not composed of 2 classes. The Cumulative
            Gain Chart is only relevant in binary classification.
    """
    y_true, y_score = np.asarray(y_true), np.asarray(y_score)

    # ensure binary classification if pos_label is not specified
    classes = np.unique(y_true)
    if (pos_label is None and
            not (np.array_equal(classes, [0, 1]) or
                 np.array_equal(classes, [-1, 1]) or
                 np.array_equal(classes, [0]) or
                 np.array_equal(classes, [-1]) or
                 np.array_equal(classes, [1]))):
        raise ValueError("Data is not binary and pos_label is not specified")
    elif pos_label is None:
        pos_label = 1.

    # make y_true a boolean vector
    y_true = (y_true == pos_label)

    sorted_indices = np.argsort(y_score)[::-1]
    y_true = y_true[sorted_indices]
    gains = np.cumsum(y_true)

    percentages = np.arange(start=1, stop=len(y_true) + 1)

    gains = gains / float(np.sum(y_true))
    percentages = percentages / float(len(y_true))

    gains = np.insert(gains, 0, [0])
    percentages = np.insert(percentages, 0, [0])

    return percentages, gains

def plot_cumulative_gain(y_true, y_probas, title='Lift Curve'):
    """Generates the Cumulative Gains Plot from labels and scores/probabilities
    The cumulative gains chart is used to determine the effectiveness of a
    binary classifier. A detailed explanation can be found at
    http://mlwiki.org/index.php/Cumulative_Gain_Chart. The implementation
    here works only for binary classification.
    Args:
        y_true (array-like, shape (n_samples)):
            Ground truth (correct) target values.
        y_probas (array-like, shape (n_samples, n_classes)):
            Prediction probabilities for each class returned by a classifier.
        title (string, optional): Title of the generated plot. Defaults to
            "Cumulative Gains Curve".

    """
    y_true = np.array(y_true)
    y_probas = np.array(y_probas)

    classes = np.unique(y_true)
    if len(classes) != 2:
        raise ValueError('Cannot calculate Cumulative Gains for data with '
                         '{} category/ies'.format(len(classes)))

    # Compute Cumulative Gain Curves
    percentages, gains1 = cumulative_gain_curve(y_true, y_probas)

    plt.title(title)

    plt.plot(percentages, gains1, lw=3, label='Model'.format(classes[0]))

    plt.plot([0, 1], [0, 1], 'k--', lw=2, label='Baseline')

    plt.legend(loc='lower right')

    plt.show()

def dwp_3months_ago(dwp):
    if dwp%100 > 3:
        return dwp-3
    else:
        return (dwp//100-1)*100 + 12 -3 + dwp%100


def compute_variable_unstacked(data, list_dwp, aggreg, timelag_n):

    to_merge = pd.DataFrame()
    for i in range(len(list_dwp)):
        filter_col = [col for col in data if (col <= list_dwp[i])]
        datatemp = data[filter_col]
        datatemp = datatemp[datatemp.columns[-timelag_n:]]
        datatemp.columns = map((aggreg + '_{}_MONTH_AGO').format, range(timelag_n, 0, -1))
        datatemp['DWP'] = list_dwp[i]
        datatemp.set_index('DWP', append=True, inplace=True)
        to_merge = pd.concat([to_merge, datatemp])

    return to_merge.reset_index()