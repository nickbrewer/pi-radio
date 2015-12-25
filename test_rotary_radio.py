#!/usr/bin/env python
#
# Raspberry Pi Rotary Test Encoder Class
# $Id: test_rotary_class.py,v 1.4 2014/07/22 13:10:01 bob Exp $
#
# Author : Bob Rathbone
# Site   : http://www.bobrathbone.com
#
# This class uses standard rotary encoder with push switch
#
# License: GNU V3, See https://www.gnu.org/copyleft/gpl.html
#
# Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
#             The authors shall not be liable for any loss or damage however caused.
#

import sys
import time
import atexit
import traceback
import RPi.GPIO as GPIO
import os
import atexit
from time import sleep

from rotary_class import RotaryEncoder

stderr = sys.stderr.write;

# Register exit routine
def finish():
    exec_command("service mpd stop")
    print("Radio stopped")

# Switch definitions
MENU_SWITCH = 25 #not using this, but afraid to comment it out yet
LEFT_SWITCH = 14 #not using this, but afraid to comment it out yet
RIGHT_SWITCH = 15 #not using this, but afraid to comment it out yet
UP_SWITCH = 17 #not using this, but afraid to comment it out yet
DOWN_SWITCH = 18 #not using this, but afraid to comment it out yet
MUTE_SWITCH = 4 #not using this, but afraid to comment it out yet

# Execute system command sub-routine
def exec_command(cmd):
     result = ""
     p = os.popen(cmd)
     for line in p.readline().split('\n'):
          result = result + line
     return result

# Try to trap any exit errors 
def exit_fn():
        if not traceback.format_exc().startswith('None'):
                s=traceback.format_exc()
	sys.exit(0)

# Register
atexit.register(exit_fn)

# This is the callback routine to handle volume events
def volume_event(event):
	display_event("Volume", event)
	return

# This is the callback routine to handle tuner events
def tuner_event(event):
	display_event("Tuner", event)
	return

def display_event(name,event): # This is the meat of the code that I need. 
	if event == RotaryEncoder.CLOCKWISE: # Right now I'm using it for volume, but eventually it will be used to switch to the next station
                print name + " volume up", exec_command("mpc volume +4")
	elif event == RotaryEncoder.ANTICLOCKWISE:
                print name + " volume down", exec_command("mpc volume -4")

# Allow user to select board revision
revision = 2

volumeknob = RotaryEncoder(LEFT_SWITCH,RIGHT_SWITCH,MUTE_SWITCH,volume_event,revision)
tunerknob = RotaryEncoder(UP_SWITCH,DOWN_SWITCH,MENU_SWITCH,tuner_event,revision)

### Main routine ###
if __name__ == "__main__":
        exec_command("service mpd start") # These lines probably  need to be moved into a different spot so it doesn't
        #exec_command("mpc clear")         # keep resetting the sound to 90 after changing the volume
     	#exec_command("mpc load mylist.pls") #The MPC Clear/Load Playlist I'm still working on, stupid permissions!
        exec_command("mpc play")          
        exec_command("mpc volume 90") 
        print "Use Ctl-C to exit"

	while True:
                time.sleep(0.2)

               
	




