// ============================================================
// 🐶 DOG BREED CLASSIFIER - Express Backend (Final Version)
// ============================================================
import express from "express";
import multer from "multer";
import cors from "cors";
import { spawn } from "child_process";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

// Configure multer for image uploads
const upload = multer({ dest: "uploads/" });

// ------------------------------------------------------------
// ✅ Prediction Endpoint
// ------------------------------------------------------------
app.post("/predict", upload.single("file"), (req, res) => {
  const imagePath = req.file.path;

  // Call Python script for prediction
  const pythonProcess = spawn("python", ["predictor.py", imagePath]);

  let result = "";

  pythonProcess.stdout.on("data", (data) => {
    result += data.toString();
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error("🐍 Python error:", data.toString());
  });

  pythonProcess.on("close", () => {
    try {
      fs.unlinkSync(imagePath); // cleanup temp file
      res.json({ prediction: JSON.parse(result.trim()) });
    } catch (err) {
      console.error("Error parsing prediction:", err);
      res.status(500).json({ error: "Prediction failed" });
    }
  });
});

// ------------------------------------------------------------
// ✅ Server Listen
// ------------------------------------------------------------
app.listen(PORT, () => {
  console.log(`✅ Backend running at http://localhost:${PORT}`);
});
