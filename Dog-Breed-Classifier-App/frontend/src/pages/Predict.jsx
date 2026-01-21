import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Predict() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [redirecting, setRedirecting] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setPrediction(null);
  };

  const handlePredict = async () => {
    if (!file) {
      alert("Please upload an image first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const res = await fetch("http://localhost:5000/predict", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      // ✅ Pick the top prediction (highest confidence)
      const topPrediction = data.prediction.sort(
        (a, b) => b.confidence - a.confidence
      )[0];

      // ✅ Clean breed name for display and search
      const cleanName = topPrediction.breed
        .replace(/^[nN]?\d+-/, "") // remove ID like n02085782-
        .replace(/[_-]/g, " ") // replace underscores or hyphens
        .replace(/\b\w/g, (c) => c.toUpperCase()); // capitalize words

      setPrediction({
        ...topPrediction,
        cleanBreed: cleanName,
      });
    } catch (err) {
      console.error("Prediction error:", err);
      alert("Something went wrong! Try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleKnowMore = (breed) => {
    setRedirecting(true);
    setTimeout(() => {
      navigate(`/breed/${encodeURIComponent(breed)}`);
    }, 1200);
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-linear-to-b from-gray-950 via-gray-900 to-black text-gray-100 px-6 py-12 overflow-hidden relative">
      {/* === BACK BUTTON === */}
      <button
        onClick={() => navigate("/home")}
        className="absolute top-6 left-6 px-5 py-2 text-sm font-semibold text-white bg-linear-to-r from-purple-600 to-pink-500 rounded-full hover:scale-105 transition-all duration-300 shadow-lg shadow-pink-500/40"
      >
        ⬅ Home
      </button>

      {/* === HEADER === */}
      <header className="text-center mb-10 animate-fadeIn">
        <h1 className="text-5xl font-extrabold bg-linear-to-r from-amber-400 via-pink-500 to-purple-600 text-transparent bg-clip-text drop-shadow-lg">
          🐕 Dog Breed Prediction
        </h1>
        <p className="text-gray-400 text-lg mt-3">
          Upload your dog’s image and find out its breed instantly!
        </p>
      </header>

      {/* === UPLOAD BOX === */}
      <div className="bg-gray-900/60 backdrop-blur-lg border border-gray-700 rounded-3xl p-10 shadow-xl shadow-purple-900/30 w-full max-w-2xl text-center animate-slideUp flex flex-col items-center">
        {/* File Upload */}
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-300 border border-gray-700 rounded-lg cursor-pointer bg-gray-800/50 p-3 focus:outline-none hover:bg-gray-800 transition"
        />

        {/* Preview */}
        {file && (
          <div className="mt-6">
            <img
              src={URL.createObjectURL(file)}
              alt="preview"
              className="rounded-2xl w-64 h-64 object-cover mx-auto border border-gray-700 shadow-lg shadow-purple-800/30"
            />
          </div>
        )}

        {/* Predict Button */}
        <button
          onClick={handlePredict}
          disabled={loading}
          className="mt-8 px-10 py-4 text-lg font-semibold text-white bg-linear-to-r from-purple-600 via-pink-500 to-amber-400 rounded-full hover:scale-105 transition-all duration-300 shadow-lg shadow-pink-600/40 disabled:opacity-50"
        >
          {loading ? "🔍 Analyzing..." : "🚀 Predict Breed"}
        </button>

        {/* === RESULT SECTION === */}
        {!loading && prediction && (
          <div className="mt-10 flex justify-center w-full">
            <div className="bg-gray-900/60 border border-gray-700 rounded-2xl p-6 w-full max-w-md text-center shadow-lg shadow-purple-800/20 animate-fadeIn">
              <h2 className="text-2xl font-semibold mb-4 text-pink-400">
                🐶 Predicted Breed
              </h2>

              <p className="text-2xl font-bold text-amber-400 mb-6">
                {prediction.cleanBreed}
              </p>

              {/* Know About Breed Button */}
              <button
                onClick={() => handleKnowMore(prediction.cleanBreed)}
                disabled={redirecting}
                className="mt-2 px-8 py-3 text-lg font-semibold text-white bg-linear-to-r from-amber-400 via-pink-500 to-purple-600 rounded-full hover:scale-105 transition-all duration-300 shadow-lg shadow-pink-500/40 disabled:opacity-70"
              >
                {redirecting ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                    Loading...
                  </span>
                ) : (
                  <>🐾 Know About {prediction.cleanBreed}</>
                )}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* === FOOTER === */}
      <footer className="text-sm text-gray-500 text-center mt-10">
        © 2025 Dog Breed Classifier | Built with ❤️ using React + TailwindCSS
      </footer>
    </div>
  );
}
