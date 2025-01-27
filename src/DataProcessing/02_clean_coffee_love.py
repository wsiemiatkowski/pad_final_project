import pandas as pd

from src.DataProcessing.utils.processing_vars import (
    IRRELEVANT_WORDS_IN_ORIGIN,
    VARIETY_MAPPING,
    COLORS,
)


def get_df_without_empty_or_irrelevant_rows(file, irrelevant_words):
    """
    Return only those rows that are not empty or do not contain any irrelevant words.
    Irrelevant rows decided upon the interpretation of the results of `01_analyze_coffee_love_for_cleaning.py`.
    Column region has been dropped. During the inspection of the dataframe I deemd it too unstable.
    """
    df = pd.read_csv(file, sep="\t")
    df = df.drop(columns=["region"])
    df = df[df["origin"].notna()]
    df = df[df["origin"] != ""]

    mask = ~df["origin"].str.lower().isin(word.lower() for word in irrelevant_words)

    df = df[mask]
    df = df.reset_index(drop=True)

    return df


def clean_long_titles(row, origins):
    """
    For some reason some of the entries have the whole title instead of origin inside the origin column.
    To fix this let's extract the origin from the title.
    """

    origin = row["origin"]

    if len(origin.split()) > 1:
        real_origin = [word for word in origins if word in origins][0]
        row["origin"] = real_origin

    return row


def clean_variety_wrongly_merged(df):
    """
    Some of the rows have merged different varieties into one string.
    """

    df.loc[
        df["variety"].str.contains("TypicaCaturraCastillo", case=False, na=False),
        "variety",
    ] = "Typica, Caturra, Castillo"
    df.loc[
        df["variety"].str.contains("BourbonCaturraTypica", case=False, na=False),
        "variety",
    ] = "Bourbon, Caturra, Typica"
    df.loc[
        df["variety"].str.contains("Bourbon Mundo Nuovo Robusta", case=False, na=False),
        "variety",
    ] = "Bourbon, Mundo Nuovo, Robusta"
    df.loc[
        df["variety"].str.contains("Sl28Sl34Ruiru 11", case=False, na=False), "variety"
    ] = "Sl28, Sl34, Ruiru 11"

    return df


def clean_wrong_add_ons(df):
    """
    Some varieties have add-ons that are useless for our use case.
    """
    df.loc[df["variety"].str.contains("catuai", case=False, na=False), "variety"] = (
        "Catuai"
    )
    df["variety"] = df["variety"].str.replace(r"\(.*?\)", "", regex=True).str.strip()

    return df


def clean_wrongly_annotated_kenya(df):
    """
    Some Kenyan coffees are annotated as a mix, not the exact varieties. Let's change that.
    """
    df.loc[df["variety"] == "mixed Kenyan cultivars", "variety"] = (
        "Sl28, Sl34, Ruiru 11, Batian"
    )

    return df


def clean_ethiopia(df):
    """
    All Ethiopians are some kind of mix of heirloom varities, but they are annotated in different ways.
    Let's unify that.
    """
    df.loc[df["origin"] == "Etiopia", "variety"] = "Heirloom"

    return df


def split_multiple_varieties(df):
    """
    We need data about specific varieties so if we have a mix of varieties then it's better to split them into
    new rows. After all they are all varieties grown in a specific region.
    """

    df_expanded = (
        df.assign(variety=df["variety"].str.split(r"\s*[,&]\s*"))
        .explode("variety")
        .reset_index(drop=True)
    )

    return df_expanded


def merge_rare_classes(df, threshold):
    """
    During the examination of the dataset some countries have been noted to be very rare in the dataset.
    To address this issue I will be combining them into other category.
    This way they can have some meaning for the model, and they won't have to be erased.
    """

    country_counts = df["origin"].value_counts()
    df["origin"] = df["origin"].where(
        df["origin"].map(country_counts) >= threshold, "Other"
    )

    return df


def clean_color_information(value):
    """
    Delete color information.
    """

    if isinstance(value, str):
        parts = value.split(" ")
        if parts[0].lower() in COLORS:
            return parts[1] if len(parts) > 1 else ""
        else:
            return value
    else:
        return value


def map_varieties_for_proper_merge(df, mapping_solution):
    """
    Not all varieties are included in `data/01_raw/varieties.tsv`, some have extra information,
    some simply are not cover by that database. We need to map them for further processing.
    For varieties with no clear connection we will be using different filling methods.
    To be continued in 0`4_mege_files.py`.
    """

    df["variety"] = df["variety"].apply(
        lambda x: mapping_solution[x] if x in mapping_solution else x
    )

    return df


def fill_in_empty_varieties(group):
    """
    Some of the rows do not contain any varieties.
    We will fill those in using the most common varieties for said country.
    """

    mode = group["variety"].mode()

    if not mode.empty:
        group["variety"] = group["variety"].fillna(mode[0])
    return group


if __name__ == "__main__":
    original_file = "../../data/01_raw/coffee_love_corrected.tsv"
    output_file = "../../data/02_intermediate/coffee_love_corrected.tsv"

    coffee_love_df = get_df_without_empty_or_irrelevant_rows(
        original_file, IRRELEVANT_WORDS_IN_ORIGIN
    )
    coffee_love_origins = coffee_love_df["origin"].unique().tolist()
    coffee_love_df = coffee_love_df.apply(
        clean_long_titles, axis=1, origins=coffee_love_origins
    )
    coffee_love_df = clean_wrongly_annotated_kenya(coffee_love_df)
    coffee_love_df = clean_ethiopia(coffee_love_df)
    coffee_love_df = clean_variety_wrongly_merged(coffee_love_df)
    coffee_love_df = split_multiple_varieties(coffee_love_df)
    coffee_love_df = clean_wrong_add_ons(coffee_love_df)
    coffee_love_df = merge_rare_classes(coffee_love_df, threshold=10)
    coffee_love_df["variety"] = coffee_love_df["variety"].apply(clean_color_information)
    coffee_love_df = map_varieties_for_proper_merge(coffee_love_df, VARIETY_MAPPING)
    coffee_love_df["variety"] = coffee_love_df["variety"].replace("", pd.NA)
    coffee_love_df = coffee_love_df.groupby("origin").apply(fill_in_empty_varieties)
    coffee_love_df.to_csv(output_file, sep="\t", index=False)
