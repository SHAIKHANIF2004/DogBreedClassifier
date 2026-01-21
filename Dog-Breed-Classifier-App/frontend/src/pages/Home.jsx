import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Home() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const dogImages = [
    "https://images.unsplash.com/photo-1558788353-f76d92427f16?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1507149833265-60c372daea22?auto=format&fit=crop&w=400&q=80",
  ];

  const handleLogoutClick = () => {
    setShowConfirm(true);
  };

  const confirmLogout = () => {
    setShowConfirm(false);
    navigate("/");
  };

  const cancelLogout = () => {
    setShowConfirm(false);
  };

  // 🚀 Predict with loader
  const handlePredict = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      navigate("/predict");
    }, 2000);
  };

  return (
    <div className="min-h-screen flex flex-col justify-between items-center bg-linear-to-b from-gray-950 via-gray-900 to-black text-gray-100 px-6 py-10 overflow-hidden relative">
      {/* ===== Logout Button ===== */}
      <button
        onClick={handleLogoutClick}
        className="absolute top-6 right-6 px-5 py-2 text-sm font-semibold text-white bg-linear-to-r from-red-600 to-pink-500 rounded-full hover:scale-105 transition-all duration-300 shadow-lg shadow-pink-600/40"
      >
        🔒 Logout
      </button>

      {/* ===== Header Section ===== */}
      <header className="text-center space-y-4 animate-fadeIn mt-10">
        <h1 className="text-5xl md:text-6xl font-extrabold bg-linear-to-r from-amber-400 via-pink-500 to-purple-600 text-transparent bg-clip-text drop-shadow-lg">
          🐾 Dog Breed Classifier
        </h1>
        <p className="text-lg text-gray-400 max-w-2xl mx-auto leading-relaxed">
          Upload your dog’s photo and let AI identify its breed instantly!
        </p>
      </header>

      {/* ===== Dog Gallery (5 Images) ===== */}
      <section className="flex justify-center gap-6 mt-10 flex-wrap">
        {dogImages.map((url, index) => (
          <div
            key={index}
            className="relative overflow-hidden rounded-2xl group shadow-lg shadow-purple-900/40 hover:scale-105 transition-transform duration-300"
          >
            <img
              src={url}
              alt={`Dog ${index + 1}`}
              loading="lazy"
              className="w-44 h-44 md:w-48 md:h-48 object-cover rounded-2xl border border-gray-800"
            />
          </div>
        ))}
      </section>

      {/* ===== Predict Button ===== */}
      <div className="mt-12 mb-6 animate-fadeIn">
        <button
          onClick={handlePredict}
          disabled={loading}
          className={`px-10 py-4 text-lg font-semibold text-white bg-linear-to-r from-purple-600 via-pink-500 to-amber-400 rounded-full transition-all duration-300 shadow-lg shadow-pink-600/40 ${
            loading ? "opacity-60 cursor-not-allowed" : "hover:scale-105"
          }`}
        >
          {loading ? "⏳ Loading..." : "🚀 Start Prediction"}
        </button>
      </div>

      {/* ===== Footer ===== */}
      <footer className="text-sm text-gray-500 text-center">
        © 2025 Dog Breed Classifier | Built with ❤️ using React + TailwindCSS
      </footer>

      {/* ===== Loader Overlay ===== */}
      {loading && (
        <div className="fixed inset-0 bg-black/80 flex flex-col items-center justify-center z-50">
          <div className="w-16 h-16 border-4 border-pink-500 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-lg text-gray-300">Preparing your prediction...</p>
        </div>
      )}

      {/* ===== Logout Confirmation Modal ===== */}
      {showConfirm && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 animate-fadeIn">
          <div className="bg-gray-900 rounded-2xl p-8 shadow-lg text-center border border-pink-600/40 max-w-sm w-full mx-4">
            <h2
              className="text-2xl font-semibold mb-4 text-transparent bg-clip-text bg-linear-to-r
 from-amber-400 via-pink-500 to-purple-600"
            >
              Confirm Logout
            </h2>
            <p className="text-gray-300 mb-6">
              Are you sure you want to log out of Dog Breed Classifier?
            </p>
            <div className="flex justify-center gap-4">
              <button
                onClick={confirmLogout}
                className="px-5 py-2 bg-linear-to-r from-red-600 to-pink-500 rounded-full text-white font-medium hover:scale-105 transition-all duration-200"
              >
                Yes, Log Out
              </button>
              <button
                onClick={cancelLogout}
                className="px-5 py-2 bg-gray-700 rounded-full text-gray-300 hover:scale-105 transition-all duration-200"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
