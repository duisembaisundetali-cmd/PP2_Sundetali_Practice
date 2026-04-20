import pygame
import os

class MusicPlayer:
    def __init__(self, track_files):
        pygame.mixer.init()
        self.tracks = track_files
        self.current_index = 0
        self.is_playing = False
        if self.tracks:
            pygame.mixer.music.load(self.tracks[self.current_index])
            
    def play(self):
        if self.tracks:
            pygame.mixer.music.play()
            self.is_playing = True
            
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        
    def next_track(self):
        if self.tracks:
            self.current_index = (self.current_index + 1) % len(self.tracks)
            pygame.mixer.music.load(self.tracks[self.current_index])
            if self.is_playing:
                self.play()
                
    def prev_track(self):
        if self.tracks:
            self.current_index = (self.current_index - 1) % len(self.tracks)
            pygame.mixer.music.load(self.tracks[self.current_index])
            if self.is_playing:
                self.play()
                
    def get_info(self):
        if not self.tracks:
            return "No tracks loaded."
        status = "Playing" if self.is_playing else "Stopped"
        track_name = os.path.basename(self.tracks[self.current_index])
        return f"{status}: {track_name}"