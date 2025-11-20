import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function AnalysisResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const data = location.state?.data;

  if (!data) {
    return (
      <div style={styles.container}>
        <p>No analysis data available. Try running a new analysis.</p>
        <button style={styles.button} onClick={() => navigate("/")}>
          Back to Home
        </button>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>
        {data.student} — {data.stroke}
      </h2>

      <section>
        <h3 style={styles.sectionTitle}>What You're Doing Well</h3>
        {data.suggestions.doing_well.length === 0 && (
          <p style={styles.text}>No positives detected yet.</p>
        )}
        {data.suggestions.doing_well.map((s, i) => (
          <p key={i} style={styles.good}>
            {s}
          </p>
        ))}
      </section>

      <section>
        <h3 style={styles.sectionTitle}>What to Improve</h3>
        {data.suggestions.work_on.length === 0 && (
          <p style={styles.text}>No issues detected. Great job!</p>
        )}
        {data.suggestions.work_on.map((s, i) => (
          <p key={i} style={styles.bad}>
            {s}
          </p>
        ))}
      </section>

      <button style={styles.button} onClick={() => navigate("/")}>
        Back to Home
      </button>
    </div>
  );
}

const styles = {
  container: { padding: 20 },
  header: { fontSize: 22, fontWeight: "bold", marginBottom: 20 },
  sectionTitle: {
    fontSize: 18,
    marginTop: 20,
    fontWeight: 600,
    color: "#1a3e72",
  },
  text: {
    padding: 10,
  },
  good: {
    backgroundColor: "#e9f5ff",
    padding: 10,
    borderRadius: 6,
    marginBottom: 6,
  },
  bad: {
    backgroundColor: "#fff4e5",
    padding: 10,
    borderRadius: 6,
    marginBottom: 6,
  },
  button: {
    marginTop: 30,
    backgroundColor: "#1a73e8",
    color: "#fff",
    border: "none",
    padding: 15,
    borderRadius: 8,
    fontSize: 18,
    cursor: "pointer",
  },
};

