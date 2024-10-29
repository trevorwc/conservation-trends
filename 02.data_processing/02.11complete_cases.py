import pandas as pd
import json

cons_df = pd.read_json('conservation_articles.json')
print(cons_df.head)
print(cons_df.columns)

subset_df = cons_df[cons_df["abstract"].notnull() & cons_df["published-online"].notnull()]

print(subset_df.head)

subset_df.to_json('conservation_full.json', orient='records', indent=4)