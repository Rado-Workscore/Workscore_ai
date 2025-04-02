import os
import json
import shutil
from collections import defaultdict

# Tracking ֆայլի տեղը
TRACKING_JSON = "data/cache/warehouse_1/new_video/processed_1_tracking.json"
# Crop ֆայլերի տեղը
CROP_DIR = "data/crops/warehouse_1/new_video"
# Output՝ ըստ ID-ների դասավորված
OUTPUT_DIR = "tests/reid_samples"

# Բեռնենք tracking տվյալները
with open(TRACKING_JSON, "r") as f:
    tracking_data = json.load(f)

# Պատրաստենք dict՝ track_id → list of crop paths
track_crops = defaultdict(list)

for item in tracking_data:
    frame_name = item["frame"]             # օրինակ՝ frame_0183.jpg
    track_id = str(item["track_id"])       # օրինակ՝ 13
    crop_filename = f"{frame_name.replace('.jpg', '')}_person{track_id}.jpg"
    crop_path = os.path.join(CROP_DIR, crop_filename)

    if os.path.exists(crop_path):
        track_crops[track_id].append(crop_path)
    else:
        print(f"❌ Չկա crop ֆայլ՝ {crop_path}")

# Տեղափոխենք ըստ ID-ների
for track_id, paths in track_crops.items():
    dest_dir = os.path.join(OUTPUT_DIR, track_id)
    os.makedirs(dest_dir, exist_ok=True)

    for src_path in paths:
        fname = os.path.basename(src_path)
        dst_path = os.path.join(dest_dir, fname)
        shutil.copy2(src_path, dst_path)

print("✅ Crop-երը բաժանվեցին ըստ track ID-ների։")
