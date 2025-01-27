import pandas as pd


def drop_irrelevant_columns(df, columns):
    for column in columns:
        df = df.drop(column, axis=1)

    return df


def add_heirloom(df):
    """
    Heirloom is a group of varieties grown around the world originating from Ethiopia. Without genetic tests
    it's impossible to difference them. Let's add Heirloom for easier processing of Ethiopia, since most Ethiopian
    beans are just assumed as heirloom.
    """
    df.loc[len(df)] = [
        "Heirloom",
        "high",
        "Good",
        "Medium, High",
        "Tolerant",
        "Tolerant",
        "Tolerant",
    ]
    return df


def delete_parentheses(df):
    """
    Clean excess data from variety names
    """
    df["name"] = df["name"].str.replace(r"\(.*?\)", "", regex=True).str.strip()

    return df


def rename_name_to_varieties(df):
    """
    Let's make sure the column has the same name in both tsv files.
    """
    df = df.rename(columns={"name": "variety"})
    return df


if __name__ == "__main__":
    original_file = "../../data/01_raw/varieties.tsv"
    output_file = "../../data/02_intermediate/cleaned_varieties.tsv"

    varieties_df = pd.read_csv(original_file, sep="\t")
    varieties_df = drop_irrelevant_columns(
        varieties_df, ["url", "description", "Stature", "Leaf tip color", "Bean Size"]
    )
    varieties_df = add_heirloom(varieties_df)
    varieties_df = delete_parentheses(varieties_df)
    varieties_df = rename_name_to_varieties(varieties_df)
    varieties_df.to_csv(output_file, sep="\t", index=False)
