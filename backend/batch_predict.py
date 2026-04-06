@app.route("/batch_predict", methods=["POST"])
def batch_predict():
    global llm_calls

    try:
        file = request.files["file"]
        df = pd.read_csv(file)

        results = []

        high, medium, low = 0, 0, 0
        total_prob = 0
        all_drivers = []

        for _, row in df.iterrows():
            data = row.to_dict()

            input_df = pd.DataFrame([data])
            input_df = input_df.reindex(columns=columns, fill_value=0)

            scaled = scaler.transform(input_df)
            prob = model.predict_proba(scaled)[0][1]

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

            # 🔥 Only few LLM calls
            if prob > 0.5 and llm_calls < 5:
                strategy = generate_strategy(data, prob, risk)
                llm_calls += 1
            else:
                strategy = ["Low priority"]

            results.append({
                "probability": float(prob),
                "risk": risk,
                "drivers": drivers,
                "strategy": strategy
            })

        # 🔥 SUMMARY
        avg_prob = total_prob / len(df)

        top_drivers = list(set(all_drivers))[:5]

        # 🔥 ONE LLM CALL FOR WHOLE DATA
        summary_strategy = generate_strategy(
            {"drivers": top_drivers},
            avg_prob,
            "Mixed"
        )

        return jsonify({
            "individual": results,
            "summary": {
                "total_users": len(df),
                "high_risk": high,
                "medium_risk": medium,
                "low_risk": low,
                "average_probability": avg_prob,
                "top_drivers": top_drivers,
                "overall_strategy": summary_strategy
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500