import os
import cv2

# ---------------- CONFIG ----------------
base_dir = r"C:\Users\shaik\Desktop\DogBreedClassification\processed_dataset"
splits = ['train', 'val', 'test']
target_images = {'train': 60, 'val': 20, 'test': 20}  # adjust per split
min_width = 100
min_height = 100
blur_threshold = 100
target_size = (224, 224)  # resize all images

# ---------------- PROCESS ----------------
for split in splits:
    split_dir = os.path.join(base_dir, split)
    print(f"\n===== Processing {split} =====")
    
    for breed in os.listdir(split_dir):
        breed_path = os.path.join(split_dir, breed)
        if not os.path.isdir(breed_path):
            continue

        print(f"\nProcessing breed: {breed}")
        all_files = os.listdir(breed_path)
        image_files = [f for f in all_files if f.lower().endswith(('.jpg','.jpeg','.png'))]

        valid_images = []

        # Step 1: Keep only clear and valid images, resize
        for img_name in image_files:
            img_path = os.path.join(breed_path, img_name)
            try:
                img = cv2.imread(img_path)
                if img is None:
                    continue
                h, w = img.shape[:2]
                if h < min_height or w < min_width:
                    continue
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
                if lap_var < blur_threshold:
                    continue

                # Resize to 224x224
                img_resized = cv2.resize(img, target_size)
                cv2.imwrite(img_path, img_resized)
                valid_images.append(img_name)
            except:
                continue

        # Step 2: Check if enough images
        required = target_images[split]
        if len(valid_images) < required:
            print(f"⚠️ Breed {breed} in {split} has only {len(valid_images)} valid images. Needed {required}. Skipping...")
            continue

        # Step 3: Keep exactly required number
        images_to_keep = valid_images[:required]
        images_to_remove = set(image_files) - set(images_to_keep)
        for img_name in images_to_remove:
            os.remove(os.path.join(breed_path, img_name))

        print(f"✅ Breed {breed} in {split}: kept exactly {required} clear images resized to 224x224.")
