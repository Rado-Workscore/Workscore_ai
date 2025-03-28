import os
import json
import cv2


def load_detections(detections_path):
    with open(detections_path, "r") as f:
        return json.load(f)


def crop_and_save(detections, frames_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for detection in detections:
        frame_name = detection["frame"]
        boxes = detection["boxes"]

        frame_path = os.path.join(frames_dir, frame_name)
        frame = cv2.imread(frame_path)

        if frame is None:
            print(f"⚠️ Չհաջողվեց կարդալ ֆրեյմը՝ {frame_path}")
            continue

        for idx, box in enumerate(boxes):
            xmin, ymin, xmax, ymax = map(int, box)
            crop = frame[ymin:ymax, xmin:xmax]

            crop_filename = f"{os.path.splitext(frame_name)[0]}_person{idx}.jpg"
            crop_path = os.path.join(output_dir, crop_filename)

            cv2.imwrite(crop_path, crop)

    print(f"✅ Cropping ավարտված է։ Կտրված պատկերը պահվել են՝ {output_dir}")


def main():
    detections_path = "data/cache/warehouse_1/new_video/detections.json"
    frames_dir = "data/frames/warehouse_001/new_video/processed_1"
    output_dir = "data/crops/warehouse_001/new_video/"

    detections = load_detections(detections_path)
    crop_and_save(detections, frames_dir, output_dir)


if __name__ == "__main__":
    main()
