from machine import I2C, ADC, Pin
import neopixel
import utime
from utime import sleep

# Board LED config
Board_LED_num_pixels = 42 # 42 Board LEDs
Board_LED_pin = Pin(22, Pin.OUT)
Board_pixels = neopixel.NeoPixel(Board_LED_pin, Board_LED_num_pixels)

# Board_pixels.fill((255, 255, 255))
# Board_pixels.write()
# # sleep(5)

# # Board_pixels.fill((0,0,0))
# # Board_pixels.write()

while True:
    print("Testing board LEDs (5 seconds)...")
    # Light up all board LEDs (dim white)
    for i in range(42):
        Board_pixels[i] = ((255, 255, 255))
        Board_pixels.write()
        sleep(.3)
        Board_pixels[i] = ((0, 0, 0))
        Board_pixels.write()
        sleep(.3)
        print("Test complete")