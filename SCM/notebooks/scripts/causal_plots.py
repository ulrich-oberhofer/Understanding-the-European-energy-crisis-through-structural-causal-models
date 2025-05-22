# This file includes code adapted from the PyWhy project (https://github.com/py-why)
# Licensed under the MIT License:
# 
# MIT License

#     Copyright (c) PyWhy contributors. All rights reserved.

#     Permission is hereby granted, free of charge, to any person obtaining a copy
#     of this software and associated documentation files (the "Software"), to deal
#     in the Software without restriction, including without limitation the rights
#     to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#     copies of the Software, and to permit persons to whom the Software is
#     furnished to do so, subject to the following conditions:

#     The above copyright notice and this permission notice shall be included in all
#     copies or substantial portions of the Software.

#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#     SOFTWARE

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def plot_coefficients(df, col, ax, color):
    """
    Plot a bar chart of structural coefficients.

    Parameters:
    df (pandas.DataFrame): DataFrame containing the coefficients.
    col (str): The column name in the DataFrame to plot as the height of the bars.
    ax (matplotlib.axes.Axes): The matplotlib axes object on which to plot the bar chart.
    color (str): The color of the bars.

    Returns:
    None
    """
    ax.bar(x=df.index, height=df[col], color=color)
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
    _ = plt.setp(
        ax.xaxis.get_majorticklabels(), rotation=45, ha="right", rotation_mode="anchor"
    )


def plot_evaluation_results_custom(
    evaluation_result, ax, bins=None, savepath=None, display=True
):
    """
    Plot a custom flasification histogram.
    adapted from: from dowhy.gcm.falsify import plot_evaluation_results
    https://github.com/py-why/dowhy/blob/main/dowhy/gcm/falsify.py
    
    Parameters:
    evaluation_result (dowhy.gcm.falsify.FalsificationResult): The evaluation result to plot, containing the summary of falsification tests.
    ax (matplotlib.axes.Axes): The axes on which to plot the histogram.
    bins (int or sequence, optional): The number of bins or bin edges for the histogram. Defaults to None.
    savepath (str, optional): The file path to save the plot. If None, the plot is not saved. Defaults to None.
    display (bool, optional): Whether to display the plot using `plt.show()`. Defaults to True.

    Returns:
    tuple:
            A tuple containing:
            - labels (list of str): Descriptions of the violations for each falsification method.
            - p_values (str): A formatted string summarizing the p-values for each falsification method.
    """
    from dowhy.gcm.falsify import FalsifyConst, FALSIFY_METHODS

    COLORS = list(mcolors.TABLEAU_COLORS.values())

    # Plot histograms
    p_values = ""
    data = []
    labels = []

    evaluation_summary = {
        k: v for k, v in evaluation_result.summary.items() if k != FalsifyConst.MEC
    }
    for i, (m, m_summary) in enumerate(evaluation_summary.items()):
        data.append(m_summary[FalsifyConst.F_PERM_VIOLATIONS])
        labels.append(f"Violations of {FALSIFY_METHODS[m]} of permuted DAGs")
        p_values += (
            f"p-value {FALSIFY_METHODS[m]} = {m_summary[FalsifyConst.P_VALUE]:.2f}\n"
        )

    ax.hist(
        data,
        color=COLORS[: len(evaluation_summary)],
        bins=bins,
        alpha=0.5,
        label="",
        edgecolor="k",
    )

    # Plot given violations
    for i, (m, m_summary) in enumerate(evaluation_summary.items()):
        ylim = ax.get_ylim()[1]
        ax.plot(
            [m_summary[FalsifyConst.F_GIVEN_VIOLATIONS]] * 2,
            [0, ylim],
            "--",
            c=COLORS[i],
            label=f"Violations of {FALSIFY_METHODS[m]} of given DAG",
        )
        ax.set_ylim([0, ylim])

    ax.margins(0.05, 0)
    if savepath:
        plt.savefig(savepath, bbox_inches="tight")
    if display:
        plt.show()
    return labels, p_values
