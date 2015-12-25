# Simple Raspberry PI Internet radio using four buttons
import RPi.GPIO as GPIO
import os
import atexit
import time
from time import sleep
import sys
import atexit
import traceback

from rotary_class import RotaryEncoder

stderr = sys.stderr.write;

# Register exit routine
def finish():
    exec_command("service mpd stop")
    print("Radio stopped")

atexit.register(finish)

# This is the callback routine to handle volume events
def volume_event(event):
	display_event("Volume", event)
	return

# This is the callback routine to handle tuner events
def tuner_event(event):
	display_event("Tuner", event)
	return

# Switch definitions
MENU_SWITCH = 25
LEFT_SWITCH = 14
RIGHT_SWITCH = 15
UP_SWITCH = 17
DOWN_SWITCH = 18
MUTE_SWITCH = 4
revision = 2

# Execute system command sub-routine
def exec_command(cmd):
     result = ""
     p = os.popen(cmd)
     for line in p.readline().split('\n'):
          result = result + line
     return result

### Main routine ###
if __name__ == "__main__":
     exec_command("service mpd start")
     exec_command("mpc clear")
     #exec_command("mpc load mylist.pls")
     exec_command("mpc play")
     exec_command("mpc volume 70")

     while True:
          if event == RotaryEncoder.CLOCKWISE: 
               exec_command("mpc volume +4")
          if event == RotaryEncoder.ANTICLOCKWISE:
               exec_command("mpc volume -4")
          sleep(0.2)
