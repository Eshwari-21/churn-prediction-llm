import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("../data/netflix_customer_churn.csv")

# Drop ID
df = df.drop("customer_id", axis=1)

# Target
y = df["churned"]
X = df.drop("churned", axis=1)

# Encode categorical
X = pd.get_dummies(X)

# Save columns
joblib.dump(X.columns, "../models/columns.pkl")

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, "../models/scaler.pkl")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "../models/churn_model.pkl")

print("✅ Model trained and saved!")