import pandas as pd

"""
    It seems the file saved in a wrong way tho it reads normally in pandas,
    therefor I'm resaving it for better readability before re-annotation.
"""

original_file = '../../data/01_raw/coffeelove_data.tsv'
corrected_file = '../../data/01_raw/coffee_love_corrected.tsv'

df = pd.read_csv(original_file, sep='\t')
df.to_csv(corrected_file, index=False, sep='\t')