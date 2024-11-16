import cv2
import os
import argparse
import time
import sys
import numpy as np
import linecache

from src.audio_player import AudioPlayer
from tqdm import tqdm

from src.utils import clear_screen


class VideoRenderer:
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

    def rgb_to_ansi_bg(self, r, g, b):
        return f"\033[48;2;{r};{g};{b}m"  # ANSI background color

    def rgb_to_ansi_fg(self, r, g, b):
        return f"\033[38;2;{r};{g};{b}m"  # ANSI foreground color

    def frame_to_ascii(self, frame) -> str:
        # Convert resized frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Create a string of ASCII characters
        ascii_chars = np.vectorize(self.pixel_to_ascii)(gray_frame)

        ascii_frame = "\n".join("".join(row) for row in ascii_chars)

        return ascii_frame

    # TODO: Make an async function that handles printing and generating frames instead of running on the same thread
    def frame_to_ascii_rgb(self, frame) -> str:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        brightness = (
            0.299 * rgb_frame[:, :, 0]
            + 0.587 * rgb_frame[:, :, 1]
            + 0.114 * rgb_frame[:, :, 2]
        )

        # Apply contrast adjustments to RGB channels
        contrast_adjusted = np.clip(rgb_frame + self.args.contrast, 0, 255)

        # Convert each brightness value to an ASCII character
        ascii_chars = np.vectorize(self.pixel_to_ascii)(brightness.astype(int))

        # Generate ANSI color codes for background and foreground
        bg_colors = np.vectorize(self.rgb_to_ansi_bg)(
            rgb_frame[:, :, 0], rgb_frame[:, :, 1], rgb_frame[:, :, 2]
        )
        fg_colors = np.vectorize(self.rgb_to_ansi_fg)(
            contrast_adjusted[:, :, 0],
            contrast_adjusted[:, :, 1],
            contrast_adjusted[:, :, 2],
        )

        # Create the formatted ASCII image by combining fg, bg colors, and ASCII chars
        ascii_image_array = np.char.add(np.char.add(fg_colors, bg_colors), ascii_chars)
        ascii_image_array = np.char.add(ascii_image_array, "\033[0m")

        # Convert the 2D array into a single string with newlines for each row
        ascii_image = "\n".join("".join(row) for row in ascii_image_array)

        return ascii_image

    def print_ascii_frame(self, ascii_frame: str) -> None:
        # Move cursor to top left of the terminal
        sys.stdout.write("\033[H" + ascii_frame + "\n")
        sys.stdout.flush()

    def print_ascii_frames(self, video_path: str, is_audio=False) -> None:
        clear_screen()
        cap = cv2.VideoCapture(video_path)

        cap.get(cv2.CAP_PROP_FRAME_COUNT)
        target_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1 / target_fps  # Time per frame in seconds (1/60)

        audio_player = None

        audio_time_skip = self.args.startin / target_fps

        if is_audio:
            audio_player = AudioPlayer(video_path, self.args)

        clear_screen()

        count = 0

        try:
            while cap.isOpened():
                start_time = time.time()

                ret, rgb_frame = cap.read()

                if self.args.endin is not None and count >= self.args.endin:
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

                        if self.args.isrgb:
                            ascii_frame = self.frame_to_ascii_rgb(frame)
                        else:
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
        clear_screen()

        if os.path.exists(output_path):
            print(f"{output_path} already exists!")
            return

        cap = cv2.VideoCapture(video_path)

        total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if self.args.endin is not None:
            total_frame_count = self.args.endin - self.args.startin

        count = self.args.startin

        target_fps = int(cap.get(cv2.CAP_PROP_FPS))

        print(f"Saving ascii frames to {output_path}")

        # Set the frame data on the first line
        with open(output_path, "w") as f:
            f.write(f"{self.r_width, self.r_height, total_frame_count, target_fps}\n")

        with tqdm(total=total_frame_count) as pbar:
            try:
                while cap.isOpened():
                    ret, rgb_frame = cap.read()

                    if self.args.endin is not None and count >= self.args.endin:
                        break

                    if ret:
                        frame = cv2.resize(
                            rgb_frame,
                            dsize=(self.r_width, self.r_height),
                            interpolation=cv2.INTER_LINEAR,
                        )

                        if self.args.isrgb:
                            ascii_frame = self.frame_to_ascii_rgb(frame)
                        else:
                            ascii_frame = self.frame_to_ascii(frame)

                        self.save_frame(ascii_frame, output_path)
                        count += 1
                        pbar.update(1)
                    else:
                        break
            except KeyboardInterrupt:
                clear_screen()

        print(f"Saving frames completed.")

    def get_frame_from_file(self, frames_path, line_start, line_end):
        ascii_frame = ""
        for i in range(line_start, line_end):
            ascii_frame += linecache.getline(frames_path, i + 2)

        return ascii_frame

    def read_frames(self, frames_path):
        clear_screen()

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
                if self.args.endin is not None and count >= self.args.endin:
                    break

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
