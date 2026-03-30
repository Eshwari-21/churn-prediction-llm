import React, { useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

function App() {

  const [formData, setFormData] = useState({
    last_login_days: "",
    watch_hours: "",
    number_of_profiles: "",
    avg_watch_time_per_day: "",
    monthly_fee: ""
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/predict",
        {
          last_login_days: Number(formData.last_login_days),
          watch_hours: Number(formData.watch_hours),
          number_of_profiles: Number(formData.number_of_profiles),
          avg_watch_time_per_day: Number(formData.avg_watch_time_per_day),
          monthly_fee: Number(formData.monthly_fee)
        }
      );

      setResult(response.data);

    } catch (error) {
      alert("Backend error");
    }
  };

  return (
    <div style={{ padding: "40px" }}>

      <h2>Netflix Churn Prediction</h2>

      <input name="last_login_days" placeholder="Last Login Days" onChange={handleChange} /><br/><br/>
      <input name="watch_hours" placeholder="Watch Hours" onChange={handleChange} /><br/><br/>
      <input name="number_of_profiles" placeholder="Profiles" onChange={handleChange} /><br/><br/>
      <input name="avg_watch_time_per_day" placeholder="Avg Watch Time" onChange={handleChange} /><br/><br/>
      <input name="monthly_fee" placeholder="Monthly Fee" onChange={handleChange} /><br/><br/>

      <button onClick={handleSubmit}>Predict</button>

      {result && (
        <div style={{ marginTop: "30px" }}>

          <h3>Results</h3>

          <p><b>Churn Probability:</b> {result.churn_probability}</p>
          <p><b>Risk:</b> {result.risk}</p>

          <h4>Why churn risk?</h4>
          <ul>
            {result.feature_reasons.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>

          {result.strategy ? (
            <>
              <h4>Retention Strategy</h4>
              <p>{result.strategy}</p>
            </>
          ) : (
            <p>No strategy needed (Low Risk)</p>
          )}

          {result.after_strategy ? (
            <>
              <h4>Impact Analysis</h4>
              <LineChart width={300} height={200} data={[
                { name: "Before", value: result.churn_probability },
                { name: "After", value: result.after_strategy.new_probability }
              ]}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" />
              </LineChart>
            </>
          ) : (
            <p>No impact analysis available</p>
          )}

        </div>
      )}

    </div>
  );
}

export default App;