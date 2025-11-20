import React from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Tennis Technique Analyzer</h1>
      <p style={styles.subtitle}>
        Upload a short stroke video and get quick coaching feedback.
      </p>
      <button style={styles.button} onClick={() => navigate("/analyze")}>
        Start New Analysis
      </button>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
    backgroundColor: "#ffffff",
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#1a3e72",
    marginBottom: 10,
    textAlign: "center",
  },
  subtitle: {
    fontSize: 16,
    color: "#5a5a5a",
    marginBottom: 40,
    textAlign: "center",
    maxWidth: 320,
  },
  button: {
    backgroundColor: "#1a73e8",
    color: "#fff",
    border: "none",
    padding: "15px 30px",
    borderRadius: 8,
    fontSize: 18,
    cursor: "pointer",
    width: "80%",
    maxWidth: 300,
  },
};

