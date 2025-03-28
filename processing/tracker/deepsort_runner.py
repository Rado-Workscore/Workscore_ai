import os
import json
from processing.tracker.deepsort_wrapper import DeepSortTracker
from processing.yolo.yolo_runner import run_yolo_on_frames

def run_tracking_on_video(warehouse_id, camera_id, video_id):
    # ⛓️ Ուղիներ
    frames_dir = f"data/frames/{warehouse_id}/{camera_id}/{video_id}"
    cache_dir = f"data/cache/{warehouse_id}/{camera_id}"
    os.makedirs(cache_dir, exist_ok=True)

    # 📥 YOLO detections
    yolo_results = run_yolo_on_frames(frames_dir)

    # 🔄 Initialize DeepSORT
    tracker = DeepSortTracker(warehouse_id)

    all_tracking = []

    for frame_idx, result in enumerate(yolo_results):
        boxes = result.boxes
        if boxes is None or boxes.xyxy is None:
            continue

        dets = []
        for i in range(len(boxes)):
            xyxy = boxes.xyxy[i].tolist()
            conf = float(boxes.conf[i])
            cls = int(boxes.cls[i])
            dets.append({
                "bbox": xyxy,
                "confidence": conf,
                "class": cls
            })

        # ➕ Tracking
        tracks = tracker.update_tracks(dets, frame_idx=frame_idx)

        for track in tracks:
            all_tracking.append({
                "frame": frame_idx,
                "track_id": track.track_id,
                "bbox": track.bbox
            })

    # 💾 Պահել tracking արդյունքը JSON ֆայլում
    output_path = os.path.join(cache_dir, f"{video_id}_tracking.json")
    with open(output_path, "w") as f:
        json.dump(all_tracking, f, indent=2)

    print(f"✅ Tracking արդյունքը պահվեց՝ {output_path}")

    # Հաշվել քանի unique մարդ է track արվել
    unique_ids = set([track["track_id"] for track in all_tracking])
    print(f"👤 Հետեւվել է {len(unique_ids)} տարբեր track_id (մարդու)։")

