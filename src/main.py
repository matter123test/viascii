from renderer import Renderer
import argparse, ffmpeg, time


# Initialize the parser
parser = argparse.ArgumentParser(description="Video to ascii renderer")

# Add arguments
parser.add_argument("video", type=str, help="The path of the video")
parser.add_argument("-a", "--audio", action="store_true", help="Enable audio")
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

# Parse arguments
args = parser.parse_args()


def calculate_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()

        func(*args, **kwargs)

        end = time.time()

        print(f"{func.__name__} took: {end-start:.1}s")

    return wrapper


def main():
    viascii = Renderer(args)

    video_path = args.video

    if args.savepath is not None:
        viascii.save_frames(video_path, args.savepath)
        return

    if args.audio:
        viascii.print_ascii_frames(video_path, is_audio=True)
    else:
        viascii.print_ascii_frames(video_path)


if __name__ == "__main__":
    main()
