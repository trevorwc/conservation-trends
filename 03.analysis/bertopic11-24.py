from bertopic import BERTopic
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords

# Set up stop words
stop_words = stopwords.words("english")

# Configure vectorizer and load data
vectorizer_model = CountVectorizer(stop_words=stop_words, ngram_range=(1, 2))
cdf_subs = pd.read_json('/Users/trevor/Desktop/Subjects/1.125/project/conservation_filtered.json')

# Initialize embedding model and BERTopic
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
topic_model = BERTopic(embedding_model=embedding_model, vectorizer_model=vectorizer_model)

# Fit-transform and extract topics and probabilities
topics, probabilities = topic_model.fit_transform(cdf_subs['abstract'].tolist())

# Add topics and probabilities to the DataFrame
cdf_subs['topic'] = topics
cdf_subs['probability'] = probabilities

# Get topic information and merge with the DataFrame
topic_info = topic_model.get_topic_info()
topic_info.rename(columns={'Topic': 'topic'}, inplace=True)
cdf_subs = cdf_subs.merge(topic_info[['topic', 'Name']], on='topic', how='left')

# Generate embeddings for the abstracts and add them to the DataFrame
embeddings = embedding_model.encode(cdf_subs['abstract'].tolist(), show_progress_bar=True)
cdf_subs['embedding'] = embeddings.tolist()

# Save the DataFrame to a JSON file
cdf_subs.to_json('/Users/trevor/Desktop/Subjects/1.125/project/conservation_filtered_bertopic_with_embeddings.json', 
                 orient='records', 
                 indent=4)
