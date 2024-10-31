from bertopic import BERTopic
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
#import nltk
#nltk.download("stopwords")
from nltk.corpus import stopwords

stop_words = stopwords.words("english")

vectorizer_model = CountVectorizer(stop_words=stop_words, ngram_range=(1, 2))

cdf_subs = pd.read_json('/workspaces/conservation-trends/conservation_filtered.json')


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
topic_model = BERTopic(embedding_model=embedding_model, vectorizer_model=vectorizer_model)

topics, probabilities = topic_model.fit_transform(cdf_subs['abstract'].tolist())
cdf_subs['topic'] = topics
cdf_subs['probability'] = probabilities

topic_info = topic_model.get_topic_info()
topic_info.rename(columns={'Topic': 'topic'}, inplace=True)
cdf_subs = cdf_subs.merge(topic_info[['topic', 'Name']], on='topic', how='left')

#print(topic_info)

#print(topic_info.to_string())

# can probably just remove based on topic later?
cdf_subs.to_json('/workspaces/conservation-trends/cdf_topics.json', orient='records', indent=4)