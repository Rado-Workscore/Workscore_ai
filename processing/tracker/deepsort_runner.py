import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import os
import json
from processing.tracker.deepsort_wrapper import DeepSortTracker

def run_tracking_from_detections(detections_path, frames_dir, warehouse_id, output_path):
    # 📥 Բեռնում ենք YOLO detect արված տվյալները
    with open(detections_path, "r") as f:
        detections = json.load(f)

    # 🔄 Initialize DeepSORT tracker
    tracker = DeepSortTracker(warehouse_id)
    all_tracks = []

    for frame_idx, detection in enumerate(detections):
        boxes = detection.get("boxes", [])

        dets = []
        for box in boxes:
            x1, y1, x2, y2 = box
            w, h = x2 - x1, y2 - y1
            dets.append({
                "bbox": [x1, y1, x2, y2],
                "confidence": 0.9,
                "class": 0
            })

        # 🧍 Թարմացնում ենք tracking
        tracks = tracker.update_tracks(dets, frame_idx=frame_idx)

        for track in tracks:
            all_tracks.append({
                "frame": detection["frame"],
                "track_id": track["track_id"],
                "bbox": track["bbox"]
            })

    # 💾 Պահում ենք tracking արդյունքը
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(all_tracks, f, indent=2)

    print(f"✅ Tracking արդյունքը պահպանվեց՝ {output_path}")
    unique_ids = set(t["track_id"] for t in all_tracks)
    print(f"👤 Հետեւվել է {len(unique_ids)} տարբեր track_id։")


def main():
    # 🔧 Կոնֆիգուրացիա
    warehouse_id = "warehouse_001"
    camera_id = "new_video"
    video_id = "processed_1"

    detections_path = f"data/cache/{warehouse_id}/{camera_id}/detections.json"
    frames_dir = f"data/frames/{warehouse_id}/{camera_id}/{video_id}"
    output_path = f"data/cache/{warehouse_id}/{camera_id}/{video_id}_tracking.json"

    run_tracking_from_detections(detections_path, frames_dir, warehouse_id, output_path)

if __name__ == "__main__":
    main()
