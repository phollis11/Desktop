import torch
from PIL import Image
import open_clip
import os

# ===============================
# CONFIG
# ===============================
EMBED_FILE = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\model\all_embeddings.pt"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "ViT-B-32"
PRETRAINED = "openai"

# ===============================
# LOAD MODEL AND EMBEDDINGS
# ===============================
model, _, preprocess = open_clip.create_model_and_transforms(MODEL_NAME, pretrained=PRETRAINED)
model.to(DEVICE)
model.eval()
tokenizer = open_clip.get_tokenizer(MODEL_NAME)

data = torch.load(EMBED_FILE)
# Convert cards list → dict keyed by oracle_id
cards = {c["oracle_id"]: c for c in data["cards"]}

text_embeddings = data["text_embeddings"]
image_embeddings = data["image_embeddings"]

# Convert embeddings to a tensor for fast search
image_ids = list(image_embeddings.keys())
image_tensor = torch.stack([image_embeddings[k] for k in image_ids]).to(DEVICE)
text_ids = list(text_embeddings.keys())
text_tensor = torch.stack([text_embeddings[k] for k in text_ids]).to(DEVICE)

# ===============================
# HELPER FUNCTIONS
# ===============================
def find_similar_image(query_path, top_k=5):
    """Find the most similar cards for a query image"""
    img = preprocess(Image.open(query_path).convert("RGB")).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        q_embed = model.encode_image(img)
        q_embed /= q_embed.norm(dim=-1, keepdim=True)
        sims = q_embed @ image_tensor.T
        top_idx = sims[0].topk(top_k).indices.cpu().numpy()
    return [cards[image_ids[i]] for i in top_idx]

def find_similar_text(query_text, top_k=5):
    """Find the most similar cards for a query text"""
    tokens = tokenizer([query_text]).to(DEVICE)
    with torch.no_grad():
        q_embed = model.encode_text(tokens)
        q_embed /= q_embed.norm(dim=-1, keepdim=True)
        sims = q_embed @ text_tensor.T
        top_idx = sims[0].topk(top_k).indices.cpu().numpy()
    return [cards[text_ids[i]] for i in top_idx]

# ===============================
# EXAMPLE USAGE
# ===============================
if __name__ == "__main__":
    # Search by image
    query_image_path = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\card_tracking\cropped_cards\card_0.jpg"
    top_cards = find_similar_image(query_image_path)
    print("Top matches for image:")
    for c in top_cards:
        print(f"{c['name']} | {c['type_line']} | {c['oracle_id']}")

    # Search by text
    query_text = "Lightning Bolt deals 3 damage to any target."
    top_cards = find_similar_text(query_text)
    print("\nTop matches for text:")
    for c in top_cards:
        print(f"{c['name']} | {c['type_line']} | {c['oracle_id']}")
