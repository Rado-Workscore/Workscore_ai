import os
import cv2
import torch
import json
from ultralytics import YOLO


def load_yolo_config(warehouse_id):
    config_path = f"data/warehouses/{warehouse_id}/config/yolo.json"
    with open(config_path, "r") as f:
        return json.load(f)


def run_yolo_on_frames(frames_dir, warehouse_id="default_warehouse", device="cpu"):
    import os
    os.environ["CUDA_VISIBLE_DEVICES"] = "" if device == "cpu" else device


    # 📥 Բեռնել YOLO պարամետրերը տվյալ պահեստի համար
    config = load_yolo_config(warehouse_id)

    model_path = config.get("model", "yolov8m.pt")
    conf = config.get("conf", 0.25)
    iou = config.get("iou", 0.45)
    classes = config.get("classes", [0])
    imgsz = config.get("imgsz", 640)
    device = config.get("device", "cpu")

    # 🧠 Բեռնել մոդելը
    model = YOLO(model_path)
    


    # 📁 Բոլոր ֆրեյմերի ուղիները
    frame_files = sorted([
        os.path.join(frames_dir, f)
        for f in os.listdir(frames_dir)
        if f.endswith(".jpg") or f.endswith(".png")
    ])

    results = []
    for frame_path in frame_files:
        frame = cv2.imread(frame_path)
        if frame is None:
            print(f"⚠️ Չհաջողվեց կարդալ ֆրեյմը՝ {frame_path}")
            continue

        # 🔍 YOLO դետեկցիա
        result = model.predict(
            source=frame,
            conf=conf,
            iou=iou,
            classes=classes,
            imgsz=imgsz,
            device="cpu",
            verbose=False
        )[0]  # Վերցնում ենք միայն առաջին արդյունքը

        boxes = result.boxes.xyxy.cpu().numpy().tolist()
        results.append({
        "frame": os.path.basename(frame_path),  # frame-ի անունը
        "boxes": boxes
})


    print(f"✅ YOLO վերլուծությունն ավարտվեց՝ {len(results)} ֆրեյմի վրա։")
    return results