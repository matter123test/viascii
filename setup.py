import os
import platform
import zipfile
import tarfile
import urllib.request
from tqdm import tqdm

from src.utils import get_os_name


def download(url, output_dir):
    # Get the file size from the server
    response = urllib.request.urlopen(url)
    total_size = int(response.info().get("Content-Length", 0))

    # Set up the progress bar
    with tqdm(
        total=total_size, unit="B", unit_scale=True, desc="Downloading", ncols=80
    ) as progress:
        # Open the URL and download the file in chunks
        with urllib.request.urlopen(url) as source, open(output_dir, "wb") as target:
            while True:
                chunk = source.read(1024)  # Read in 1KB chunks
                if not chunk:
                    break
                target.write(chunk)
                progress.update(len(chunk))  # Update progress bar with chunk size

    print("\nDownload completed!")


def extract(format, compressed_file_path: str, output_dir: str) -> None:
    if format == ".zip":    
        with zipfile.ZipFile(compressed_file_path, "r") as ref:
            ref.extractall(output_dir)
            
    if format == ".tar.xz":
        with tarfile.open(compressed_file_path, "r") as ref:
            ref.extractall(output_dir)


def install_ffmpeg():
    os_name = get_os_name()
    
    ffmpeg_urls = {
        "windows": "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
        "linux": "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz",
    }

    formats = {
        "windows": ".zip",
        "linux": ".tar.xz"
    }

    url = ffmpeg_urls.get(os_name)
    if not url:
        raise RuntimeError("FFmpeg binary is not available for your OS.")
    
    

    download_path = "ffmpeg_download"
    os.makedirs(download_path, exist_ok=True)

    print(f"Downloading FFmpeg for {os_name}...")

    file_format = formats.get(os_name)
    compressed_file_path = f"ffmpeg{file_format}"
    
    download(url, f"{download_path}/{compressed_file_path}")

    print(f"Extracting {compressed_file_path}")
    # Extract the binary
    extract(file_format, f"{download_path}/{compressed_file_path}", f"{download_path}")

    # Remove downloaded zip file
    print(f"Removing downloaded zip file")
    os.remove(f"{download_path}/{compressed_file_path}")
    print(f"Removed zip file")

    return download_path

if __name__ == "__main__":
    ffmpeg_binary = install_ffmpeg()
    print(f"FFmpeg installed successfully: {ffmpeg_binary}")
