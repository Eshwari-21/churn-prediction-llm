import React, { useState } from "react";
import axios from "axios";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

function App() {
  const [formData, setFormData] = useState({
    last_login_days: "",
    watch_hours: "",
    profiles: "",
    avg_watch_time: "",
    monthly_fee: ""
  });

  const [result, setResult] = useState(null);
  const [file, setFile] = useState(null);
  const [batchResult, setBatchResult] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: Number(e.target.value)
    });
  };

  const handlePredict = async () => {
    try {
      const res = await axios.post("http://localhost:5000/predict", formData);
      setResult(res.data);
    } catch {
      alert("Backend not running!");
    }
  };

  const handleBatch = async () => {
    const fd = new FormData();
    fd.append("file", file);

    try {
      const res = await axios.post(
        "http://localhost:5000/batch_predict",
        fd
      );
      setBatchResult(res.data);
    } catch {
      alert("Batch failed!");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Netflix Churn Prediction</h2>

      {/* 🔹 SINGLE PREDICTION */}
      <h3>Single Prediction</h3>
      {Object.keys(formData).map((k) => (
        <input key={k} name={k} placeholder={k} onChange={handleChange} />
      ))}

      <br /><br />
      <button onClick={handlePredict}>Predict</button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <p><b>Probability:</b> {result.probability.toFixed(3)}</p>
          <p><b>Risk:</b> {result.risk}</p>

          <b>Strategies (LLM):</b>
          <ul>
            {result.strategy.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>

          <p><b>Impact:</b> {result.impact}</p>
        </div>
      )}

      <hr />

      {/* 🔹 BATCH */}
      <h3>Batch Prediction</h3>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <br /><br />
      <button onClick={handleBatch}>Run Batch</button>

      {/* 🔹 DASHBOARD SUMMARY */}
      {batchResult?.summary && (
        <div style={{ marginTop: 30 }}>
          <h2>📊 Dashboard Summary</h2>

          <div style={{
            display: "flex",
            gap: "20px",
            marginTop: "10px",
            fontWeight: "bold"
          }}>
            <div>👥 Total: {batchResult.summary.total_users}</div>
            <div>🔴 High: {batchResult.summary.high_risk}</div>
            <div>🟡 Medium: {batchResult.summary.medium_risk}</div>
            <div>🟢 Low: {batchResult.summary.low_risk}</div>
          </div>

          <p style={{ marginTop: 10 }}>
            Avg Probability: {batchResult.summary.average_probability.toFixed(3)}
          </p>

          {/* 🔥 LLM STRATEGY (CHECK THIS) */}
          {batchResult.summary.overall_strategy && (
            <>
              <b>LLM Strategies:</b>
              <ul>
                {batchResult.summary.overall_strategy.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}

      {/* 🔹 PIE CHART */}
      {batchResult?.summary && (
        <div style={{ marginTop: 30 }}>
          <h3 style={{ textAlign: "center" }}>Risk Distribution</h3>

          <div style={{
            width: "350px",
            height: "350px",
            margin: "auto"
          }}>
            <Pie
              data={{
                labels: ["High", "Medium", "Low"],
                datasets: [
                  {
                    data: [
                      batchResult.summary.high_risk,
                      batchResult.summary.medium_risk,
                      batchResult.summary.low_risk
                    ],
                    backgroundColor: [
                      "#ff4d4d",
                      "#ffc107",
                      "#28a745"
                    ]
                  }
                ]
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
