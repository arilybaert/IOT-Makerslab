import pygame

class Player:
    app.config["MUSIC_UPLOADS"] = "/home/pi/Documents/IOT-Makerslab/app/static/music/uploads/"

    def play(file):
        pygame.mixer.init()
    
    #a = pygame.mixer.sound(app.config["MUSIC_UPLOADS"] + file)
    #b = a.get_length()

        pygame.mixer.music.load(app.config["MUSIC_UPLOADS"] + file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            # print("\r"+str(pygame.mixer.music.get_pos()))
            continue