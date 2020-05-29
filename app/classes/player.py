#
# Author: Edelweise, Ari Lybaert & Arne Verleyen
# 
# Link: https://github.com/eidleweise/EDMC_Podcast_Player/blob/e211bd27006ebd1c659bbc40f32526631cf96098/player.py
#

import sys
import os.path
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED


this = sys.modules[__name__]

if sys.version_info[0] < 3:
    sys.path.append(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'pygame2'))
    import pygame
else:
    sys.path.append(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'pygame3'))
    import pygame


class Player(object):

    def __init__(self):
        self.sense = SenseHat()

        self.volume = 100
        # initially the music is OFF
        self.music_playing = False
        # init all the sound stuff
        # give myself a large buffer, as well (last value), otherwise playback stutters
        pygame.mixer.init(44100, -16, True, 4096)

    def start_next_song(self, file_name):
        # turn of song events...
        pygame.mixer.music.set_endevent()
        pygame.mixer.music.load(file_name)
        # when new music is loaded, the volume param is reset. Fix it
        pygame.mixer.music.set_volume((float)((float)(self.volume) / 100.0))
        pygame.mixer.music.play()
        # set an endevent to catch it
        pygame.mixer.music.set_endevent(SONG_END)
        self.music_playing = True
        self.sense.clear()

        #play logo
        self.sense.set_pixel(2, 1, [0, 0, 255])
        self.sense.set_pixel(2, 2, [0, 0, 255])
        self.sense.set_pixel(2, 3, [0, 0, 255])
        self.sense.set_pixel(2, 4, [0, 0, 255])
        self.sense.set_pixel(2, 5, [0, 0, 255])
        self.sense.set_pixel(2, 6, [0, 0, 255])
        self.sense.set_pixel(2, 7, [0, 0, 255])

        self.sense.set_pixel(3, 2, [0, 0, 255])
        self.sense.set_pixel(3, 3, [0, 0, 255])
        self.sense.set_pixel(3, 4, [0, 0, 255])
        self.sense.set_pixel(3, 5, [0, 0, 255])
        self.sense.set_pixel(3, 6, [0, 0, 255])

        self.sense.set_pixel(4, 3, [0, 0, 255])
        self.sense.set_pixel(4, 4, [0, 0, 255])
        self.sense.set_pixel(4, 5, [0, 0, 255])

        self.sense.set_pixel(5, 4, [0, 0, 255])

        return True
    def set_volume(self, new_volume):
        """Sets and inits new volume level"""
        # must be within range 0-100
        if new_volume < 0:
            self.volume = 0
        elif new_volume > 100:
            self.volume = 100
        else:
            self.volume = new_volume
        pygame.mixer.music.set_volume((float)((float)(self.volume) / 100.0))
        return True

    def get_volume(self):
        """Returns value of current volume"""
        return self.volume

    def stop_music(self):
        """Simply stops the current music"""
        # turn off events as well
        pygame.mixer.music.set_endevent()
        pygame.mixer.music.pause()
        self.music_playing = False
        
        self.sense.clear()

        # pauze logo
        self.sense.set_pixel(2, 0, [255, 0, 0])
        self.sense.set_pixel(2, 1, [255, 0, 0])
        self.sense.set_pixel(2, 2, [255, 0, 0])
        self.sense.set_pixel(2, 3, [255, 0, 0])
        self.sense.set_pixel(2, 4, [255, 0, 0])
        self.sense.set_pixel(2, 5, [255, 0, 0])
        self.sense.set_pixel(2, 6, [255, 0, 0])
        self.sense.set_pixel(2, 7, [255, 0, 0])

        self.sense.set_pixel(3, 0, [255, 0, 0])
        self.sense.set_pixel(3, 1, [255, 0, 0])
        self.sense.set_pixel(3, 2, [255, 0, 0])
        self.sense.set_pixel(3, 3, [255, 0, 0])
        self.sense.set_pixel(3, 4, [255, 0, 0])
        self.sense.set_pixel(3, 5, [255, 0, 0])
        self.sense.set_pixel(3, 6, [255, 0, 0])
        self.sense.set_pixel(3, 7, [255, 0, 0])

        self.sense.set_pixel(5, 0, [255, 0, 0])
        self.sense.set_pixel(5, 1, [255, 0, 0])
        self.sense.set_pixel(5, 2, [255, 0, 0])
        self.sense.set_pixel(5, 3, [255, 0, 0])
        self.sense.set_pixel(5, 4, [255, 0, 0])
        self.sense.set_pixel(5, 5, [255, 0, 0])
        self.sense.set_pixel(5, 6, [255, 0, 0])
        self.sense.set_pixel(5, 7, [255, 0, 0])

        self.sense.set_pixel(6, 0, [255, 0, 0])
        self.sense.set_pixel(6, 1, [255, 0, 0])
        self.sense.set_pixel(6, 2, [255, 0, 0])
        self.sense.set_pixel(6, 3, [255, 0, 0])
        self.sense.set_pixel(6, 4, [255, 0, 0])
        self.sense.set_pixel(6, 5, [255, 0, 0])
        self.sense.set_pixel(6, 6, [255, 0, 0])
        self.sense.set_pixel(6, 7, [255, 0, 0])
        return True

    def start_music(self):
        """Turns music back on"""
        pygame.mixer.music.set_endevent(SONG_END)
        pygame.mixer.music.unpause()
        self.music_playing = True

        self.sense.clear()

        #play logo
        self.sense.set_pixel(2, 1, [0, 0, 255])
        self.sense.set_pixel(2, 2, [0, 0, 255])
        self.sense.set_pixel(2, 3, [0, 0, 255])
        self.sense.set_pixel(2, 4, [0, 0, 255])
        self.sense.set_pixel(2, 5, [0, 0, 255])
        self.sense.set_pixel(2, 6, [0, 0, 255])
        self.sense.set_pixel(2, 7, [0, 0, 255])

        self.sense.set_pixel(3, 2, [0, 0, 255])
        self.sense.set_pixel(3, 3, [0, 0, 255])
        self.sense.set_pixel(3, 4, [0, 0, 255])
        self.sense.set_pixel(3, 5, [0, 0, 255])
        self.sense.set_pixel(3, 6, [0, 0, 255])

        self.sense.set_pixel(4, 3, [0, 0, 255])
        self.sense.set_pixel(4, 4, [0, 0, 255])
        self.sense.set_pixel(4, 5, [0, 0, 255])

        self.sense.set_pixel(5, 4, [0, 0, 255])
        return True

    def get_pos(self):
        pos = pygame.mixer.music.get_pos()
        return pos


SONG_END = 2514
player = Player()