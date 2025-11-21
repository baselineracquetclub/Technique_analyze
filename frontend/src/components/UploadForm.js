import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const API_BASE =
  process.env.REACT_APP_API_BASE_URL || 10.1.10.134:8000;

export default function UploadForm() {
  const [studentName, setStudentName] = useState("");
  const [strokeType, setStrokeType] = useState("forehand");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please upload a video.");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("student_name", studentName);
    formData.append("stroke_type", strokeType);

    try {
      const res = await axios.post(`${API_BASE}/analyze`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      navigate("/results", { state: { data: res.data } });
    } catch (err) {
      console.error(err);
      alert("Error analyzing video. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>Analyze Stroke</h2>

      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          style={styles.input}
          type="text"
          placeholder="Student Name"
          value={studentName}
          onChange={(e) => setStudentName(e.target.value)}
          required
        />

        <select
          style={styles.input}
          value={strokeType}
          onChange={(e) => setStrokeType(e.target.value)}
        >
          <option value="forehand">Forehand</option>
          <option value="backhand">Backhand</option>
          <option value="serve">Serve</option>
          <option value="volley">Volley</option>
        </select>

        <input
          style={styles.input}
          type="file"
          accept="video/*"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button style={styles.button} type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>
    </div>
  );
}

const styles = {
  container: { padding: 20 },
  header: {
    fontSize: 24,
    marginBottom: 20,
    fontWeight: "bold",
    color: "#1a3e72",
  },
  form: { display: "flex", flexDirection: "column", gap: 15 },
  input: {
    padding: 12,
    borderRadius: 8,
    border: "1px solid #ccc",
    fontSize: 16,
  },
  button: {
    backgroundColor: "#1a73e8",
    color: "#fff",
    border: "none",
    padding: 15,
    borderRadius: 8,
    fontSize: 18,
    cursor: "pointer",
  },
};

