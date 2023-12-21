from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import tensorflow as tf
from flask_cors import CORS  # Enable CORS for all routes
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load and preprocess data
wisata_place = pd.read_csv('./wisata_place_cleaned.csv')
wisata_place = wisata_place[wisata_place['City'] == 'Yogyakarta']

stopword_factory = StopWordRemoverFactory()
stopwords = stopword_factory.get_stop_words()

corpus = wisata_place['Description'].astype(str)
wisata_place['Description'] = corpus.apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stopwords]))

# TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords, max_df=0.8, ngram_range=(1, 2))
tfidf_matrix = tfidf_vectorizer.fit_transform(wisata_place['Description'])
terms = tfidf_vectorizer.get_feature_names_out()
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=terms)

# Load the pre-trained model
model = tf.keras.models.load_model('./TARA_MODEL.h5')

class ContentBasedFilteringModel:
    def preprocess_text(self, text, stopwords):
        if isinstance(text, str):
            cleaned_text = ' '.join([word for word in text.split() if word.lower() not in stopwords])
        elif isinstance(text, list):
            cleaned_text = ' '.join([word for word in ' '.join(text).split() if word.lower() not in stopwords])
        else:
            raise ValueError("Unsupported input type. Expected str or list.")

        return cleaned_text

    def get_user_preferences(self, user_input):
        user_preferences = f'{user_input}'
        return user_preferences

    def get_recommendations(self, user_preferences, tfidf_vectorizer, df_tfidf, item_data):
        user_preferences = self.preprocess_text(user_preferences, tfidf_vectorizer.get_stop_words())
        user_vector = tfidf_vectorizer.transform([user_preferences]).toarray()

        tfidf_similarities = cosine_similarity(user_vector, df_tfidf)
        tfidf_similar_items = tfidf_similarities.argsort()[0][::-1]
        # Get recommendations based on TF-IDF
        tfidf_recommendations = item_data.iloc[tfidf_similar_items[:15]]

        return tfidf_recommendations

# Instantiate the model
tf_model = ContentBasedFilteringModel()

# Flask API endpoint
@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    try:
        # Get user input from the request
        user_preferences= request.json.get('userPreferences')
        
        # Get recommendations
        recommendations = tf_model.get_recommendations(user_preferences, tfidf_vectorizer, tfidf_df, wisata_place)

        # Convert recommendations to JSON and return
        return jsonify(recommendations.to_dict(orient='records'))

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)


