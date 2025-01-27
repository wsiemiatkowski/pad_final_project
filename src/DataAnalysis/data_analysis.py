import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency


def load_data(filepath):
    return pd.read_csv(filepath, sep="\t")


def cross_tabulation(data, col1, col2):
    cross_tab = pd.crosstab(data[col1], data[col2])

    return cross_tab


def chi_square_test(cross_tab):
    chi2, p, dof, expected = chi2_contingency(cross_tab)

    return {"chi2": chi2, "p_value": p, "degrees_of_freedom": dof, "expected": expected}


def most_common_varieties(data):
    return data.groupby("origin")["variety"].value_counts().unstack().fillna(0)


def yield_analysis(data):
    return data.groupby(["variety", "Yield Potential"]).size().unstack().fillna(0)


def plot_yield_analysis(yield_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    yield_data.plot(kind="bar", stacked=True, ax=ax)
    ax.set_title("Yield Potential by Coffee Variety")
    ax.set_ylabel("Count")
    ax.set_xlabel("Coffee Variety")
    plt.tight_layout()
    return fig


def plot_variety_by_origin(data):
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.countplot(
        data=data,
        x="origin",
        order=data["origin"].value_counts().index,
        hue="variety",
        ax=ax,
    )

    ax.set_title("Coffee Varieties by Origin")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    ax.legend(
        title="Variety",
        bbox_to_anchor=(
            1.05,
            1,
        ),
        loc="upper left",
    )
    plt.tight_layout()

    return fig


def plot_correlation_heatmap(data):
    encoded_data = pd.get_dummies(data, drop_first=True)
    correlation = encoded_data.corr()

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(correlation, annot=False, cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap")
    plt.tight_layout()

    return fig
