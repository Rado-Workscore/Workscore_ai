import ffmpeg

def get_rotation_angle(video_path):
    try:
        meta_dict = ffmpeg.probe(video_path)
        rotation = int(meta_dict['streams'][0]['tags'].get('rotate', 0))
        return rotation
    except Exception:
        return 0  # Եթե չի հաջողվում – ենթադրում ենք ուղղ է
