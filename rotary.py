# Sample code for both the RotaryEncoder class and the Switch class.
# The common pin for the encoder should be wired to ground. 
# The sw_pin should be shorted to ground by the switch.

import gaugette.rotary_encoder
import gaugette.switch
import sys
import time
import atexit
import traceback
import Adafruit_GPIO as GPIO
import os
import atexit
from time import sleep
import Image
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO.SPI as SPI

stderr = sys.stderr.write;

# Image Raspberry Pi configuration. 
DC = 22
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0
A_PIN  = 29
B_PIN  = 28

encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
encoder.start()

last_state = None
station = ""
name = ""

# Create TFT LCD display class.
disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))

# Initialize display.
disp.begin()

# Execute system command sub-routine
def exec_command(cmd):
     result = ""
     p = os.popen(cmd)
     for line in p.readline().split('\n'):
          result = result + line
     return result

def image():
	if name == "http://206.190.136.141:9169/Live":
		image = Image.open('/home/pi/Adafruit_Python_ILI9341/examples/ksua.jpg') # Load an image.
		image = image.rotate(90).resize((240, 320)) # Resize the image and rotate it so it's 240x320 pixels.
		disp.display(image)  # Draw the image
	if name == "Radio":
		image = Image.open('/home/pi/Adafruit_Python_ILI9341/examples/krua.jpg') # Load an image.		
		image = image.rotate(90).resize((240, 320)) # Resize the image and rotate it so it's 240x320 pixels.			
		disp.display(image)  # Draw the image
	if name == "Rockabilly":
		image = Image.open('/home/pi/Adafruit_Python_ILI9341/examples/cat.jpg') # Load an image.		
		image = image.rotate(90).resize((240, 320)) # Resize the image and rotate it so it's 240x320 pixels.			
		disp.display(image)  # Draw the image

### Main routine ### 
if __name__ == "__main__":
        exec_command("service mpd start") 
        exec_command("mpc clear")         
     	exec_command("mpc load mylist")
        exec_command("mpc play")           
        exec_command("mpc volume 100") 
        disp.clear()
        image()
        print "Use Ctl-C to exit"

while True:
	try:		
		delta = encoder.get_delta()
		if delta == 1:
			exec_command("mpc next")
			print "Next"
			station = exec_command("mpc current").split(" ")
			name = station[0]
			image()
			time.sleep(0.5)
			
		elif delta == -1:
			exec_command("mpc prev")
			print "Previous"
			station = exec_command("mpc current").split(" ")
			name = station[0]
			image()
			time.sleep(0.5)	
					
	except KeyboardInterrupt:
		exec_command("mpc stop")
		print "\nExit"
		sys.exit(0)
