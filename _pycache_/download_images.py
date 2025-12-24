import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===============================
# CONFIGURATION
# ===============================
JSONL_FILE = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\data\raw\scryfall_bulk.jsonl"  # path to your bulk JSONL
IMG_FOLDER = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\data\images"# folder where images will be saved
HEADERS = {
    "User-Agent": "MTG-BulkImageDownloader/1.0",
    "Accept": "application/json"
}
MAX_WORKERS = 8  # number of parallel downloads

# ===============================
# SETUP
# ===============================
os.makedirs(IMG_FOLDER, exist_ok=True)

# Helper to extract the URL and local filename
def get_image_info(card):
    # Only download if this card has normal image
    uris = card.get("image_uris")
    if not uris:
        return None

    url = uris.get("normal")
    if not url:
        return None

    # Use oracle_id (unique across printings) as filename
    oracle_id = card.get("oracle_id")
    if not oracle_id:
        return None

    filename = f"{oracle_id}.jpg"
    return url, os.path.join(IMG_FOLDER, filename)

# Download a single image
def download_image(task):
    url, path = task
    try:
        if os.path.exists(path):
            return f"Exists: {path}"
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
        return f"Downloaded: {path}"
    except Exception as e:
        return f"Failed ({e}): {url}"

# Load cards and build download list
tasks = []
with open(JSONL_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        card = json.loads(line)
        info = get_image_info(card)
        if info:
            tasks.append(info)

print(f"Total images to fetch: {len(tasks)}")

# ===============================
# MULTITHREADED DOWNLOAD
# ===============================
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(download_image, t) for t in tasks]
    for future in as_completed(futures):
        print(future.result())
