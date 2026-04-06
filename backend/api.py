from flask import Flask, request, jsonify
import pandas as pd
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model
model = pickle.load(open("models/churn_model.pkl", "rb"))
columns = pickle.load(open("models/columns.pkl", "rb"))

# Risk logic
def get_risk(prob):
    if prob > 0.7:
        return "High"
    elif prob > 0.4:
        return "Medium"
    return "Low"

# Drivers logic
def get_drivers(data):
    drivers = []
    if data.get("last_login_days", 0) > 30:
        drivers.append("User inactive")
    if data.get("watch_hours", 0) < 5:
        drivers.append("Low engagement")
    if data.get("monthly_fee", 0) > 800:
        drivers.append("High cost")
    return drivers

# Dummy LLM (safe version to avoid quota issues)
def generate_strategy(prob, risk):
    if risk == "High":
        return ["Give discount", "Send re-engagement emails"]
    elif risk == "Medium":
        return ["Offer recommendations", "Push notifications"]
    else:
        return ["Customer safe — no action needed"]

# SINGLE PREDICT
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    df = pd.DataFrame([data])
    df = pd.get_dummies(df)
    df = df.reindex(columns=columns, fill_value=0)

    prob = model.predict_proba(df)[0][1]

    risk = get_risk(prob)
    drivers = get_drivers(data)
    strategy = generate_strategy(prob, risk)

    improved_prob = prob * 0.7
    impact = f"Churn reduced by {(prob - improved_prob)*100:.1f}%"

    return jsonify({
        "probability": float(prob),
        "risk": risk,
        "drivers": drivers,
        "strategy": strategy,
        "improved_probability": float(improved_prob),
        "impact": impact
    })

# BATCH PREDICT
@app.route("/batch_predict", methods=["POST"])
def batch_predict():
    file = request.files["file"]
    df = pd.read_csv(file)

    results = []

    high = medium = low = 0
    total_prob = 0
    all_drivers = []

    for _, row in df.iterrows():
        data = row.to_dict()

        input_df = pd.DataFrame([data])
        input_df = pd.get_dummies(input_df)
        input_df = input_df.reindex(columns=columns, fill_value=0)

        prob = model.predict_proba(input_df)[0][1]

        risk = get_risk(prob)
        drivers = get_drivers(data)

        total_prob += prob
        all_drivers.extend(drivers)

        if risk == "High":
            high += 1
        elif risk == "Medium":
            medium += 1
        else:
            low += 1

        results.append({
            "probability": float(prob),
            "risk": risk,
            "strategy": generate_strategy(prob, risk)
        })

    avg_prob = total_prob / len(df)

    summary = {
        "total_users": len(df),
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "average_probability": float(avg_prob),
        "top_drivers": list(set(all_drivers))
    }

    return jsonify({
        "individual": results,
        "summary": summary
    })

if __name__ == "__main__":
    app.run(debug=True)
    