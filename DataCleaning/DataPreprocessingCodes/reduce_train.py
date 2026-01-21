import os
import cv2

# ------------------ CONFIG ------------------
train_dir = r"C:\Users\shaik\Desktop\DogBreedClassification\processed_dataset"
# your local train path
target_images = 60
min_width = 100
min_height = 100
blur_threshold = 100  # lower = more blurry

# ------------------ PROCESS ------------------
for breed in os.listdir(train_dir):
    breed_path = os.path.join(train_dir, breed)
    if not os.path.isdir(breed_path):
        continue
    
    print(f"\nProcessing breed: {breed}")
    images = os.listdir(breed_path)
    valid_images = []
    
    # Step 1: Keep only clear images
    for img_name in images:
        img_path = os.path.join(breed_path, img_name)
        try:
            img = cv2.imread(img_path)
            if img is None:
                continue  # skip unreadable
            h, w = img.shape[:2]
            if h < min_height or w < min_width:
                continue  # skip too small
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            if laplacian_var < blur_threshold:
                continue  # skip blurry
            valid_images.append(img_name)
        except:
            continue
    
    # Step 2: Check if we have enough images
    if len(valid_images) < target_images:
        print(f"⚠️ Breed {breed} has only {len(valid_images)} clear images. Need at least {target_images}.")
        continue  # skip this breed, or you can manually add images
    
    # Step 3: Keep exactly 60 images
    images_to_keep = valid_images[:target_images]
    images_to_remove = set(os.listdir(breed_path)) - set(images_to_keep)
    for img_name in images_to_remove:
        os.remove(os.path.join(breed_path, img_name))
    
    print(f"✅ Breed {breed}: kept exactly {target_images} clear images.")
