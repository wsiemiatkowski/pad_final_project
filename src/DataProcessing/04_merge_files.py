import pandas as pd


varieties_file = "../../data/02_intermediate/cleaned_varieties.tsv"
coffee_love_file = "../../data/02_intermediate/coffee_love_corrected.tsv"
output_file = "../../data/03_final/merged_files.tsv"

coffee_love_df = pd.read_csv(coffee_love_file, sep="\t")
varieties_df = pd.read_csv(varieties_file, sep="\t")

coffee_love_df["variety"] = coffee_love_df["variety"].str.lower()
varieties_df["variety"] = varieties_df["variety"].str.lower()

merged_df = pd.merge(coffee_love_df, varieties_df, on="variety", how="inner")
merged_df.to_csv(output_file, sep="\t", index=False)

empty_rows = merged_df.isnull().all(axis=1)

if empty_rows.any():
    print(f"There are still rows to be worked on! The sum is: {len(empty_rows)}")
else:
    print(f"There are no rows to be worked on!")
