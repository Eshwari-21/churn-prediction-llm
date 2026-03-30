from flask import Flask, request, jsonify
import joblib
from feature_engineering import preprocess
from gemini_engine import generate_strategy
from impact_engine import estimate_impact

app = Flask(__name__)

model = joblib.load("../models/churn_model.pkl")


def get_risk(prob):
    if prob > 0.7:
        return "High"
    elif prob > 0.4:
        return "Medium"
    return "Low"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    processed = preprocess(data)
    prob = model.predict_proba([processed])[0][1]

    risk = get_risk(prob)

    result = {
        "churn_probability": round(prob, 3),
        "risk": risk
    }

    if prob > 0.4:
        result["strategy"] = generate_strategy(data, prob, risk)
        result["after_strategy"] = estimate_impact(data, prob)

    return jsonify(result)


@app.route("/batch", methods=["POST"])
def batch():
    file = request.files["file"]
    key_area = request.args.get("key_area")

    path = "temp.csv"
    file.save(path)

    batch_predict(path, key_area)

    return {"message": "Batch completed. Check output.csv"}


if __name__ == "__main__":
    app.run(debug=True)