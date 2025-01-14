import json
import datetime
from joblib import dump
import numpy as np
from keras import Sequential
from keras.src.callbacks import EarlyStopping
from keras.src.layers import Dense, Dropout
from keras.src.metrics import Precision, Recall
from keras.src.utils import to_categorical
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight

# Load the JSON data
try:
    with open('./results_lemmatized.json', encoding='utf-8') as f:
        lemmatized_results = json.load(f)
except FileNotFoundError:
    print("Error: The file 'results_lemmatized.json' was not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error: The file 'results_lemmatized.json' is not properly formatted JSON.")
    exit(1)

# Initialize lists for documents and their labels
documents = []
labels = []
for document in lemmatized_results:
    # Check that the document has valid 'paragraphs' and 'theme'
    if 'paragraphs' in document and 'theme' in document and document['paragraphs']:
        text = ' '.join([' '.join(paragraph) for paragraph in document['paragraphs']])
        documents.append(text)
        labels.append(document['theme'])
    else:
        print(f"Warning: A document is missing 'paragraphs' or 'theme': {document}")

# Check that we have at least two classes
if len(set(labels)) < 2:
    print("Error: The dataset must contain at least two classes.")
    exit(1)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=5000)  # Add stop_words parameter if needed for Arabic
X = vectorizer.fit_transform(documents).toarray()

# Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)  # Transform to numeric labels
y_one_hot = to_categorical(y)  # Convert to one-hot encoding

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_one_hot, test_size=0.2, random_state=42)

# Compute class weights
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y),
    y=y
)
class_weights_dict = {i: class_weights[i] for i in range(len(class_weights))}

# Model Initialization
model = Sequential()
# Input Layer
model.add(Dense(128, activation='relu', input_dim=X.shape[1]))
# Hidden Layers
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.3))
# Output Layer
num_classes = len(set(labels))
model.add(Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy', Precision(name='precision'), Recall(name='recall')]
)

# Early Stopping Callback
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Train the model
model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=50,
    batch_size=32,
    class_weight=class_weights_dict,
    callbacks=[early_stopping]
)

# Evaluate the model
loss, accuracy, precision, recall = model.evaluate(X_test, y_test)
print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"Loss: {loss}")

# Classification Report
y_pred = model.predict(X_test).argmax(axis=1)
y_true = y_test.argmax(axis=1)
print(classification_report(y_true, y_pred, target_names=label_encoder.classes_))
print(confusion_matrix(y_true, y_pred))


# Add a timestamp to the filename
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
model.save(f"model_{timestamp}.h5")
dump(vectorizer, 'vectorizer.joblib')
dump(label_encoder, 'label_encoder.joblib')
