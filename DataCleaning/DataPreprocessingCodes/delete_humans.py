import os
import shutil
import random # Needed for random selection
from ultralytics import YOLO
from tqdm import tqdm

# --- Configuration ---
ROOT_DATASET_PATH = 'processed_dataset'
TARGET_SUBFOLDER = 'train'
DATASET_PATH = os.path.join(ROOT_DATASET_PATH, TARGET_SUBFOLDER)

MIN_IMAGES_PER_BREED = 80
MAX_IMAGES_PER_BREED = 85 # NEW: The desired maximum count
REJECTED_ROOT_FOLDER = 'rejected_train_images'

# Load a pre-trained YOLOv8 model for object detection
try:
    model = YOLO('yolov8n.pt')
except Exception as e:
    print(f"Error loading YOLOv8 model: {e}")
    print("Please ensure you have an internet connection to download the model weights.")
    exit()

# YOLO COCO Class IDs
PERSON_CLASS_ID = 0
CONFIDENCE_THRESHOLD = 0.5

# Create the root folder for rejected images
os.makedirs(REJECTED_ROOT_FOLDER, exist_ok=True)

# 1. Path Check
if not os.path.exists(DATASET_PATH):
    print(f"Error: The target path '{DATASET_PATH}' does not exist. Please check your folder structure.")
    exit()

breed_folders = sorted([d for d in os.listdir(DATASET_PATH) 
                        if os.path.isdir(os.path.join(DATASET_PATH, d))])
print(f"Found {len(breed_folders)} breed folders in the '{TARGET_SUBFOLDER}' set to process.")

# 2. Iterate through each breed
for breed_name in tqdm(breed_folders, desc=f"Filtering {TARGET_SUBFOLDER} Breeds (Target 80-90)"):
    breed_path = os.path.join(DATASET_PATH, breed_name)
    all_image_files = sorted([f for f in os.listdir(breed_path) 
                              if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    
    initial_count = len(all_image_files)
    
    # Lists for categorization
    human_images = []
    pure_dog_images = []
    
    # 3. Object Detection and Primary Filtering (Identify Human vs. Pure Dog)
    for image_filename in all_image_files:
        image_path = os.path.join(breed_path, image_filename)
        
        try:
            results = model.predict(source=image_path, verbose=False, conf=CONFIDENCE_THRESHOLD)
            person_detected = False
            
            if results and results[0].boxes is not None:
                for box in results[0].boxes:
                    if int(box.cls.item()) == PERSON_CLASS_ID:
                        person_detected = True
                        break
            
            if person_detected:
                human_images.append(image_filename)
            else:
                pure_dog_images.append(image_filename)
                
        except Exception as e:
            print(f"\n[ERROR] Could not process image {image_filename} in {breed_name}: {e}")
            
    
    # 4. Enforce Minimum (80) and Maximum (90) Limits
    images_to_delete = []
    current_total_count = len(human_images) + len(pure_dog_images)
    
    # --- STEP A: Prioritize removing Human Images ---
    # Determine how many human images we MUST keep to meet the minimum 80
    required_human_to_keep = max(0, MIN_IMAGES_PER_BREED - len(pure_dog_images))
    
    # The number of human images we can safely remove
    human_images_to_remove = human_images[:len(human_images) - required_human_to_keep]
    images_to_delete.extend(human_images_to_remove)
    
    # Remaining human images are the ones we must keep (or are too few to care about)
    human_images_kept = human_images[len(human_images) - required_human_to_keep:]
    
    # Update current total count after first wave of removals
    current_total_count = len(pure_dog_images) + len(human_images_kept)

    # --- STEP B: Randomly remove remaining excess images to hit MAX (90) ---
    if current_total_count > MAX_IMAGES_PER_BREED:
        excess_count = current_total_count - MAX_IMAGES_PER_BREED
        
        # Combine the lists of images available for random removal
        # (It's safer to remove from the remaining human images first, then pure dogs)
        removable_images = human_images_kept + pure_dog_images
        
        # Ensure we don't accidentally drop below the min threshold of 80
        # This check is mostly for safety, as the limit is MAX_IMAGES_PER_BREED=90
        if (current_total_count - excess_count) < MIN_IMAGES_PER_BREED:
             excess_count = current_total_count - MIN_IMAGES_PER_BREED
             
        # Randomly select excess_count images from the removable list
        # Ensure we have enough images to remove
        if excess_count > 0 and len(removable_images) >= excess_count:
             random_removals = random.sample(removable_images, excess_count)
             images_to_delete.extend(random_removals)
             
    # 5. Remove and Relocate Images
    
    # Create a subfolder for rejected images of this breed
    breed_rejected_path = os.path.join(REJECTED_ROOT_FOLDER, breed_name)
    os.makedirs(breed_rejected_path, exist_ok=True)
    
    final_images_deleted = []
    
    for image_filename in set(images_to_delete): # Use set to handle potential duplicates in list extensions
        src_path = os.path.join(breed_path, image_filename)
        dst_path = os.path.join(breed_rejected_path, image_filename)
        
        # Only move the file if it still exists (i.e., hasn't been moved by an earlier loop)
        if os.path.exists(src_path):
            try:
                shutil.move(src_path, dst_path)
                final_images_deleted.append(image_filename)
            except Exception as e:
                print(f"\n[ERROR] Could not move file {src_path}: {e}")

    # 6. Report
    total_removed = len(final_images_deleted)
    final_count = initial_count - total_removed
    
    if total_removed > 0 or final_count < MIN_IMAGES_PER_BREED or final_count > MAX_IMAGES_PER_BREED:
        print(f"\n🐶 **Breed: {breed_name}**")
        print(f"   Initial Images: {initial_count}")
        print(f"   Images Removed: {total_removed}")
        print(f"   Final Images:   {final_count} (Target Range: 80-90)")
        
        if final_count < MIN_IMAGES_PER_BREED:
             print(f"   ⚠️ **WARNING:** Final count is below the minimum of {MIN_IMAGES_PER_BREED}.")
        elif final_count > MAX_IMAGES_PER_BREED:
             print(f"   ⚠️ **WARNING:** Final count is above the maximum of {MAX_IMAGES_PER_BREED}.")


print("\n--- Training Data Filtering Complete ---")
print(f"Rejected training images moved to the '{REJECTED_ROOT_FOLDER}' folder for review.")