from pygame import mixer, event
import time, random, pygame

audio_list = list(range(1,22))
random.shuffle(audio_list)

index = 0

MUSIC_END = pygame.USEREVENT + 1
pygame.init()
screen = pygame.display.set_mode((50,50))

mixer.music.load(str(audio_list[index]) + '.mp3')
mixer.music.play()
mixer.music.set_endevent(MUSIC_END)

while index < 2:
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            index += 1
            time.sleep(random.randint(1,3))
            mixer.music.load(str(audio_list[index]) + '.mp3')
            print('playing')
            mixer.music.play()
            mixer.music.set_endevent(MUSIC_END)