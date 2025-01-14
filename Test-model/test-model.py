from keras.models import load_model
from joblib import load
import re
import numpy as np
import requests

# Load the saved model (replace 'model.h5' with the correct path if needed)
model = load_model('../theme-detection-model/model_20241221-154919.h5')

# Load the saved vectorizer
vectorizer = load('../theme-detection-model/vectorizer(1).joblib')

# Load the saved label encoder (make sure it's saved separately during training)
label_encoder = load('../theme-detection-model/label_encoder.joblib')  # You must save this encoder when training

# Load the content of the document
with open('./document.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Load stopwords from a file
with open('./stopwords-ar.txt', 'r', encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())

# Split the content into paragraphs based on a regex
paragraphs = re.split(r'\.?\s*\n+', content)

# Function to clean up each paragraph
def nettoyer_paragraphe(paragraphe):
    paragraphe = re.sub(r'\s+', ' ', paragraphe)  # Replace multiple spaces with a single space
    paragraphe = re.sub(r'[^\u0621-\u064A ]', '', paragraphe)  # Keep only Arabic letters and spaces
    paragraphe = re.sub(r'\u0640', '', paragraphe)  # Remove Kashida (Arabic elongation mark)
    return paragraphe.strip()

# Function to lemmatize words using the API
def lemmatize_word(word):
    # Example API URL: Replace this with the correct URL for your lemmatization API
    api_url = "http://localhost:8084/api/lemma"
    payload = {"word": word}
    
    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json().get('lemma', word)  # Get the lemma from the API response
        else:
            print(f"Error lemmatizing word: {word}")
            return word  # Return the original word if API fails
    except Exception as e:
        print(f"API error: {e}")
        return word  # Return the original word in case of an error

# Apply cleaning and lemmatization to each paragraph and filter out stopwords
cleaned_paragraphs = [
    ' '.join([lemmatize_word(word) for word in nettoyer_paragraphe(para).split() if word not in stopwords])
    for para in paragraphs if para.strip()
]

# Join all paragraphs into a single string to be vectorized
document = ' '.join(cleaned_paragraphs)

# Vectorize the new document using the loaded vectorizer
X_test = vectorizer.transform([document]).toarray()

# Predict the theme for the new Arabic document
predicted_probabilities = model.predict(X_test)

# Get the predicted class (index of the highest probability)
predicted_class = np.argmax(predicted_probabilities, axis=1)

# Get the theme name using the inverse transformation of the label encoder
predicted_theme = label_encoder.inverse_transform(predicted_class)

# Print the predicted theme
print(f"The predicted theme is: {predicted_theme[0]}")
