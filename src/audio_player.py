import pygame
import ffmpeg
import os

class AudioPlayer:
    def __init__(self, video_path, args):
        self.audio_path = self.extract_audio(video_path)
        self.args = args
        self.audio_played = False
        
        self.volume = self.args.audiovolume / 100
        
        pygame.init()

    def extract_audio(self, video_path: str) -> str:
        audio_output_path = video_path.split(".")[0] + "_split.wav"

        # Extract audio from video
        ffmpeg.input(video_path).output(audio_output_path).run()

        return audio_output_path

    def play_audio(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.audio_path)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(self.volume)
        
        self.audio_played = True

    def stop_audio(self):
        pygame.mixer.music.stop()

        # Remove created audio file
        if self.args.rtemp:
            try:
                os.remove(self.audio_path)
            except Exception as e:
                print(e)
        
        self.audio_played = False
                
    def print_time(self) -> None:
        print(pygame.mixer.music.get_pos() / 1000.0)
        
    def set_pos(self, time) -> None:
        pygame.mixer.music.set_pos(time)
        
    def is_audio_played(self):
        return self.audio_played