import cv2
import os
import random

CARD_DIR = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\data\images"
BG_DIR = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\card_tracking\background_images"

IMG_OUT = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\card_tracking\cards_dataset\images\train"
LBL_OUT = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\card_tracking\cards_dataset\labels\train"

os.makedirs(IMG_OUT, exist_ok=True)
os.makedirs(LBL_OUT, exist_ok=True)

NUM_IMAGES = 1000

card_files = os.listdir(CARD_DIR)
bg_files = os.listdir(BG_DIR)

assert card_files, "No card images found"
assert bg_files, "No background images found"

for i in range(NUM_IMAGES):

    img_name = f"img_{i}.jpg"
    bg = cv2.imread(os.path.join(BG_DIR, random.choice(bg_files)))
    h, w, _ = bg.shape

    place_card = random.random() < 0.6

    if place_card:
        card = cv2.imread(
            os.path.join(CARD_DIR, random.choice(card_files)),
            cv2.IMREAD_UNCHANGED
        )

        # Handle PNG alpha
        if card.shape[2] == 4:
            alpha = card[:, :, 3] / 255.0
            card = card[:, :, :3]
        else:
            alpha = None

        scale = random.uniform(0.3, 0.7)
        card = cv2.resize(card, None, fx=scale, fy=scale)
        ch, cw, _ = card.shape

        if cw >= w or ch >= h:
            scale = min(w / cw, h / ch) * 0.9
            card = cv2.resize(card, None, fx=scale, fy=scale)
            ch, cw, _ = card.shape

        x = random.randint(0, w - cw)
        y = random.randint(0, h - ch)

        roi = bg[y:y+ch, x:x+cw]

        if alpha is not None:
            alpha = cv2.resize(alpha, (cw, ch))
            for c in range(3):
                roi[:, :, c] = roi[:, :, c] * (1 - alpha) + card[:, :, c] * alpha
        else:
            roi[:] = card

        bg[y:y+ch, x:x+cw] = roi

        # Save label ONLY when card exists
        x_center = (x + cw / 2) / w
        y_center = (y + ch / 2) / h
        bw = cw / w
        bh = ch / h

        with open(os.path.join(LBL_OUT, img_name.replace(".jpg", ".txt")), "w") as f:
            f.write(f"0 {x_center} {y_center} {bw} {bh}")

    # Save image (both cases)
    cv2.imwrite(os.path.join(IMG_OUT, img_name), bg)
