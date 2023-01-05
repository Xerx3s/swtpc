import './index.css';
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";

// Importing Pages
import Home from "./pages/home";
import TreatmentMethods from "./pages/treatmentmethods";
import Faq from "./pages/faq";
import AnalyzeSimple from "./pages/analyze_simple";
import NoPage from "./pages/nopage";

const rootElement = createRoot(document.getElementById("root"));
rootElement.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />}>
        <Route path="/" element={<Home />} />
        <Route path="treatmentmethods" element={<TreatmentMethods />} />
        <Route path="faq" element={<Faq />} />
        <Route path="analyze/simple" element={<AnalyzeSimple />} />
        <Route path="*" element={<NoPage />} />
      </Route>
    </Routes>
  </BrowserRouter>
);