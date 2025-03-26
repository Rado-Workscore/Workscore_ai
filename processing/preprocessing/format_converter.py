import os
import ffmpeg

def convert_to_mp4(input_path):
    if input_path.endswith(".mp4"):
        return input_path  # Ոչ մի բան չանենք, եթե արդեն mp4 է

    output_path = input_path.rsplit(".", 1)[0] + ".mp4"

    if os.path.exists(output_path):
        print(f"✅ Արդեն կա mp4 տարբերակ՝ {output_path}")
        return output_path

    print(f"🎞️ Փոխակերպում ենք `{input_path}` → `{output_path}`")

    try:
        ffmpeg.input(input_path).output(
            output_path,
            vcodec="libx264",
            acodec="aac",
            strict="experimental",
            preset="fast",
            crf=23
        ).run(overwrite_output=True)

        print(f"✅ Փոխակերպում ավարտվեց․ {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Սխալ՝ վիդեոն mp4 դարձնելիս: {e}")
        return None
