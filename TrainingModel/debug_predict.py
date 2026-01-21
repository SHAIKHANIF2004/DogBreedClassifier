import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image
from PIL import Image

# ============================================================
# ✅ PATHS (update these if needed)
# ============================================================
base_dir = "final_dataset"          # same folder as in training
model_path = "efficientnetb3_clean_rgb.h5"   # your trained model

train_dir = os.path.join(base_dir, "train")
if not os.path.exists(train_dir):
    raise FileNotFoundError(f"Train folder not found: {train_dir}")

# ============================================================
# ✅ Load class names
# ============================================================
breed_labels = sorted(os.listdir(train_dir))
print(f"Loaded {len(breed_labels)} class labels.")
print("Example breeds:", breed_labels[:5])

# ============================================================
# ✅ Load model
# ============================================================
model = tf.keras.models.load_model(model_path, compile=False)
print("✅ Model loaded successfully.")

# ============================================================
# ✅ Choose one test image
# ============================================================
test_image_path = input("\nEnter path to a test dog image: ")

if not os.path.exists(test_image_path):
    raise FileNotFoundError(f"Image not found: {test_image_path}")

# ============================================================
# ✅ Try two preprocessing styles
# ============================================================
def preprocess_v1(img_path):
    img = Image.open(img_path).convert("RGB").resize((300, 300))
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, 0)

def preprocess_v2(img_path):
    img = Image.open(img_path).convert("RGB").resize((300, 300))
    arr = image.img_to_array(img)
    arr = tf.keras.applications.efficientnet.preprocess_input(arr)
    return np.expand_dims(arr, 0)

# ============================================================
# ✅ Predict using both methods
# ============================================================
for name, preprocess_fn in [("divide by 255", preprocess_v1), ("efficientnet preprocess", preprocess_v2)]:
    print(f"\n🔍 Predictions using {name}:")
    img_array = preprocess_fn(test_image_path)
    preds = model.predict(img_array)[0]
    top5_idx = preds.argsort()[-5:][::-1]
    for i in top5_idx:
        print(f"  idx {i:03d} | prob {preds[i]:.4f} | label {breed_labels[i]}")
