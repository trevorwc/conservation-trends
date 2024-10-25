# Extract relevant information through Crossref API
# https://habanero.readthedocs.io/en/latest/modules/crossref.html

# === Imports =======
from habanero import Crossref
import json

# === Helper Functions =======
cr = Crossref()

# Get all articles from GCB
res = cr.works(cursor = "*", 
               limit = 100, 
               cursor_max=100000,
               filter = {'type': 'journal-article', 'from-pub-date': "2013", 'issn': '1365-2486'},
               select=[ "title", "abstract", "author", "container-title","DOI", "published-online"],
               progress_bar=True
               )

print(sum([ len(z['message']['items']) for z in res ]))
items = [ z['message']['items'] for z in res ]
items = [ item for sublist in items for item in sublist ]
ecology_prompt = [item for batch in res for item in batch['message']['items']]

with open('gcb_articles.json', 'w') as f:
    json.dump(ecology_prompt, f, indent=4)
"""
"""
# Get all articles related to conservation 
res = cr.works(query = "conservation",
                cursor = "*", 
               limit = 100, 
               cursor_max=1000000,
               filter = {'type': 'journal-article', 'from-pub-date': "2013"},
               select=[ "title", "abstract", "author", "container-title","DOI", "published-online"],
               progress_bar=True
               )

print(sum([ len(z['message']['items']) for z in res ]))
items = [ z['message']['items'] for z in res ]
items = [ item for sublist in items for item in sublist ]
cons_prompt = [item for batch in res for item in batch['message']['items']]

with open('conservation_articles.json', 'w') as f:
    json.dump(cons_prompt, f, indent=4)

# Get all articles related to ecology 
res = cr.works(query = "ecology",
                cursor = "*", 
               limit = 100, 
               cursor_max=1000000,
               filter = {'type': 'journal-article', 'from-pub-date': "2013"},
               select=[ "title", "abstract", "author", "container-title","DOI", "published-online"],
               progress_bar=True
               )

print(sum([ len(z['message']['items']) for z in res ]))
items = [ z['message']['items'] for z in res ]
items = [ item for sublist in items for item in sublist ]
cons_prompt = [item for batch in res for item in batch['message']['items']]

with open('conservation_articles.json', 'w') as f:
    json.dump(cons_prompt, f, indent=4)
