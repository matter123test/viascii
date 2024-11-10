import cv2
import os
import pygame
import argparse
import time
import sys
import numpy as np
from tqdm import tqdm
import ffmpeg


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

    # Assuming pixel_to_ascii is defined to convert a pixel to an ASCII character
    def frame_to_ascii(self, frame) -> str:
        # Convert resized frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Create a string of ASCII characters
        ascii_chars = np.vectorize(self.pixel_to_ascii)(gray_frame)

        # Join ASCII characters into lines
        ascii_frame = "\n".join("".join(row) for row in ascii_chars)

        return ascii_frame

    def print_ascii_frame(self, ascii_frame: str) -> None:
        # Move cursor to top left of the terminal
        sys.stdout.write("\033[H" + ascii_frame + "\n")
        sys.stdout.flush()

    def print_ascii_frames(self, video_path: str, is_audio=False) -> None:
        os.system("clear")

        cap = cv2.VideoCapture(video_path)

        target_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1 / target_fps  # Time per frame in seconds (1/60)

        audio_player = None

        if is_audio:
            audio_player = AudioPlayer(video_path, self.args)
            audio_player.play_audio()
            
        os.system("clear")

        try:
            while cap.isOpened():
                start_time = time.time()

                ret, rgb_frame = cap.read()

                if ret:
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

        total_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        frame_count = 0

        target_fps = cap.get(cv2.CAP_PROP_FPS)

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


class AudioPlayer:
    def __init__(self, video_path, args):
        self.audio_path = self.extract_audio(video_path)
        self.args = args

    def extract_audio(self, video_path: str) -> str:
        audio_output_path = video_path.split(".")[0] + "_split.wav"

        # Extract audio from video
        ffmpeg.input(video_path).output(audio_output_path).run()

        return audio_output_path

    def play_audio(self):
        pygame.init()
        pygame.mixer.music.load(self.audio_path)
        pygame.mixer.music.play()

    def stop_audio(self):
        pygame.mixer.music.stop()

        # Remove created audio file
        if self.args.rtemp:
            try:
                os.remove(self.audio_path)
            except Exception as e:
                print(e)
