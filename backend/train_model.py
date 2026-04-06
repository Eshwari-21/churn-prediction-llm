import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Correct path
file_path = os.path.join("..", "data", "netflix_customer_churn.csv")

df = pd.read_csv(file_path)

print("Columns:", df.columns)

# Target column
target = "churned"

# Drop useless column
if "customer_id" in df.columns:
    df = df.drop(columns=["customer_id"])

# Features & target
X = df.drop(target, axis=1)
y = df[target]

# Convert categorical → numeric
X = pd.get_dummies(X)

# Save columns
os.makedirs("models", exist_ok=True)
pickle.dump(X.columns, open("models/columns.pkl", "wb"))

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model (NO SCALING)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Accuracy
print("Accuracy:", model.score(X_test, y_test))

# Save model
pickle.dump(model, open("models/churn_model.pkl", "wb"))

print("✅ Model trained successfully")