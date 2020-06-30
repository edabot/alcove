from Tkinter import *
import tkSnack

root = Tk()
tkSnack.initializeSnack(root)

snd = tkSnack.Sound()
snd.read('sound.wav')
snd.play(blocking=1)from pydub import AudioSegment
from pydub.playback import play

song = AudioSegment.from_wav("1.wav")
python3-tksnackplay(song)
