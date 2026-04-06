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

  // ✅ SAFE API CALL
  const handlePredict = async () => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/predict",
        formData
      );
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Backend error — check if server is running");
    }
  };

  // ✅ SAFE BATCH
  const handleBatch = async () => {
    try {
      const fd = new FormData();
      fd.append("file", file);

      const res = await axios.post(
        "http://127.0.0.1:5000/batch_predict",
        fd
      );

      setBatchResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Batch failed — check backend");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Netflix Churn Prediction</h2>

      {/* ================= SINGLE ================= */}
      <h3>Single Prediction</h3>

      {Object.keys(formData).map((k) => (
        <input
          key={k}
          name={k}
          placeholder={k}
          onChange={handleChange}
        />
      ))}

      <br /><br />
      <button onClick={handlePredict}>Predict</button>

      {/* ✅ SAFE RESULT DISPLAY */}
      {result && !result.error && (
        <div>
          <p>
            <b>Probability:</b>{" "}
            {result?.probability !== undefined
              ? result.probability.toFixed(3)
              : "N/A"}
          </p>

          <p><b>Risk:</b> {result?.risk || "N/A"}</p>

          <b>LLM Strategies:</b>
          <ul>
            {result?.strategy?.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>

          <p><b>Impact:</b> {result?.impact || "N/A"}</p>

          {/* ✅ GRAPH */}
          <div style={{ width: "300px" }}>
            <Pie
              data={{
                labels: ["Before", "After"],
                datasets: [{
                  data: [
                    result?.probability || 0,
                    result?.improved_probability || 0
                  ],
                  backgroundColor: ["#ff4d4d", "#28a745"]
                }]
              }}
            />
          </div>
        </div>
      )}

      {/* ❗ ERROR DISPLAY */}
      {result?.error && (
        <p style={{ color: "red" }}>
          Backend Error: {result.error}
        </p>
      )}

      <hr />

      {/* ================= BATCH ================= */}
      <h3>Batch Prediction</h3>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <br /><br />
      <button onClick={handleBatch}>Run Batch</button>

      {/* ✅ SAFE BATCH DISPLAY */}
      {batchResult?.summary && (
        <div>
          <h2>Dashboard</h2>

          <p>Total: {batchResult.summary.total_users}</p>
          <p>High: {batchResult.summary.high_risk}</p>
          <p>Medium: {batchResult.summary.medium_risk}</p>
          <p>Low: {batchResult.summary.low_risk}</p>
          <p>Avg Prob: {batchResult.summary.average_probability?.toFixed(3)}</p>

          <b>LLM Strategies:</b>
          <ul>
            {batchResult.summary.overall_strategy?.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>

          <p><b>Impact:</b> {batchResult.summary.impact}</p>

          {/* ✅ GRAPH */}
          <div style={{ width: "300px" }}>
            <Pie
              data={{
                labels: ["High", "Medium", "Low"],
                datasets: [{
                  data: [
                    batchResult.summary.high_risk,
                    batchResult.summary.medium_risk,
                    batchResult.summary.low_risk
                  ],
                  backgroundColor: ["#ff4d4d", "#ffc107", "#28a745"]
                }]
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;