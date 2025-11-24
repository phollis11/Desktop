from ultralytics import YOLO
import cv2


model = YOLO(r"C:\Users\pholl\OneDrive\Desktop\_pycache_\CIS 314\yolov8n-face.pt")   
source = r"C:\Users\pholl\OneDrive\Pictures\Camera Roll\WIN_20251109_14_19_34_Pro.mp4"
results = model(source)

height, width, _ = results[0].orig_img.shape
out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

for frame_result in results:
    annotated_frame = frame_result.plot()
    out.write(annotated_frame)

out.release()
cv2.destroyAllWindows()
