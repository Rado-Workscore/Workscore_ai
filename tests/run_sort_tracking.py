import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import numpy as np
from sort import Sort

# 📂 YOLO detections
detections_path = "data/cache/warehouse_1/new_video/detections.json"
with open(detections_path, "r") as f:
    detections = json.load(f)

# ▶️ Initialize SORT with new settings
tracker = Sort(
    max_age=300,     # պահել մինչև 60 ֆրեյմ
    min_hits=3,     # հաստատել track հենց առաջինից
    iou_threshold=0.3
)

tracked_results = []

for item in detections:
    frame = item["frame"]
    boxes = item.get("boxes", [])
    np_boxes = np.array([[*box, 0.9] for box in boxes])  # bbox + confidence

    tracked = tracker.update(np_boxes)

    for trk in tracked:
        x1, y1, x2, y2, track_id = trk
        tracked_results.append({
            "frame": frame,
            "track_id": int(track_id),
            "bbox": [float(x1), float(y1), float(x2), float(y2)]
        })

# 💾 Պահել արդյունքը
output_path = "data/cache/warehouse_1/new_video/sort_tracking.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as f:
    json.dump(tracked_results, f, indent=2)

# 📊 Վերլուծություն
unique_ids = set(t["track_id"] for t in tracked_results)

print(f"✅ SORT tracking ավարտվեց։")
print(f"📁 Արդյունքը պահպանվել է՝ {output_path}")
print(f"📦 Մուտքային ֆրեյմեր՝ {len(detections)}")
print(f"👤 Unique ID-ներ (մարդիկ)՝ {len(unique_ids)}")
