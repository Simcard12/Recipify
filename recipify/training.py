import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

def train_model(data_path, model_path, vectorizer_path):
    """
    Trains a machine learning model to classify receipts and saves it.

    Args:
        data_path (str): Path to the CSV dataset.
        model_path (str): Path to save the trained model.
        vectorizer_path (str): Path to save the vectorizer.
    """
    # Load the dataset
    data = pd.read_csv(data_path)

    # Extract features and labels
    X = data['receipt_text']
    y = data['label']

    # Convert text to numeric features using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X_transformed = vectorizer.fit_transform(X)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.3, random_state=42)

    # Train a logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Save the model and vectorizer
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    print(f"Model saved to {model_path}")
    print(f"Vectorizer saved to {vectorizer_path}")
