# tracking_runner.py
import sys
import os
import json  # ← ճիշտ տեղում է հիմա
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from processing.yolo.yolo_runner import run_yolo_on_frames


def run_tracking(detections):
    """
    Կատարել tracking YOLO detections-ի հիման վրա։
    Այս պահին վերադարձնում է placeholder tracking արդյունքներ։
    """
    tracks = []

    for i, detection in enumerate(detections):
        boxes = detection.get("boxes", [])
        track_info = [
            {
                "track_id": idx,
                "bbox": box
            }
            for idx, box in enumerate(boxes)
        ]

        tracks.append({
            "frame_id": i,
            "tracks": track_info
        })

    return tracks

def save_detections(detections, save_path="data/cache/warehouse_1/new_video/detections.json"):
    """Պահել YOLO-ի արդյունքը .json ֆայլում"""
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "w") as f:
            json.dump(detections, f, indent=2)

        print(f"✅ YOLO արդյունքը պահպանվեց՝ {save_path}")
    except Exception as e:
        print(f"⚠️ Ошибка при сохранении файла: {e}")

def main():
    frames_dir = "data/frames/warehouse_001/new_video/processed_1"
    print("🔍 Looking for frames in:", os.path.abspath(frames_dir))
    print("📁 Exists:", os.path.exists(frames_dir))
    detections = run_yolo_on_frames(frames_dir, warehouse_id="warehouse_001", device="cpu")
    save_detections(detections)  # Սա միայն պահում է YOLO-ի արդյունքները
    


if __name__ == "__main__":
    main()
