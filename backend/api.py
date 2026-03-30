from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from feature_engineering import preprocess
from gemini_engine import generate_strategy
from impact_engine import estimate_effect

app = Flask(__name__)
CORS(app)

model = joblib.load("../models/churn_model.pkl")

# Risk calculation
def get_risk(prob):
    if prob > 0.75:
        return "High"
    elif prob > 0.45:
        return "Medium"
    return "Low"

# Feature explanation
def explain_features(data):
    explanation = []

    if data["last_login_days"] > 30:
        explanation.append("User inactive for long time")

    if data["watch_hours"] < 5:
        explanation.append("Low engagement")

    if data["avg_watch_time_per_day"] < 2:
        explanation.append("Low daily usage")

    if data["monthly_fee"] > 500:
        explanation.append("High subscription cost")

    if data["number_of_profiles"] == 1:
        explanation.append("Single user account (less retention)")

    return explanation

@app.route("/")
def home():
    return "Backend running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    processed = preprocess(data)
    prob = model.predict_proba([processed])[0][1]

    risk = get_risk(prob)

    result = {
        "churn_probability": round(prob, 3),
        "risk": risk,
        "feature_reasons": explain_features(data)
    }

    if prob > 0.45:
        result["strategy"] = generate_strategy(data, prob, risk)
        result["after_strategy"] = estimate_effect(data, prob)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)