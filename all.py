#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
 
from rpi_ws281x import *
import argparse
import RPi.GPIO as GPIO
from pygame import mixer, event
import time, random, pygame, noise, threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

audio_list = list(range(1,22))
random.shuffle(audio_list)
MUSIC_END = pygame.USEREVENT + 1
pygame.init()
mixer.init()
screen = pygame.display.set_mode((50,50))

def playAudio(i):
    time.sleep(2)
    file = str(audio_list[i]) + '.mp3'
    mixer.music.load(file)
    print(file)
    mixer.music.play()
    mixer.music.set_endevent(MUSIC_END)
 
# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
 
def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
 
def flame(strip, x):

        for i in range(strip.numPixels()):
            y = i * 1
            red = int((noise.pnoise2(x,y) + 1) * 128 + 20)
            if red > 255:
                red = 255
            green = int(red * .5)

            strip.setPixelColor(i, Color(green,red,0))
        strip.show()
        time.sleep(.05)

def flameIn(strip):
    for t in range(10):
        red = int(200 * t / 10)
        green = int(red * .5)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(green, red, 0))
        strip.show()
        time.sleep(.05)

def flameOut(strip):
    for t in range(20):
        red = 200 - int(200 * t / 20)
        green = int(red * .5)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(green, red, 0))
        strip.show()
        time.sleep(.05)
 
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
 
def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
 
def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
 
def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
 
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    colorWipe(strip, Color(0,0,0), 10)
    
    index = 0
    playing = False
    flameX = 0.1
    flameSpeed = .08
    audioPlaying = False
    
    
    colorWipe(strip, Color(50, 100, 0), 10)  # Red wipe
    colorWipe(strip, Color(0,0,0), 10)

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
 
    try:
        while True:
            if GPIO.input(23) and not playing:
                print('Motion detected')
                playing = True
                audioplayer = threading.Thread(target=playAudio,args=(index,))
                audioplayer.start()
                index = (index + 1) % 22
                flameIn(strip)
            
            if playing:
                flameX += flameSpeed
                flame(strip, flameX)
            else:
                time.sleep(0.1)

            for event in pygame.event.get():
                if event.type == MUSIC_END:
                    playing = False
                    flameOut(strip)
                    colorWipe(strip, Color(0,0,0), 10)
                    print('ready')

#                 if index < 2 and event.type == MUSIC_END:
#                     index += 1
#                     time.sleep(random.randint(1,3))
#                     file = str(audio_list[index]) + '.mp3'
#                     mixer.music.load(file)
#                     print(file)
#                     print('playing')
#                     mixer.music.play()
#                     mixer.music.set_endevent(MUSIC_END)
    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)

