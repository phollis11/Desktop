import requests
import json
import sys

# ----------------------------
# Configuration
# ----------------------------
BULK_API_URL = "https://api.scryfall.com/bulk-data"
OUTPUT_FILE = "scryfall_bulk.jsonl"

HEADERS = {
    "User-Agent": "MTG-CLIP-Research/0.1 (contact: phollis0216@gmail.com",
    "Accept": "application/json"
}

# ----------------------------
# Fetch bulk metadata
# ----------------------------
print("Fetching bulk metadata...")
resp = requests.get(BULK_API_URL, headers=HEADERS)
resp.raise_for_status()

bulk_data = resp.json()["data"]

# Find the default_cards dataset
bulk_entry = next(
    item for item in bulk_data
    if item["type"] == "default_cards"
)

download_url = bulk_entry["download_uri"]
print(f"Downloading bulk cards from:\n{download_url}")

# ----------------------------
# Download bulk cards
# ----------------------------
resp = requests.get(download_url, headers=HEADERS)
resp.raise_for_status()

cards = resp.json()  # large JSON array

print(f"Total cards received: {len(cards)}")

# ----------------------------
# Write JSON Lines file
# ----------------------------
print(f"Writing to {OUTPUT_FILE} ...")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for card in cards:
        f.write(json.dumps(card, ensure_ascii=False) + "\n")

print("Done.")
print(f"Saved {len(cards)} cards to {OUTPUT_FILE}")
