import os
from processing.preprocessing.format_converter import convert_to_mp4


WAREHOUSE_ID = "warehouse_001"
VIDEOS_DIR = f"data/videos/{WAREHOUSE_ID}"
FRAMES_DIR = f"data/frames/{WAREHOUSE_ID}"

all_files = [
    f for f in os.listdir(VIDEOS_DIR)
    if os.path.isfile(os.path.join(VIDEOS_DIR, f))
]


# Նախ վերափոխել բոլոր .MOV, .avi, .mkv ֆայլերը mp4 ձևաչափի
converted = []
for f in all_files:
    input_path = os.path.join(VIDEOS_DIR, f)
    mp4_path = convert_to_mp4(input_path)
    if mp4_path:
        converted.append(os.path.basename(mp4_path))

# Վերջնական mp4 ֆայլերի ցանկ
video_files = [f for f in converted if f.endswith(".mp4")]


print(f"\n📂 Գտնվեցին {len(video_files)} վիդեոներ՝ {VIDEOS_DIR} պանակում\n")

for video_file in video_files:
    video_name = video_file.split(".")[0]
    frame_output_dir = os.path.join(FRAMES_DIR, video_name)

    if os.path.exists(frame_output_dir):
        print(f"⏭️ Անցնում ենք {video_file} – արդեն վերլուծված է։")
        continue

    print(f"🔄 Վերլուծում ենք {video_file} ...")
    print(f"📍 Տեսանյութի ուղին: {os.path.join(VIDEOS_DIR, video_file)}")
    print(f"📁 Ֆրեյմերը կպահվեն այստեղ: {frame_output_dir}")

    from processing.preprocessing.video_loader import load_video
    from processing.preprocessing.cutter import cut_video_into_frames
    from processing.preprocessing.rotation_helper import get_rotation_angle

    original_path = os.path.join(VIDEOS_DIR, video_file)

    # Փոխել .MOV կամ այլ ֆորմատներ → mp4
    video_path = convert_to_mp4(original_path)

    if not video_path:
        print(f"❌ Բաց թողնվեց {video_file} – չի հաջողվել mp4 դարձնել։")
        continue


    # ՍՏԱՆԱԼ ՊՏՏՄԱՆ ԱՆԿՅՈՒՆԸ
    rotation = get_rotation_angle(video_path)
    print(f"↩️ Վիդեոն ունի {rotation}° պտտում։")

    cap = load_video(video_path)
    cut_video_into_frames(cap, frame_output_dir, rotation=rotation)

