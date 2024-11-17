import os
import platform


def get_os_name() -> str:
    return platform.system().lower()

os_name = get_os_name()

# Check the operating system
if os_name == "windows":
    clear_command = "cls"
elif os_name == "linux":
    clear_command = "clear"


def clear_screen() -> None:
    os.system(clear_command)
    
def get_ffmpeg_binary() -> str | None:
    
    FFMPEG_DOWNLOAD_PATH = "ffmpeg_download"
    
    if not os.path.exists(FFMPEG_DOWNLOAD_PATH):
        print("ffmpeg_download doesn't exist")
        quit()
    
    if os_name == "windows":
        for root, dirs, files in os.walk(FFMPEG_DOWNLOAD_PATH):
            for file in files:
                if file == "ffmpeg.exe":
                    return os.path.join(root, file)

    elif os_name == "linux":
        for root, dirs, files in os.walk(FFMPEG_DOWNLOAD_PATH):
            for file in files:
                file_path = os.path.join(root, file)
                
                if file == "ffmpeg" and not os.path.isdir(file_path):
                    return file_path
                
    return None    
        
