import cv2
import os
import argparse
import time
import sys
import numpy as np
import linecache

from audio_player import AudioPlayer
from tqdm import tqdm


class Renderer:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.r_width, self.r_height = args.dimensions

        self.grayscale = args.grayscale

        grayscale_normal = self.grayscale
        grayscale_inverted = self.grayscale[::-1]

        if args.inverted:
            self.grayscale = grayscale_inverted
        else:
            self.grayscale = grayscale_normal

    def pixel_to_ascii(self, gray_value: np.ndarray) -> str:
        num_chars = len(self.grayscale)
        # Normalize the grayscale value to the range of characters
        return self.grayscale[int(gray_value / 255 * (num_chars - 1))]

    def frame_to_ascii(self, frame) -> str:
        # Convert resized frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Create a string of ASCII characters
        ascii_chars = np.vectorize(self.pixel_to_ascii)(gray_frame)

        ascii_frame = "\n".join("".join(row) for row in ascii_chars)

        return ascii_frame

    def print_ascii_frame(self, ascii_frame: str) -> None:
        # Move cursor to top left of the terminal
        sys.stdout.write("\033[H" + ascii_frame + "\n")
        sys.stdout.flush()

    def print_ascii_frames(self, video_path: str, is_audio=False) -> None:
        os.system("clear")

        cap = cv2.VideoCapture(video_path)

        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        target_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1 / target_fps  # Time per frame in seconds (1/60)

        audio_player = None

        audio_time_skip = self.args.startin / target_fps

        if is_audio:
            audio_player = AudioPlayer(video_path, self.args)

        os.system("clear")

        count = 0

        try:
            while cap.isOpened():
                start_time = time.time()

                ret, rgb_frame = cap.read()

                if count >= self.args.endin:
                    break

                if ret:
                    if count >= self.args.startin:
                        # Play audio after searching the frame
                        if (
                            audio_player is not None
                            and not audio_player.is_audio_played()
                        ):
                            audio_player.play_audio()
                            audio_player.set_pos(audio_time_skip)

                        frame = cv2.resize(
                            rgb_frame,
                            dsize=(self.r_width, self.r_height),
                            interpolation=cv2.INTER_LINEAR,
                        )

                        ascii_frame = self.frame_to_ascii(frame)
                        self.print_ascii_frame(ascii_frame)

                        # Calculate the elapsed time for this frame
                        elapsed_time = time.time() - start_time

                        # If processing was faster than the frame delay, wait for the remaining time
                        if elapsed_time < frame_delay:
                            time.sleep(frame_delay - elapsed_time)
                    else:
                        sys.stdout.write(
                            "\033[H" + f"Searching for frame n°{self.args.startin}\n"
                        )
                        sys.stdout.flush()

                    count += 1
                else:
                    break

        except KeyboardInterrupt:
            pass

        if audio_player is not None:
            audio_player.stop_audio()

        cap.release()

    def save_frame(self, ascii_frame: str, output_path: str) -> None:
        with open(output_path, "a") as f:
            f.write(f"{ascii_frame}\n")

    def save_frames(self, video_path, output_path):
        os.system("clear")

        if os.path.exists(output_path):
            print(f"{output_path} already exists!")
            return

        cap = cv2.VideoCapture(video_path)

        total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_count = 0

        target_fps = int(cap.get(cv2.CAP_PROP_FPS))

        print(f"Saving ascii frames to {output_path}")

        # Set the frame data on the first line
        with open(output_path, "w") as f:
            f.write(f"{self.r_width, self.r_height, total_frame_count, target_fps}\n")

        with tqdm(total=total_frame_count) as pbar:
            try:
                while cap.isOpened():
                    ret, rgb_frame = cap.read()

                    if ret:
                        frame = cv2.resize(
                            rgb_frame,
                            dsize=(self.r_width, self.r_height),
                            interpolation=cv2.INTER_LINEAR,
                        )

                        ascii_frame = self.frame_to_ascii(frame)

                        self.save_frame(ascii_frame, output_path)
                        frame_count += 1
                        pbar.update(1)
                    else:
                        break
            except KeyboardInterrupt:
                os.system("clear")

        print(f"Saving frames completed.")

    def get_frame_from_file(self, frames_path, line_start, line_end):
        ascii_frame = ""
        for i in range(line_start, line_end):
            ascii_frame += linecache.getline(frames_path, i + 2)

        return ascii_frame

    def read_frames(self, frames_path):
        os.system("clear")

        frame_format = None
        with open(frames_path, "r") as f:
            frame_format = f.readline()

        width, height, total_frame_count, target_fps = tuple(
            map(int, frame_format.strip("()\n").split(","))
        )

        frame_delay = 1 / target_fps  # Time per frame in seconds (1/60)

        # Default value is 0
        count = self.args.startin

        try:
            while count < total_frame_count:
                start_time = time.time()

                # Calculating line_start and line_end for each frame
                line_start = count * height
                line_end = line_start + height

                # print(f"{line_start}, {line_end}")
                ascii_frame = self.get_frame_from_file(
                    frames_path, line_start, line_end
                )

                self.print_ascii_frame(ascii_frame)

                # Calculate the elapsed time for this frame
                elapsed_time = time.time() - start_time

                # If processing was faster than the frame delay, wait for the remaining time
                if elapsed_time < frame_delay:
                    time.sleep(frame_delay - elapsed_time)

                count += 1
        except KeyboardInterrupt:
            pass
