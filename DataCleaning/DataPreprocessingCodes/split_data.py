import os
import shutil
import random

SOURCE_DIR = r"C:\Users\shaik\Desktop\DogBreedClassification\images"
TRAIN_DIR = r"C:\Users\shaik\Desktop\DogBreedClassification\dataset\train"
VAL_DIR = r"C:\Users\shaik\Desktop\DogBreedClassification\dataset\val"
TEST_DIR = r"C:\Users\shaik\Desktop\DogBreedClassification\dataset\test"

train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

for folder in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
    os.makedirs(folder, exist_ok=True)

random.seed(42)

for breed in os.listdir(SOURCE_DIR):
    breed_path = os.path.join(SOURCE_DIR, breed)
    if not os.path.isdir(breed_path):
        continue
    
    # Only images
    images = [f for f in os.listdir(breed_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if len(images) == 0:
        continue
    
    random.shuffle(images)
    
    n_total = len(images)
    n_train = max(int(train_ratio * n_total), 1)
    n_val = max(int(val_ratio * n_total), 1)
    n_test = max(n_total - n_train - n_val, 1)
    
    for folder, n in zip([TRAIN_DIR, VAL_DIR, TEST_DIR], [n_train, n_val, n_test]):
        target_breed_dir = os.path.join(folder, breed)
        os.makedirs(target_breed_dir, exist_ok=True)
        for img in images[:n]:
            shutil.copy(os.path.join(breed_path, img), target_breed_dir)
        images = images[n:]
    
    print(f"{breed}: train={n_train}, val={n_val}, test={n_test}")

print("Dataset split completed successfully!")
