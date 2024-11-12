import argparse
import time
import os

from video_renderer import VideoRenderer
from image_renderer import ImageRenderer

# Initialize the parser
parser = argparse.ArgumentParser(description="Video to ascii converter")

# Add arguments
parser.add_argument(
    "-v", "--video", type=str, help="The path of the video", default=None
)

parser.add_argument("-a", "--audio", action="store_true", help="Enable audio")
parser.add_argument(
    "-av", "--audiovolume", type=float, help="Change the audio volume", default=50
)

parser.add_argument(
    "-i", "--inverted", action="store_false", help="Reverse the ascii grayscale string"
)
parser.add_argument(
    "-rt", "--rtemp", action="store_true", help="Removes created audio file"
)
parser.add_argument(
    "-g",
    "--grayscale",
    type=str,
    help="Custom grayscale string",
    default="""@MBHENR#KWXDFPQASUZbdehx*8Gm&04LOVYkpq5Tagns69owz$CIu23Jcfry%1v7l+it[] {}?j|()=~!-/<>\"^_';,:`. """,
)

parser.add_argument(
    "-d",
    "--dimensions",
    type=lambda s: tuple(map(int, s.strip("()").split(","))),
    help="Dimensions in the format (x,y)",
    default=(100, 50),
)

parser.add_argument(
    "-s",
    "--savepath",
    type=str,
    help="Saves the ascii frames into a text file",
    default=None,
)

parser.add_argument(
    "-r",
    "--read",
    type=str,
    help="Reads the ascii frames from a text file",
    default=None,
)

parser.add_argument(
    "-st", "--startin", type=int, help="Starts from a specific frame", default=0
)

parser.add_argument(
    "-ed",
    "--endin",
    type=int,
    help="Ends the process on a specific frame",
    default=None,
)

# Image args
parser.add_argument(
    "-im", "--image", type=str, help="The path of the image", default=None
)

parser.add_argument("-ir", "--isrgb", action="store_true", help="This only applies to images")

parser.add_argument("-an", "--angle", type=int, help="Changes the image angle", default=90)

parser.add_argument("-c", "--contrast", type=int, help="Set the contrast of the foreground text", default=0)

program_args = parser.parse_args()


def calculate_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()

        func(*args, **kwargs)

        end = time.time()

        print(f"{func.__name__} took: {end - start:.1}s")

    return wrapper


def main():
    # Read from file
    viascii = VideoRenderer(program_args)
    if program_args.endin is not None and program_args.endin < program_args.startin:
        print("Ending frame number is lower than the starting frame number")
        return

    if program_args.read is not None:
        viascii.read_frames(program_args.read)
        return

    # Render video
    if program_args.video is not None:
        video_path = program_args.video

        if not os.path.exists(video_path):
            print(f"'{video_path}' does not exist.")
            return

        if program_args.savepath is not None:
            viascii.save_frames(video_path, program_args.savepath)
            return

        if program_args.audio:
            viascii.print_ascii_frames(video_path, is_audio=True)
        else:
            viascii.print_ascii_frames(video_path)

    # Render image
    elif program_args.image is not None:

        iascii = ImageRenderer(program_args)

        iascii.print_image(program_args.image, program_args.isrgb, program_args.angle)


if __name__ == "__main__":
    main()
