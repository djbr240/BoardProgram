from machine import Pin  # Import Pin class from machine module
import neopixel
from utime import sleep

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 25
pin = Pin(28, Pin.OUT)

pixels = neopixel.NeoPixel(pin, num_pixels)

while True:
    for i in range(num_pixels):
        # Turn on the current LED (white color)
        pixels[i] = (255, 255, 255)
        pixels.write()  # Update the NeoPixels
        sleep(0.5)  # Keep the LED on for 0.5 seconds

        # Turn off the current LED
        pixels[i] = (0, 0, 0)
        pixels.write()  # Update the NeoPixels
        sleep(0.5)  # Keep the LED off for 0.5 seconds
