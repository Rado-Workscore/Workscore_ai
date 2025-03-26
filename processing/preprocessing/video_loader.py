import cv2

def load_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception(f"Չհաջողվեց բացել վիդեոն՝ {video_path}")
    return cap
