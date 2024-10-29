import pandas as pd
import json

cons_df = pd.read_json('conservation_articles.json')
print(cons_df.head)
print(cons_df.columns)


def extract_year(published_online):
    try:
        # Extract the year from the first element of 'date-parts'
        return published_online['date-parts'][0][0]
    except (KeyError, IndexError, TypeError):
        # Return None if the structure is unexpected
        return None
    
def extract_month(published_online):
    try:
        # Extract the month from the first element of 'date-parts'
        return published_online['date-parts'][0][1]
    except (KeyError, IndexError, TypeError):
        # Return None if the structure is unexpected
        return None    

def extract_day(published_online):
    try:
        # Extract the day from the first element of 'date-parts'
        return published_online['date-parts'][0][2]
    except (KeyError, IndexError, TypeError):
        # Return None if the structure is unexpected
        return None   

cons_df['year'] = cons_df['published-online'].apply(extract_year)

cons_df['month'] = cons_df['published-online'].apply(extract_month)

cons_df['day'] = cons_df['published-online'].apply(extract_day)

subset_df = cons_df[cons_df["abstract"].notnull() & cons_df["year"].notnull()]

print(subset_df["month"], subset_df["published-online"])

subset_df.to_json('conservation_full.json', orient='records', indent=4)
# 81958 conservation articles since 2013