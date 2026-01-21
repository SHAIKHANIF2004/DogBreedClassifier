import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      navigate("/home");
    }, 1500);
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-linear-to-b from-gray-950 via-gray-900 to-black text-gray-100 px-6 py-10 overflow-hidden">
      {/* ===== Header Section ===== */}
      <header className="text-center space-y-4 animate-fadeIn mb-10">
        <h1 className="text-5xl md:text-6xl font-extrabold bg-linear-to-r from-amber-400 via-pink-500 to-purple-600 text-transparent bg-clip-text drop-shadow-lg">
          🐾 Welcome Back!
        </h1>
        <p className="text-lg text-gray-400 max-w-xl mx-auto leading-relaxed">
          Login to continue exploring your Dog Breed Classifier 🐶
        </p>
      </header>

      {/* ===== Login Card ===== */}
      <div className="bg-white/10 backdrop-blur-lg border border-gray-800 shadow-xl rounded-2xl p-8 w-full max-w-md animate-fadeIn">
        <form onSubmit={handleLogin} className="flex flex-col gap-5">
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="px-4 py-3 rounded-xl bg-gray-900 text-gray-100 placeholder-gray-400 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-pink-500"
            required
          />

          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="px-4 py-3 rounded-xl bg-gray-900 text-gray-100 placeholder-gray-400 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-pink-500"
            required
          />

          <button
            type="submit"
            disabled={loading}
            className="mt-4 px-8 py-3 rounded-full text-lg font-semibold text-white bg-linear-to-r from-purple-600 via-pink-500 to-amber-400 hover:scale-105 transition-all duration-300 shadow-lg shadow-pink-600/40"
          >
            {loading ? "🐕 Logging in..." : "Login"}
          </button>
        </form>

        {/* Loader */}
        {loading && (
          <div className="flex justify-center mt-6">
            <div className="w-10 h-10 border-4 border-t-transparent border-amber-400 rounded-full animate-spin"></div>
          </div>
        )}
      </div>

      {/* ===== Footer ===== */}
      <footer className="text-sm text-gray-500 text-center mt-10">
        © 2025 Dog Breed Classifier | Built with ❤️ using React + TailwindCSS
      </footer>
    </div>
  );
}
