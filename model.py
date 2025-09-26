import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("F:/SIH demo streamlit/Crop_recommendation.csv")

# Features and target
X = df[['N','P','K','temperature','humidity','ph']]
y = df['label']  # Crop type

# Encode target labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save model and label encoder
joblib.dump(clf, "crop_model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("Model trained and saved successfully!")
