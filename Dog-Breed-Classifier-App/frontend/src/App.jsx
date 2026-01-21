import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Predict from "./pages/Predict";
import BreedInfo from "./pages/BreedInfo";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/predict" element={<Predict />} />
        <Route path="/breed/:breedName" element={<BreedInfo />} />
      </Routes>
    </Router>
  );
}
