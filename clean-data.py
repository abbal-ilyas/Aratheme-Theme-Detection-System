import os
import re
import json
from tqdm import tqdm  # For progress indication

# Load stopwords from a file
try:
    with open('./stopwords-ar.txt', 'r', encoding='utf-8') as f:
        stopwords = set(f.read().splitlines())
except FileNotFoundError:
    print("Error: Stopwords file not found.")
    exit(1)

# Pre-compile regular expressions
space_re = re.compile(r'\s+')
non_arabic_re = re.compile(r'[^\u0621-\u064A ]')
kashida_re = re.compile(r'\u0640')

# Function to clean and normalize a paragraph
def nettoyer_paragraphe(paragraphe):
    paragraphe = space_re.sub(' ', paragraphe)  # Replace multiple spaces with a single space
    paragraphe = non_arabic_re.sub('', paragraphe)  # Keep only Arabic letters and spaces
    paragraphe = kashida_re.sub('', paragraphe)  # Remove kashida
    return paragraphe.strip()

# Process the dataset directory
dataset_dir = './dataset'
results = []  # To store all processed data

# Iterate over subdirectories (themes)
for theme_folder in tqdm(os.listdir(dataset_dir), desc="Processing themes"):
    theme_folder_path = os.path.join(dataset_dir, theme_folder)

    if os.path.isdir(theme_folder_path):  # Check if it's a directory
        for filename in os.listdir(theme_folder_path):
            if filename.endswith(".txt"):  # Check if it's a text file
                file_path = os.path.join(theme_folder_path, filename)

                try:
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except (FileNotFoundError, UnicodeDecodeError) as e:
                    print(f"Error reading file {file_path}: {e}")
                    continue

                # Split content into paragraphs by one or more newlines
                paragraphs = re.split(r'\n+', content)

                # Process each paragraph
                paragraph_vectors = []
                for para in paragraphs:
                    cleaned_para = nettoyer_paragraphe(para)  # Clean the paragraph
                    if cleaned_para and len(cleaned_para.split()) > 1:  # Only process non-empty paragraphs
                        words = [word for word in cleaned_para.split() if word not in stopwords]
                        paragraph_vectors.append(words)

                # Store results for this document only if there are non-empty paragraphs
                if paragraph_vectors:  # Only append if there are non-empty paragraph vectors
                    results.append({
                        "theme": theme_folder,
                        "filename": filename,
                        "paragraphs": paragraph_vectors
                    })

# Save results to a JSON file
output_file = './results3.json'
try:
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)
    print(f"Results saved to {output_file}")
except IOError as e:
    print(f"Error saving results to JSON: {e}")
