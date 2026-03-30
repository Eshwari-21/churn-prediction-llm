import joblib

model = joblib.load("../models/churn_model.pkl")
scaler = joblib.load("../models/scaler.pkl")
columns = joblib.load("../models/columns.pkl")