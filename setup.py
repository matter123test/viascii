import os
import platform
import zipfile
import urllib.request
from tqdm import tqdm


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


def extract(zip_path, output_dir):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)


def install_ffmpeg():
    """Simple function to download FFmpeg binaries."""
    os_name = platform.system().lower()
    ffmpeg_urls = {
        "windows": "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
        "linux": "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz",
    }

    url = ffmpeg_urls.get(os_name)
    if not url:
        raise RuntimeError("FFmpeg binary is not available for your OS.")

    download_path = "ffmpeg_download"
    os.makedirs(download_path, exist_ok=True)

    print(f"Downloading FFmpeg for {os_name}...")

    download(url, f"{download_path}/ffmpeg.zip")

    # Extract the binary
    # with zipfile.ZipFile(f"{download_path}/ffmpeg.zip", "r") as zip_ref:
    #     zip_ref.extractall(download_path)
    extract(f"{download_path}/ffmpeg.zip", f"{download_path}")

    # Remove downloaded zip file
    print(f"Removing downloaded zip file")
    os.remove(f"{download_path}/ffmpeg.zip")
    print(f"Removed zip file")

    return download_path


if __name__ == "__main__":
    try:
        ffmpeg_binary = install_ffmpeg()
        print(f"FFmpeg installed successfully: {ffmpeg_binary}")
    except Exception as e:
        print(f"Error setting up FFmpeg: {e}")
