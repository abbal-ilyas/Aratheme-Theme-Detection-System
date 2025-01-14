import json
import re

import requests

# Load the JSON file with processed paragraphs
input_file = './results.json'  # Path to the input JSON file (the one you just created)
output_file = './results_lemmatized.json'  # Path to save the new lemmatized JSON file


def remove_arabic_diacritics(word):
    # Regular expression to match Arabic diacritical marks (harakat, sukūn, etc.)
    diacritics = r'[\u064B-\u0652]'
    # Remove diacritical marks
    return re.sub(diacritics, '', word)


def lemmatizer_api(word):
    url = 'http://localhost:8084/api/lemma'
    payload = {'textinput': word}

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            result = response.text
            # Ensure the returned word is clean of diacritics as well
            return remove_arabic_diacritics(result.strip())  # Return the lemmatized word without diacritics
        else:
            print(f"Error during lemmatization for word '{word}': {response.status_code}")
            return word  # If the API fails, return the original word without diacritics
    except Exception as e:
        print(f"Error during API request: {e}")
        return word


# Read the input JSON file
try:
    with open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
except IOError as e:
    print(f"Error reading input JSON file: {e}")
    exit(1)

# Process each document and lemmatize words
lemmatized_results = []
for document in data:
    lemmatized_paragraphs = []
    for paragraph in document['paragraphs']:
        lemmatized_paragraph = []
        for word in paragraph:
            lemmatized_word = lemmatizer_api(word)  # Lemmatize each word
            lemmatized_paragraph.append(lemmatized_word)  # Add lemmatized word to paragraph

        lemmatized_paragraphs.append(lemmatized_paragraph)

    # Append the processed document with lemmatized words
    lemmatized_results.append({
        "theme": document['theme'],
        "filename": document['filename'],
        "paragraphs": lemmatized_paragraphs
    })

# Save the lemmatized results to a new JSON file
try:
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(lemmatized_results, json_file, ensure_ascii=False, indent=4)
    print(f"Lemmatized results saved to {output_file}")
except IOError as e:
    print(f"Error saving lemmatized results to JSON: {e}")
