import os


# Check the operating system
if os.name == "nt":  # For Windows
    clear_command = "cls"
else:  # For Linux/Unix/MacOS
    clear_command = "clear"


def clear_screen() -> None:
    os.system(clear_command)


def get_ffmpeg_binary() -> str:
    FFMPEG_DOWNLOAD_PATH = "ffmpeg_download"

    if not os.path.exists(FFMPEG_DOWNLOAD_PATH):
        print("ffmpeg_download doesn't exist")
        quit()

    for root, dirs, files in os.walk(FFMPEG_DOWNLOAD_PATH):
        for file in files:
            if file == "ffmpeg.exe":
                return os.path.join(root, file)

    return "ffmpeg_download\\ffmpeg-7.1-essentials_build\\bin\\ffmpeg.exe"
