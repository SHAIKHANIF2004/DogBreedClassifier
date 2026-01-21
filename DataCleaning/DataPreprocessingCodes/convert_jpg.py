# code/convert_to_jpg.py

import os
import cv2

# Path to your folder containing images
IMAGE_FOLDER = "C:/Users/shaik/Desktop/DogBreedClassification/images"  # Change this to your folder

# Loop through all files
for filename in os.listdir(IMAGE_FOLDER):
    file_path = os.path.join(IMAGE_FOLDER, filename)
    
    # Skip if it's already a jpg
    if filename.lower().endswith(".jpg"):
        continue
    
    try:
        # Read image
        img = cv2.imread(file_path)
        if img is None:
            print(f"Skipping {filename} (cannot read)")
            continue
        
        # Create new filename with .jpg extension
        new_filename = os.path.splitext(filename)[0] + ".jpg"
        new_file_path = os.path.join(IMAGE_FOLDER, new_filename)
        
        # Save as jpg
        cv2.imwrite(new_file_path, img)
        print(f"Converted {filename} → {new_filename}")
        
        # Optional: remove original file
        os.remove(file_path)
    except Exception as e:
        print(f"Error processing {filename}: {e}")
