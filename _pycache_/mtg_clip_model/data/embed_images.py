import os
import torch
from PIL import Image
from tqdm import tqdm
import open_clip

# ===============================
# CONFIG
# ===============================
IMG_DIR = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\data\images"
EMBED_DIR = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\model"
EMBED_FILE = "image_embeddings.pt"
BATCH_SIZE = 32
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ===============================
# SETUP
# ===============================
os.makedirs(EMBED_DIR, exist_ok=True)

# Load CLIP model
model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
model.to(DEVICE)
model.eval()

# ===============================
# LOAD IMAGES
# ===============================
img_files = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
total_images = len(img_files)
print(f"Total images: {total_images}")

# ===============================
# EMBEDDING LOOP
# ===============================
all_embeddings = {}

for i in tqdm(range(0, total_images, BATCH_SIZE), desc="Embedding images"):
    batch_files = img_files[i:i+BATCH_SIZE]
    images = []
    ids = []

    for img_file in batch_files:
        try:
            img_path = os.path.join(IMG_DIR, img_file)
            img = Image.open(img_path).convert("RGB")
            images.append(preprocess(img))
            ids.append(img_file.replace(".jpg",""))
        except Exception as e:
            print(f"Failed to load {img_file}: {e}")

    if not images:
        continue

    images_tensor = torch.stack(images).to(DEVICE)
    with torch.no_grad():
        embeds = model.encode_image(images_tensor)

    embeds = embeds.cpu()
    for oracle_id, embed in zip(ids, embeds):
        all_embeddings[oracle_id] = embed

# ===============================
# SAVE EMBEDDINGS
# ===============================
torch.save(all_embeddings, os.path.join(EMBED_DIR, EMBED_FILE))
print(f"Saved all embeddings to {os.path.join(EMBED_DIR, EMBED_FILE)}")
