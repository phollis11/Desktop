import json
import torch
import open_clip
from tqdm import tqdm

# ------------------------
# CONFIG
# ------------------------
JSONL_PATH = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\data\processed\mtg_pairs.jsonl"
OUT_PATH = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\model\text_embeddings.pt"
BATCH_SIZE = 32   # 16–64 safe on CPU

device = "cuda" if torch.cuda.is_available() else "cpu"

# ------------------------
# MODEL
# ------------------------
model, _, _ = open_clip.create_model_and_transforms(
    "ViT-B-32", pretrained="openai"
)
tokenizer = open_clip.get_tokenizer("ViT-B-32")
model = model.to(device).eval()

# ------------------------
# LOAD TEXTS
# ------------------------
texts = []
oracle_ids = []

with open(JSONL_PATH, "r", encoding="utf-8") as f:
    for line in f:
        card = json.loads(line)
        text = f"{card['name']}. {card['type_line']}. {card['oracle_text']}"
        texts.append(text)
        oracle_ids.append(card["oracle_id"])

        print(text + " : " + card["oracle_id"])

# ------------------------
# EMBED IN BATCHES
# ------------------------
all_embeddings = []

with torch.no_grad():
    for i in tqdm(range(0, len(texts), BATCH_SIZE), desc="Embedding texts"):
        batch_texts = texts[i:i + BATCH_SIZE]
        tokens = tokenizer(batch_texts).to(device)

        embeds = model.encode_text(tokens)
        embeds = embeds / embeds.norm(dim=-1, keepdim=True)

        all_embeddings.append(embeds.cpu())

text_embeddings = torch.cat(all_embeddings)

# ------------------------
# SAVE
# ------------------------
torch.save(
    {
        "embeddings": text_embeddings,
        "oracle_ids": oracle_ids
    },
    OUT_PATH
)

print(f"Saved {len(text_embeddings)} text embeddings → {OUT_PATH}")
