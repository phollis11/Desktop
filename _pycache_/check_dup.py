import os
from collections import Counter

IMG_DIR = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\data\images"

# Get all filenames without extension (oracle_ids)
oracle_ids = [os.path.splitext(f)[0] for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]

total_images = len(oracle_ids)
print(f"Total images in folder: {total_images}")


# Count occurrences
counts = Counter(oracle_ids)


# Find duplicates
duplicates = [oid for oid, c in counts.items() if c > 1]

if duplicates:
    print(f"Found {len(duplicates)} duplicated oracle_ids:")
    for oid in duplicates:
        print(oid)
else:
    print("No duplicate oracle_ids found.")
