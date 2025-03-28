import cv2
import os
from processing.preprocessing.frame_preprocessor import preprocess_frame


def cut_video_into_frames(cap, output_dir, rotation=0):
    os.makedirs(output_dir, exist_ok=True)
    frame_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Ավտոմատ պտտում ըստ մետադատայի
        if rotation == 90:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif rotation == 180:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        elif rotation == 270:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        frame_filename = f"frame_{frame_count:04d}.jpg"
        # Նախամշակում ֆրեյմի վրա
        processed_frame = preprocess_frame(frame)

        # Պահել `processed/` ենթապանակում
        processed_dir = os.path.join(output_dir, "processed")
        os.makedirs(processed_dir, exist_ok=True)

        frame_path = os.path.join(processed_dir, frame_filename)
        cv2.imwrite(frame_path, processed_frame)

        
        frame_count += 1

    cap.release()
    print(f"✅ Վիդեոն կտրվեց {frame_count} ֆրեյմի։")
