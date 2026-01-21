# pyright: reportMissingImports=false
# ============================================================
# 🐶 DOG BREED CLASSIFIER - TensorFlow Predictor (Final)
# ============================================================

import sys
import json
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image
import os

# Suppress TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# ------------------------------------------------------------
# ✅ Model and Label Setup
# ------------------------------------------------------------
MODEL_PATH = "efficientnetb3_clean_rgb.h5"
TRAIN_DIR = "final_dataset/train"

# Load model once
model = tf.keras.models.load_model(MODEL_PATH, compile=False)
class_labels = sorted(os.listdir(TRAIN_DIR))

# ------------------------------------------------------------
# ✅ Prediction Function
# ------------------------------------------------------------
def predict_breed(image_path):
    img = Image.open(image_path).convert("L")  # convert grayscale
    img = img.resize((300, 300))
    img_array = np.array(img, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=-1)
    img_array = np.repeat(img_array, 3, axis=-1)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    preds = model.predict(img_array, verbose=0)
    top_indices = np.argsort(preds[0])[-3:][::-1]
    top_breeds = [(class_labels[i], float(preds[0][i]) * 100) for i in top_indices]
    return top_breeds

# ------------------------------------------------------------
# ✅ Entry Point
# ------------------------------------------------------------
if __name__ == "__main__":
    image_path = sys.argv[1]
    results = predict_breed(image_path)
    output = [{"breed": b, "confidence": c} for b, c in results]
    print(json.dumps(output))  # Output clean JSON only
