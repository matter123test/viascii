import cv2
import os
import ffmpeg
import pygame
import argparse
import time
import sys
import numpy as np

# Initialize the parser
parser = argparse.ArgumentParser(description="Realtime frame to ascii renderer")

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
    "--dimensions",
    type=lambda s: tuple(map(int, s.strip("()").split(","))),
    help="Dimensions in the format (x, y)",
    default=(100, 50),
)

# Parse arguments
args = parser.parse_args()

r_width, r_height = args.dimensions


def extract_audio(video_path: str) -> str:
    audio_output_path = video_path.split(".")[0] + "_split.wav"

    # Extract audio
    ffmpeg.input(video_path).output(audio_output_path).run()

    return audio_output_path


grayscale = args.grayscale

grayscale_normal = grayscale
grayscale_inverted = grayscale[::-1]

if args.inverted:
    grayscale = grayscale_inverted
else:
    grayscale = grayscale_normal


def pixel_to_ascii(gray_value: np.ndarray) -> str:
    num_chars = len(grayscale)
    # Normalize the grayscale value to the range of characters
    return grayscale[int(gray_value / 255 * (num_chars - 1))]


# Assuming pixel_to_ascii is defined to convert a pixel to an ASCII character
def frame_to_ascii(frame) -> str:
    # Convert resized frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Create a string of ASCII characters
    ascii_chars = np.vectorize(pixel_to_ascii)(gray_frame)

    # Join ASCII characters into lines
    ascii_frame = "\n".join("".join(row) for row in ascii_chars)

    return ascii_frame


def print_ascii_frame(ascii_frame: str) -> None:
    # Move cursor to top left of the terminal
    sys.stdout.write("\033[H" + ascii_frame + "\n")
    sys.stdout.flush()


def run(video_path: str, audio_path: str | None) -> None:
    os.system("clear")

    cap = cv2.VideoCapture(video_path)

    target_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1 / target_fps  # Time per frame in seconds (1/60)

    if audio_path is not None:
        pygame.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

    try:
        while cap.isOpened():
            start_time = time.time()

            ret, rgb_frame = cap.read()

            if ret:
                frame = cv2.resize(
                    rgb_frame, dsize=(r_width, r_height), interpolation=cv2.INTER_LINEAR
                )

                ascii_frame = frame_to_ascii(frame)
                print_ascii_frame(ascii_frame)

                # Calculate the elapsed time for this frame
                elapsed_time = time.time() - start_time

                # If processing was faster than the frame delay, wait for the remaining time
                if elapsed_time < frame_delay:
                    time.sleep(frame_delay - elapsed_time)
            else:
                break

    except KeyboardInterrupt:
        os.system("clear")

    if audio_path is not None:
        pygame.mixer.music.stop()

        # Remove created audio file
        if args.rtemp:
            try:
                os.remove(audio_path)
            except Exception as e:
                print(e)

    cap.release()


def main():
    video_path = args.video

    if args.audio:
        run(video_path, extract_audio(video_path))
    else:
        run(video_path, None)


if __name__ == "__main__":
    main()
