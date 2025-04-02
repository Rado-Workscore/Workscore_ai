import os
import json
import shutil
from collections import defaultdict

def iou(boxA, boxB):
    # Հաշվում է Intersection over Union երկու բոքսի միջև
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)

    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    union = boxAArea + boxBArea - interArea
    return interArea / union if union != 0 else 0

# Ուղիներ
CROP_DIR = "data/crops/warehouse_1/new_video"
DETECTIONS_PATH = "data/cache/warehouse_1/new_video/detections.json"
TRACKING_PATH = "data/cache/warehouse_1/new_video/processed_1_tracking.json"
OUTPUT_DIR = "tests/reid_samples"

# Բեռնում ենք YOLO detections
with open(DETECTIONS_PATH, "r") as f:
    yolo_data = {item["frame"]: item["boxes"] for item in json.load(f)}

# Բեռնում ենք DeepSORT tracking
with open(TRACKING_PATH, "r") as f:
    tracking_data = json.load(f)

# Crop-երը կապում ենք tracking ID-ներին
for item in tracking_data:
    frame = item["frame"]
    track_id = str(item["track_id"])
    trk_box = item["bbox"]  # [x1, y1, x2, y2]

    best_iou = 0
    best_idx = None

    for idx, yolo_box in enumerate(yolo_data.get(frame, [])):
        score = iou(trk_box, yolo_box)
        if score > best_iou:
            best_iou = score
            best_idx = idx

    if best_idx is not None:
        crop_filename = f"{frame.replace('.jpg', '')}_person{best_idx}.jpg"
        crop_path = os.path.join(CROP_DIR, crop_filename)

        if os.path.exists(crop_path):
            dest_dir = os.path.join(OUTPUT_DIR, f"id_{track_id}")
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(crop_path, os.path.join(dest_dir, crop_filename))
        else:
            print(f"⚠️ Չգտնվեց crop՝ {crop_filename}")
    else:
        print(f"❌ bbox_index չհաջողվեց գտնել՝ {frame}, ID={track_id}")
