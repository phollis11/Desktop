import os
import cv2
import numpy as np
from collections import defaultdict
from ultralytics import YOLO
from PIL import Image, ImageOps

# -------------------------------
# CONFIG
# -------------------------------
MODEL_PATH = r"C:\Users\pholl\OneDrive\Desktop\runs\detect\train10\weights\best.pt"
SOURCE_PATH = r"C:\Users\pholl\OneDrive\Pictures\Camera Roll\WIN_20251224_10_58_08_Pro.mp4"
OUT_DIR = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\card_tracking\cropped_cards"

MAX_DIM = 1600
CONF_THRESH = .75

track_history = defaultdict(list)

os.makedirs(OUT_DIR, exist_ok=True)

# -------------------------------
# LOAD MODEL
# -------------------------------
model = YOLO(MODEL_PATH)

# -------------------------------
# LOAD IMAGE (FIX EXIF ORIENTATION)
# -------------------------------
def load_image_correct_orientation(path):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)     # <<< FIX PHONE ROTATION
    img = img.convert("RGB")
    return np.array(img)[:, :, ::-1]       # RGB → BGR for OpenCV


if SOURCE_PATH.lower().endswith((".jpg", ".png", ".jpeg")):
    frame = load_image_correct_orientation(SOURCE_PATH)

    # -------------------------------
    # OPTIONAL: LIMIT HUGE PHONE IMAGES
    # -------------------------------
    h, w = frame.shape[:2]
    scale = MAX_DIM / max(h, w)
    if scale < 1:
        frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

    # -------------------------------
    # RUN YOLO (NO TRACKING NEEDED)
    # -------------------------------
    results = model(frame, conf=0.5)
    result = results[0]

    annotated = result.plot()
    orig = result.orig_img
    h, w = orig.shape[:2]

    # -------------------------------
    # SAVE CROPPED CARDS
    # -------------------------------
    for i, box in enumerate(result.boxes.xyxy.cpu().numpy()):
        x1, y1, x2, y2 = map(int, box)

        # Clamp bounds
        x1 = max(0, min(x1, w))
        x2 = max(0, min(x2, w))
        y1 = max(0, min(y1, h))
        y2 = max(0, min(y2, h))

        crop = orig[y1:y2, x1:x2]

        if crop.size == 0:
            continue

        out_path = os.path.join(OUT_DIR, f"card_{i}.jpg")
        cv2.imwrite(out_path, crop)

    print(f"✅ Saved {len(result.boxes)} cropped cards to:")
    print(OUT_DIR)

    # -------------------------------
    # DISPLAY RESULT
    # -------------------------------
    cv2.imshow("YOLO Card Detection", annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# -------------------------------
# VIDEO CASE
# -------------------------------
else:
    cap = cv2.VideoCapture(SOURCE_PATH)

    saved = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize very large frames (phone videos)
        h, w = frame.shape[:2]
        scale = MAX_DIM / max(h, w)
        if scale < 1:
            frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

        # Run detection
        results = model(frame, conf=CONF_THRESH)
        result = results[0]

        annotated = result.plot()
        cv2.imshow("YOLO Card Detection", annotated)

        # If detection meets confidence threshold
        if result.boxes is not None and len(result.boxes) > 0:
            orig = result.orig_img
            h, w = orig.shape[:2]

            for i, box in enumerate(result.boxes.xyxy.cpu().numpy()):
                conf = float(result.boxes.conf[i])

                if conf < CONF_THRESH:
                    continue

                x1, y1, x2, y2 = map(int, box)

                # Clamp
                x1 = max(0, min(x1, w))
                x2 = max(0, min(x2, w))
                y1 = max(0, min(y1, h))
                y2 = max(0, min(y2, h))

                crop = orig[y1:y2, x1:x2]
                if crop.size == 0:
                    continue

                out_path = os.path.join(OUT_DIR, f"card_conf_{conf:.2f}.jpg")
                cv2.imwrite(out_path, crop)

            print("✅ Card detected with confidence ≥ 50%. Cropped & saved.")
            print("Press Q to exit.")

            # 🔴 STOP VIDEO — HOLD FRAME
            cv2.imshow("YOLO Card Detection", annotated)
            cv2.waitKey(0)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            break

        # Normal quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
