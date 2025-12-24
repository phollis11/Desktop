import os
import json
import torch
from PIL import Image
from tqdm import tqdm
import open_clip

# ===============================
# CONFIG
# ===============================
JSONL_FILE = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\data\processed\mtg_pairs.jsonl"
IMAGE_BASE_DIR = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\data\images"
EMBED_FILE = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\model\all_embeddings.pt"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

BATCH_SIZE = 32  # adjust based on memory

# ===============================
# LOAD CLIP MODEL
# ===============================
model_name = "ViT-B-32"
pretrained = "openai"
model, _, preprocess = open_clip.create_model_and_transforms(model_name, pretrained=pretrained)
tokenizer = open_clip.get_tokenizer(model_name)
model.to(DEVICE)
model.eval()

# ===============================
# READ DATA
# ===============================
cards = []
with open(JSONL_FILE, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        img_path = os.path.join(IMAGE_BASE_DIR, f"{data['oracle_id']}.jpg")
        if os.path.exists(img_path):
            cards.append({
                "oracle_id": data["oracle_id"],
                "name": data["name"],
                "oracle_text": data.get("oracle_text", ""),
                "type_line": data.get("type_line", ""),
                "img_path": img_path
            })

print(f"Total cards with images: {len(cards)}")

# ===============================
# EMBED TEXT
# ===============================
text_embeddings = {}
for i in tqdm(range(0, len(cards), BATCH_SIZE), desc="Embedding text"):
    batch = cards[i:i+BATCH_SIZE]
    texts = [f"{c['name']} {c['type_line']} {c['oracle_text']}" for c in batch]
    tokens = tokenizer(texts).to(DEVICE)
    with torch.no_grad():
        embeds = model.encode_text(tokens)
        embeds = embeds / embeds.norm(dim=-1, keepdim=True)
    for idx, c in enumerate(batch):
        text_embeddings[c["oracle_id"]] = embeds[idx].cpu()

# ===============================
# EMBED IMAGES
# ===============================
image_embeddings = {}
for i in tqdm(range(0, len(cards), BATCH_SIZE), desc="Embedding images"):
    batch = cards[i:i+BATCH_SIZE]
    images = [preprocess(Image.open(c["img_path"]).convert("RGB")).to(DEVICE) for c in batch]
    images = torch.stack(images)
    with torch.no_grad():
        embeds = model.encode_image(images)
        embeds = embeds / embeds.norm(dim=-1, keepdim=True)
    for idx, c in enumerate(batch):
        image_embeddings[c["oracle_id"]] = embeds[idx].cpu()

# ===============================
# SAVE EVERYTHING
# ===============================
torch.save({
    "cards": cards,
    "text_embeddings": text_embeddings,
    "image_embeddings": image_embeddings
}, EMBED_FILE)

print(f"All embeddings saved to {EMBED_FILE}")
