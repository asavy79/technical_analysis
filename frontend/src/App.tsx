import "./App.css";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/home";

const About = () => (
  <div className="p-8">
    <h1 className="text-3xl">About Page</h1>
  </div>
);
const Contact = () => (
  <div className="p-8">
    <h1 className="text-3xl">Contact Page</h1>
  </div>
);

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </>
  );
}

export default App;
