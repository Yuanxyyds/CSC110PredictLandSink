"""
Instructions (READ THIS FIRST!)
===============================
Read the comments and comment/uncomment specific lines to choose
what part of the program intended to run.

Copyright and Usage Information
===============================

This program is provided solely for the personal and private use of teachers and TAs
checking and grading the CSC110 project at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Alex Lin, Steven Liu, Haitao Zeng, William Zhang.
"""
from typing import Tuple

import pandas as pd
import matplotlib.pyplot as plt
from numpy import mean

intercept = 0
slope = 0
intercept2 = 0
slope2 = 0
lens = 0
lens2 = 0
# Create Data Frame
df1 = pd.DataFrame(pd.read_csv('temperature.csv'))
df2 = pd.DataFrame(pd.read_csv('sealevel.csv'))


def linear_regression_model(x, y) -> Tuple[float, float, int]:
    """
    Calculate the best-fit linear line between independent variable x and
    dependent variable y (in form of: Best-fit line = a + Bx). Return a list
    contains the y-intercept a and slope B and length of data lens in [a, B, lens]
    """
    length = len(x)
    x_mean = mean(x)
    y_mean = mean(y)
    x_sum = sum(x)
    xy_sum = sum([x[i] * y[i] for i in range(0, length)])
    x_square_sum = sum([x[i] ** 2 for i in range(0, length)])
    x_slope = (xy_sum - y_mean * x_sum) / (x_square_sum - x_mean * x_sum)
    y_intercept = y_mean - x_slope * x_mean
    return (y_intercept, x_slope, length)


def build_models() -> None:
    """
    To draw a graph.
    """
    global intercept, slope, intercept2, slope2, lens, lens2, df1, df2

    intercept, slope, lens = linear_regression_model(df1.Year, df1.Tem)
    # Predict tem of current year
    df2.year = [year_to_tem(line) for line in df2.year]
    # Turn millimeter into meter
    df2.GMSL = [line / 1000 for line in df2.GMSL]
    intercept2, slope2, lens2 = linear_regression_model(df2.year, df2.GMSL)


def plot() -> None:
    """Plot the models"""
    ploting(200, df1.Year, df1.Tem, lens, intercept, slope,
            'Temperature (C) vs. Time Period', 'Time Period',
            'Temperature (C)')
    ploting(300, df2.year, df2.GMSL, lens2, intercept2, slope2,
            'Rise of sea level (m) vs. Temperature(C)',
            'Temperature(C)',
            'Rise of sea level (m)')


def ploting(seed: int, x, y, data_length: int, y_intercept: float, rate: float,
            title: str, x_lable: str, y_lable: str) -> None:
    """Modify the plot"""
    plt.figure(seed)
    plt.scatter(x, y)

    plt.plot([x[0], x[data_length - 1]],
             [x[0] * rate + y_intercept,
              x[data_length - 1] * rate + y_intercept], color='red')

    plt.title(title)
    plt.suptitle(f'Linear Regression Model: Y = {round(y_intercept, 5)} + {round(rate, 5)} * X')
    plt.xlabel(x_lable)
    plt.ylabel(y_lable)
    plt.show()


def year_to_tem(year: float) -> float:
    """Return the rise in Temperature in given year
    """
    return intercept + slope * year


def tem_to_sealevel(tem: float) -> float:
    """Return the rise in Temperature in given year
    """
    return intercept2 + slope2 * tem


if __name__ == '__main__':
    build_models()
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'random'],
        'max-line-length': 100,
        'disable': ['R1705', 'E9999', 'R0902']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
