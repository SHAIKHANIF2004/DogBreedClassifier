# code/remove_blur_duplicates.py

import os
import cv2
import hashlib
from collections import defaultdict

# Paths
PROCESSED_DIR = r"C:\Users\shaik\Desktop\DogBreedClassification\processed_dataset"

# Threshold for blur
BLUR_THRESHOLD = 100.0

# Track removed counts
removed_blur_counts = defaultdict(int)
removed_dup_counts = defaultdict(int)
total_blur_removed = 0
total_dup_removed = 0

# Track image hashes to detect duplicates
image_hashes = set()

def blur_score(image):
    """Return Laplacian variance (higher = sharper)"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def compute_hash(image):
    """Compute a hash of the image for duplicate detection"""
    img_bytes = cv2.imencode('.jpg', image)[1].tobytes()
    return hashlib.md5(img_bytes).hexdigest()

# Loop through processed dataset
for split in os.listdir(PROCESSED_DIR):
    split_dir = os.path.join(PROCESSED_DIR, split)
    if not os.path.isdir(split_dir):
        continue
    
    for breed in os.listdir(split_dir):
        breed_dir = os.path.join(split_dir, breed)
        if not os.path.isdir(breed_dir):
            continue
        
        for img_name in os.listdir(breed_dir):
            img_path = os.path.join(breed_dir, img_name)
            if not os.path.isfile(img_path):
                continue

            try:
                img = cv2.imread(img_path)
                if img is None:
                    continue

                # Check blur
                score = blur_score(img)
                if score < BLUR_THRESHOLD:
                    os.remove(img_path)
                    removed_blur_counts[breed] += 1
                    total_blur_removed += 1
                    print(f"🗑️ Removed blurry image: {img_path} (score={score:.2f})")
                    continue

                # Check duplicates
                img_hash = compute_hash(img)
                if img_hash in image_hashes:
                    os.remove(img_path)
                    removed_dup_counts[breed] += 1
                    total_dup_removed += 1
                    print(f"🗑️ Removed duplicate image: {img_path}")
                else:
                    image_hashes.add(img_hash)

            except Exception as e:
                print(f"Error processing {img_path}: {e}")

# Report
print("\n📊 Removal Summary:")
print("Blurry Images Removed:")
for breed, count in removed_blur_counts.items():
    print(f" - {breed}: {count}")
print(f"✅ Total blurry images removed: {total_blur_removed}")

print("\nDuplicate Images Removed:")
for breed, count in removed_dup_counts.items():
    print(f" - {breed}: {count}")
print(f"✅ Total duplicate images removed: {total_dup_removed}")
