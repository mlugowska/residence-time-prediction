import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import seaborn as sns
from scipy.optimize import curve_fit
from scipy.stats import norm

from utils import externals
from utils.calculate_residence_time import compute_times

from utils.read_file import read_excel

pdbs = list(externals.VMD_PDB.keys())

pdbs_from_pub = ["2YKI", "5LO5", "5LO6", "5LQ9", "5LR1", "5LR7", "5LRZ", "5LS1", "5NYI", "5T21", "6EI5", "6EL5", "6ELN",
                 "6ELO", "6ELP", "6EY8", "6EY9", "6F1N", '2X22', '2X23', '3EKX']


# linear regression - zależność liniowa (korelacja liniowa)
def create_xy(df: pd.DataFrame, y_column_name: str):
    x = df['Residence Time [s]'].to_numpy()
    y = df[y_column_name].to_numpy()
    return x, y


def linear_regression_model(X, y):
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=33)

    # apply linear regression on dataset
    lm = LinearRegression()
    lm.fit(X_train, y_train)
    pred = lm.predict(y)

    fig, ax = plt.subplots(10, 6)
    # plotting the data points
    sns.scatterplot(x=np.reshape(X, -1), y=np.reshape(y, -1))
    # plotting the line
    sns.lineplot(x=np.sort(np.reshape(X, -1)), y=np.sort(np.reshape(pred, -1)), color='red')
    # axes
    plt.xscale('log', base=10)
    plt.yscale('log', base=10)
    add_labels(X, y, ax, pdbs)


def objective(x, a, b):
    return a * x + b


def fit_linear_curve_to_data(X, y):
    from numpy import arange

    # curve fit
    popt, _ = curve_fit(objective, X, y)
    # summarize the parameter values
    a, b = popt
    print(f'y = {a:.5f} * x + {b:5f}')
    # plot input vs output
    plt.scatter(X, y)
    # define a sequence of inputs between the smallest and largest known inputs
    x_line = arange(min(X), max(X), 1)
    # calculate the output for the range
    y_line = objective(x_line, a, b)

    fig, ax = plt.subplots(10, 6)

    # create a line plot for the mapping function
    plt.plot(x_line, y_line, '--', color='red')

    plt.xscale('log', base=10)
    plt.yscale('log', base=10)

    plt.ylabel('computed tau (ns)')
    plt.xlabel('experimental tau (s)')
    add_labels(X, y, ax, pdbs)


def add_labels(X, y, ax, pdb):
    for x_pos, y_pos, label in zip(X, y, pdb):
        ax.annotate(label,  # The label for this point
                    xy=(x_pos, y_pos),  # Position of the corresponding point
                    xytext=(7, 0),  # Offset text by 7 points to the right
                    textcoords='offset points',  # tell it to use offset points
                    ha='left',  # Horizontally aligned to the left
                    va='center')  # Vertical alignment is centered


# correlation
def linear_regression_plus_correlation(X, y):
    r = np.corrcoef(X, y)

    slope, intercept, r, p, stderr = scipy.stats.linregress(X, y)
    line = f'Regression line: y={intercept:.5f}+{slope:.7f}x, r={r:.5f}'
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(X, y, linewidth=0, marker='o', label='Data points')
    X_log = np.asarray(list(map(math.log10, X)))
    ax.plot(np.sort(X), np.sort(intercept + slope * X_log), label=line)
    plt.xscale('log', base=10)
    plt.yscale('log', base=10)
    ax.legend(facecolor='white')
    plt.ylabel('computed tau (ns)')
    plt.xlabel('experimental tau (s)')
    # add_labels(X, y, ax, pdbs)


# df = read_excel(sheet_name='data')
# df = df.dropna(subset=['comp time'])
# df_with_tau = compute_times(pdb_list=pdbs, df=df)
# df_tau_without_nan = df_with_tau.dropna(subset=['Relative Residence Time [ns]'])
# X, y = create_xy(df_tau_without_nan, 'Relative Residence Time [ns]')
# linear_regression_plus_correlation(X, y)

# df_tau_without_nan = df_with_tau.dropna(subset=['Relative Residence Time [ns]'])
# # sns.factorplot(data=df_tau_without_nan, y='comp time', x='Residence Time', row='Protein Name', kind='swarm')
# # plt.show()
# # plt.clf()

# # może coś z tego będzie?
# sns.residplot(data=df_tau_without_nan, y='comp time', x='Residence Time', lowess=True)
# plt.show()

# sns.lmplot(data=df_tau_without_nan, y='comp time', x='Residence Time')
# plt.show()

