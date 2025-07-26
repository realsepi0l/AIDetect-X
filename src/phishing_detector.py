# phishing_detector.py

import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from utils.text_cleaner import clean_text

def load_emails_from_csv(file_paths):
    all_texts = []
    all_labels = []

    for path in file_paths:
        if not os.path.exists(path):
            print(f"\u26a0 File not found: {path}")
            continue

        df = pd.read_csv(path)
        print(f"\n📄 {path} label distribution:")
        print(df['label'].value_counts())

        text_column = None

        # Auto-detect primary text column
        for candidate in ['text_combined', 'text', 'email_text', 'message', 'content']:
            if candidate in df.columns:
                text_column = candidate
                break

        # Handle subject + body format
        if not text_column and {'subject', 'body'}.issubset(df.columns):
            text_column = 'combined'
            df[text_column] = df['subject'].fillna('') + ' ' + df['body'].fillna('')
            if 'urls' in df.columns:
                df[text_column] += ' ' + df['urls'].fillna('').astype(str)

        if not text_column:
            raise ValueError(f"\u274c No usable text column found in {path}")

        print(f"✅ Using column: {text_column}")
        df['cleaned'] = df[text_column].apply(clean_text)

        all_texts.extend(df['cleaned'].tolist())
        all_labels.extend(df['label'].tolist())

    return all_texts, all_labels

def main():
    csv_files = [
        'data/emails/phishing_data.csv',
        'data/emails/nigeria_fraud.csv',
        'data/emails/phish.csv',
        'data/emails/SpamAssasin.csv',
        'data/emails/dataset_1.csv',
        'data/emails/dataset_2.csv',
        'data/emails/dataset_3.csv',
        'data/emails/dataset_4.csv'
    ]

    X, y = load_emails_from_csv(csv_files)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])

    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    print(f"\n✅ Model accuracy: {acc:.2f}")
    joblib.dump(model, 'models/phishing_model.pkl')
    print("\u2705 Model saved to models/phishing_model.pkl")

def scan_email(file_path):
    model = joblib.load('models/phishing_model.pkl')
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    cleaned = clean_text(text)
    prediction = model.predict([cleaned])[0]
    proba = model.predict_proba([cleaned])[0][1]
    return prediction == 1, proba

def detect_phishing(text):
    model = joblib.load('models/phishing_model.pkl')
    cleaned = clean_text(text)
    prediction = model.predict([cleaned])[0]
    proba = model.predict_proba([cleaned])[0][1] * 100  # percent
    return prediction == 1, proba

if __name__ == '__main__':
    main()

