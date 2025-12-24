from ultralytics import YOLO
import torch

torch.set_num_threads(12)
torch.set_num_interop_threads(2)

model = YOLO("yolov8n.pt")

model.train(
    data=r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\card_tracking\data.yaml",
    epochs=40,
    imgsz=640,
    batch=16,
    workers=12,
    device="cpu"
)



"""
print(result.boxes.xyxy) # Bounding box coordinates
print(result.boxes.conf) # Confidence scores
print(result.names) # Detected class names

for frame in frames:
    if result.names == card and result.boxes.conf > 50:
        break
"""