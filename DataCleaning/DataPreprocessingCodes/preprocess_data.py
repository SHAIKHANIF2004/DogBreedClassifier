# code/preprocess_dataset_clean.py

import os
import cv2
from collections import defaultdict

# Paths
SOURCE_DIR = r"C:\Users\shaik\Desktop\DogBreedClassification\dataset"
TARGET_DIR = r"C:\Users\shaik\Desktop\DogBreedClassification\processed_dataset"
TARGET_SIZE = (224, 224)

# Create target folder
os.makedirs(TARGET_DIR, exist_ok=True)

# Track processed counts
processed_counts = defaultdict(int)

def process_folder(src_folder, dst_folder):
    """Process all images in a folder: resize and save as uint8."""
    os.makedirs(dst_folder, exist_ok=True)
    count = 0
    for img_name in os.listdir(src_folder):
        src_path = os.path.join(src_folder, img_name)
        dst_path = os.path.join(dst_folder, os.path.splitext(img_name)[0] + ".jpg")
        try:
            img = cv2.imread(src_path)
            if img is None:
                continue

            # Resize
            img = cv2.resize(img, TARGET_SIZE)

            # Ensure image is uint8 to avoid OpenCV warnings
            img = img.astype("uint8")

            # Save processed image
            cv2.imwrite(dst_path, img)
            count += 1

        except Exception as e:
            print(f"Error processing {src_path}: {e}")
    return count

# Main processing
for item in os.listdir(SOURCE_DIR):
    item_path = os.path.join(SOURCE_DIR, item)
    
    # If split folder exists (train/val/test)
    if os.path.isdir(item_path) and item.lower() in ["train", "val", "test"]:
        split_name = item
        for breed in os.listdir(item_path):
            breed_src = os.path.join(item_path, breed)
            if not os.path.isdir(breed_src):
                continue
            breed_dst = os.path.join(TARGET_DIR, split_name, breed)
            count = process_folder(breed_src, breed_dst)
            processed_counts[f"{split_name}/{breed}"] = count

    # If dataset has only breed folders
    elif os.path.isdir(item_path):
        breed = item
        breed_dst = os.path.join(TARGET_DIR, breed)
        count = process_folder(item_path, breed_dst)
        processed_counts[breed] = count

# Print summary
print("\n📊 Preprocessed Dataset Summary:")
for key, count in processed_counts.items():
    print(f"{key}: {count} images")
