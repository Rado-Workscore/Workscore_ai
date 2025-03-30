import os
import json
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort

class DeepSortTracker:
    def __init__(self, warehouse_id, frames_dir):
        self.frames_dir = frames_dir

        config_path = f"data/warehouses/{warehouse_id}/config/deepsort.json"
        with open(config_path, "r") as f:
            cfg = json.load(f)

        self.tracker = DeepSort(
            max_age=cfg["max_age"],
            n_init=cfg["n_init"],
            max_cosine_distance=cfg["max_cosine_distance"],
            nn_budget=cfg["nn_budget"],
            embedder=cfg["embedding_model"],
            half=True,
            bgr=True,
            embedder_gpu=False  # CPU
        )

    def update_tracks(self, detections, frame_idx, frame_name):
        dets = []
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            w, h = x2 - x1, y2 - y1
            dets.append(([x1, y1, w, h], det["confidence"], det["class"]))

        # ✅ Բեռնել ֆրեյմ նկարը
        frame_path = os.path.join(self.frames_dir, frame_name)
        frame = cv2.imread(frame_path)

        tracks = self.tracker.update_tracks(dets, frame=frame)

        results = []
        for track in tracks:
            if not track.is_confirmed():
                continue
            results.append({
                "track_id": track.track_id,
                "bbox": track.to_ltrb().tolist()   # ✅ Վերածում ենք list-ի, որ json-ը կարողանա պահել
            })


        return results
