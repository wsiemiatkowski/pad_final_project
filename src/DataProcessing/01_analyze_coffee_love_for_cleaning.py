import pandas as pd


def get_unique_values(df, column):
    unique_values = df[column].unique().tolist()
    return unique_values


def get_value_counts(df, column):
    value_counts = df[column].value_counts()
    return value_counts


if __name__ == "__main__":
    #coffee_love_file = '../../data/01_raw/coffee_love_corrected.tsv'
    coffee_love_file = '../../data/02_intermediate/coffee_love_corrected.tsv'
    coffee_love_df = pd.read_csv(coffee_love_file, sep='\t')

    for cf_column in coffee_love_df.columns:
        print(f"{cf_column}:")
        print(get_unique_values(coffee_love_df, cf_column))
        print(get_value_counts(coffee_love_df, cf_column))
        print('\n')

