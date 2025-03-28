import os
from processing.preprocessing.format_converter import convert_to_mp4
from processing.preprocessing.video_loader import load_video
from processing.preprocessing.cutter import cut_video_into_frames
from processing.preprocessing.rotation_helper import get_rotation_angle

WAREHOUSE_ID = "warehouse_001"
VIDEOS_DIR = f"data/videos/{WAREHOUSE_ID}"
FRAMES_DIR = f"data/frames/{WAREHOUSE_ID}"

all_files = []
for root, dirs, files in os.walk(VIDEOS_DIR):
    for f in files:
        if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
            full_path = os.path.join(root, f)
            all_files.append(full_path)

# Նախ վերափոխել բոլոր .MOV, .avi, .mkv ֆայլերը mp4 ձևաչափի
converted = []
for f in all_files:
    input_path = f
    mp4_path = convert_to_mp4(input_path)
    if mp4_path:
        converted.append(mp4_path)

# Վերջնական mp4 ֆայլերի ցանկ
video_files = [f for f in converted if f.endswith(".mp4")]

print(f"\n📂 Գտնվեցին {len(video_files)} վիդեոներ՝ {VIDEOS_DIR} պանակում\n")

for video_file in video_files:
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    frame_output_dir = os.path.join(FRAMES_DIR, video_name)

    if os.path.exists(frame_output_dir):
        print(f"⏭️ Անցնում ենք {video_file} – արդեն վերլուծված է։")
        continue

    print(f"🔄 Վերլուծում ենք {video_file} ...")
    print(f"📍 Տեսանյութի ուղին: {video_file}")
    print(f"📁 Ֆրեյմերը կպահվեն այստեղ: {frame_output_dir}")

    original_path = video_file
    video_path = convert_to_mp4(original_path)

    if not video_path:
        print(f"❌ Բաց թողնվեց {video_file} – չի հաջողվել mp4 դարձնել։")
        continue

    rotation = get_rotation_angle(video_path)
    print(f"↩️ Վիդեոն ունի {rotation}° պտտում։")

    cap = load_video(video_path)
    cut_video_into_frames(cap, frame_output_dir, rotation=rotation)



