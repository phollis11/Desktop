import os
import json

# ===============================
# CONFIG
# ===============================
SCRYFALL_JSONL = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\data\raw\scryfall_bulk.jsonl"
IMAGE_DIR = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\data\images"
OUTPUT_JSONL = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\data\processed\mtg_pairs.jsonl"

os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)

# ===============================
# BUILD PAIRS
# ===============================
written = 0
skipped = 0

with open(SCRYFALL_JSONL, "r", encoding="utf-8") as infile, \
     open(OUTPUT_JSONL, "w", encoding="utf-8") as outfile:

    for line in infile:
        line = line.strip()
        if not line:
            continue

        try:
            card = json.loads(line)
        except json.JSONDecodeError:
            skipped += 1
            continue

        oracle_id = card.get("oracle_id")
        name = card.get("name")
        type_line = card.get("type_line")
        oracle_text = card.get("oracle_text", "")

        if not oracle_id or not name or not type_line:
            skipped += 1
            continue

        image_path = os.path.join(IMAGE_DIR, f"{oracle_id}.jpg")

        # Only include cards with downloaded images
        if not os.path.exists(image_path):
            skipped += 1
            continue

        pair = {
            "oracle_id": oracle_id,
            "name": name,
            "type_line": type_line,
            "oracle_text": oracle_text,
            "image_path": image_path
        }

        outfile.write(json.dumps(pair, ensure_ascii=False) + "\n")
        written += 1

print(f"Done!")
print(f"Pairs written: {written}")
print(f"Cards skipped: {skipped}")
print(f"Output file: {OUTPUT_JSONL}")
