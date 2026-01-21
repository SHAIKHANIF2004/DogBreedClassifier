import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  FaDog,
  FaGlobeAsia,
  FaHeartbeat,
  FaRulerVertical,
  FaWeight,
  FaHome,
} from "react-icons/fa";

export default function BreedInfo() {
  const { breedName } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [info, setInfo] = useState(null);

  useEffect(() => {
    async function fetchBreedInfo() {
      setLoading(true);
      try {
        const cleanName = breedName.replace(/n\d+-/gi, "").replace(/_/g, " ");

        // ✅ Fetch breed info
        const res = await fetch(
          `https://api.thedogapi.com/v1/breeds/search?q=${encodeURIComponent(
            cleanName
          )}`
        );
        const data = await res.json();
        const breed = data[0];

        if (breed) {
          // ✅ Get high-quality image
          let imageUrl = "";
          if (breed.reference_image_id) {
            const imgRes = await fetch(
              `https://api.thedogapi.com/v1/images/${breed.reference_image_id}`
            );
            const imgData = await imgRes.json();
            imageUrl = imgData.url;
          }

          setInfo({
            name: breed.name,
            origin: breed.origin || "Unknown",
            breed_group: breed.breed_group || "—",
            life_span: breed.life_span || "—",
            height: breed.height?.metric || "—",
            weight: breed.weight?.metric || "—",
            temperament: breed.temperament || "—",
            bred_for: breed.bred_for || "—",
            image:
              imageUrl || "https://cdn2.thedogapi.com/images/BJa4kxc4X.jpg",
            description:
              breed.temperament ||
              "No detailed description available for this breed.",
          });
        } else {
          // fallback if not found
          setInfo({
            name: cleanName,
            origin: "Unknown",
            breed_group: "—",
            life_span: "—",
            height: "—",
            weight: "—",
            temperament: "—",
            bred_for: "—",
            image: "https://cdn2.thedogapi.com/images/BJa4kxc4X.jpg",
            description:
              "No information available for this breed at the moment.",
          });
        }
      } catch (error) {
        console.error("Error fetching breed info:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchBreedInfo();
  }, [breedName]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-linear-to-b from-gray-950 via-gray-900 to-black text-gray-300">
        <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-pink-500 mb-4"></div>
        <p>Fetching breed details...</p>
      </div>
    );
  }

  if (!info) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-linear-to-b from-gray-950 via-gray-900 to-black text-gray-300">
        <p>No breed information found.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-linear-to-b from-gray-950 via-gray-900 to-black text-gray-100 px-6 py-12 relative">
      {/* Back Button */}
      <button
        onClick={() => navigate("/home")}
        className="absolute top-6 left-6 flex items-center gap-2 px-5 py-2 text-sm font-semibold text-white bg-linear-to-r from-purple-600 to-pink-500 rounded-full hover:scale-105 transition-all duration-300 shadow-lg shadow-pink-500/40"
      >
        <FaHome /> Home
      </button>

      {/* Header */}
      <header className="text-center mb-12">
        <h1 className="text-5xl font-extrabold bg-linear-to-r from-amber-400 via-pink-500 to-purple-600 text-transparent bg-clip-text drop-shadow-lg">
          🐶 {info.name}
        </h1>
        <p className="text-gray-400 text-lg mt-3">
          Learn more about your furry friend 🩵
        </p>
      </header>

      {/* Main Card */}
      <div className="bg-gray-900/70 backdrop-blur-lg border border-gray-700 rounded-3xl p-10 shadow-2xl w-full max-w-6xl mx-auto grid md:grid-cols-2 gap-10 items-center">
        {/* Left: Image */}
        <div className="flex flex-col items-center">
          <img
            src={info.image}
            alt={info.name}
            className="rounded-2xl w-full h-80 object-cover shadow-lg border border-gray-700 mb-6"
          />
          <p className="text-center text-gray-400 italic">{info.description}</p>
        </div>

        {/* Right: Info */}
        <div className="text-gray-200 space-y-6">
          <div>
            <h3 className="text-2xl font-bold text-pink-400 mb-2">
              🌍 Origin & Group
            </h3>
            <p className="flex items-center gap-2">
              <FaGlobeAsia /> <span>Origin:</span> {info.origin}
            </p>
            <p className="flex items-center gap-2">
              <FaDog /> <span>Breed Group:</span> {info.breed_group}
            </p>
          </div>

          <div>
            <h3 className="text-2xl font-bold text-pink-400 mb-2">
              📏 Size & Lifespan
            </h3>
            <p className="flex items-center gap-2">
              <FaRulerVertical /> Height: {info.height} cm
            </p>
            <p className="flex items-center gap-2">
              <FaWeight /> Weight: {info.weight} kg
            </p>
            <p className="flex items-center gap-2">
              <FaHeartbeat /> Lifespan: {info.life_span}
            </p>
          </div>

          <div>
            <h3 className="text-2xl font-bold text-pink-400 mb-2">
              💖 Temperament
            </h3>
            <p>{info.temperament}</p>
          </div>

          <div>
            <h3 className="text-2xl font-bold text-pink-400 mb-2">✨ Traits</h3>
            <p>Bred For: {info.bred_for}</p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="text-sm text-gray-500 text-center mt-12">
        © 2025 Dog Breed Classifier | Made with ❤️ using React + TailwindCSS
      </footer>
    </div>
  );
}
