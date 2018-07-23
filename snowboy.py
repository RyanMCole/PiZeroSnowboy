import snowboydecoder
import sys
import signal
import random #to randomize audio playlists
import pyaudio #trying to fix autologin error
#import this to call bash commands within python:
import os

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

#don't need this warning when calling pmdl programmatically:
#if len(sys.argv) == 1:
#    print("Error: need to specify model name")
#    print("Usage: python demo.py your.model")
#    sys.exit(-1)

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

#original line from kitt.ai/snowboy:
#model = sys.argv[1]
#Add custom voice models here:
models = ['/home/pi/snowboy/resources/mybabe.pmdl', '/home/pi/snowboy/resources/dropthebase.pmdl', '/home/pi/snowboy/resources/motorfunctions.pmdl', '/home/pi/snowboy/resources/happyholidays.pmdl', '/home/pi/snowboy/resources/coolmemebro.pmdl', '/home/pi/snowboy/resources/merrychristmas.pmdl', '/home/pi/snowboy/resources/morghulis.pmdl', '/home/pi/snowboy/resources/murica.pmdl', '/home/pi/snowboy/resources/hailsatan.pmdl', '/home/pi/snowboy/resources/stop.pmdl', '/home/pi/snowboy/resources/sweater_model.pmdl', '/home/pi/snowboy/resources/unite.pmdl']

#original line from kitt.ai/snowboy:
#detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
#use this so you don't need to specify voice model when calling this script
detector = snowboydecoder.HotwordDetector(models, sensitivity=0.5)

#put what should happen when snowboy detects hotword here:

#lists for random plays.
myBaseList = [snowboydecoder.DETECT_BASE1, snowboydecoder.DETECT_BASE2]
myHolidayList = [snowboydecoder.DETECT_HH1, snowboydecoder.DETECT_HH2, snowboydecoder.DETECT_HH3, snowboydecoder.DETECT_HH4, snowboydecoder.DETECT_HH5, snowboydecoder.DETECT_HH6, snowboydecoder.DETECT_HH7, snowboydecoder.DETECT_BABE1]
myXMasList = [snowboydecoder.DETECT_XMAS1, snowboydecoder.DETECT_XMAS2]
mySweatList = [snowboydecoder.DETECT_SWEAT1, snowboydecoder.DETECT_SWEAT2, snowboydecoder.DETECT_SWEAT3, snowboydecoder.DETECT_SWEAT4, snowboydecoder.DETECT_SWEAT5, snowboydecoder.DETECT_SWEAT6]


callbacks = [
             lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_BABE1),
             lambda: snowboydecoder.play_audio_file(random.choice(myBaseList)),
             lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_FUNCTIONS1),
             lambda: snowboydecoder.play_audio_file(random.choice(myHolidayList)),
             lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_MEME1),
             lambda: snowboydecoder.play_audio_file(random.choice(myXMasList)),
             lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_MORGHULIS1),
             lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_MURICA1),
             lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_SATAN1),
             lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_STOP1),
             lambda: snowboydecoder.play_audio_file(random.choice(mySweatList)),
             lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_UNITE1)]

#without "lambda", callback will run immediately on startup, 
#and then after each hotword detection:
#callbacks = [os.system("/home/pi/test.sh")]

print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
