# code/count_images_breedwise.py

import os
from collections import defaultdict

# Path to processed dataset
PROCESSED_DIR = r"C:\Users\shaik\Desktop\DogBreedClassification\processed_dataset"

# Dictionary: {split: {breed: count}}
image_counts = defaultdict(lambda: defaultdict(int))
total_counts = defaultdict(int)
breed_totals = defaultdict(int)  # total per breed across all splits

for split in ["train", "val", "test"]:
    split_dir = os.path.join(PROCESSED_DIR, split)
    if not os.path.exists(split_dir):
        continue
    
    for breed in os.listdir(split_dir):
        breed_path = os.path.join(split_dir, breed)
        if not os.path.isdir(breed_path):
            continue
        
        count = len([f for f in os.listdir(breed_path) if os.path.isfile(os.path.join(breed_path, f))])
        image_counts[split][breed] = count
        total_counts[split] += count
        breed_totals[breed] += count  # add to breed total

# Print detailed report
print("\n📊 Processed Dataset Image Counts (Breed-wise & Split-wise):\n")
for split in ["train", "val", "test"]:
    print(f"--- {split.upper()} (Total: {total_counts[split]} images) ---")
    for breed, count in sorted(image_counts[split].items()):
        print(f"{breed}: {count} images")
    print()

# Print total per breed across all splits
print("\n📊 Total Images per Breed (All Splits Combined):\n")
for breed, count in sorted(breed_totals.items()):
    print(f"{breed}: {count} images")

# Calculate grand total
grand_total = sum(breed_totals.values())
print(f"\n🌟 GRAND TOTAL IMAGES IN PROCESSED DATASET: {grand_total}")
