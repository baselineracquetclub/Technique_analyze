import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import UploadForm from "./components/UploadForm";
import AnalysisResult from "./components/AnalysisResult";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analyze" element={<UploadForm />} />
        <Route path="/results" element={<AnalysisResult />} />
      </Routes>
    </Router>
  );
}

export default App;

