from machine import I2C, ADC, Pin
import neopixel
import utime
from utime import sleep

# Board LED config
Board_LED_num_pixels = 42 # 42 Board LEDs
Board_LED_pin = Pin(22, Pin.OUT)
Board_pixels = neopixel.NeoPixel(Board_LED_pin, Board_LED_num_pixels)

while True:
    print("Testing board LEDs (5 seconds)...")
    # Light up all board LEDs (dim white)
    Board_pixels.fill((25, 25, 25))
    Board_pixels.write()
    sleep(1)
    Board_pixels.fill((0, 0, 0))
    Board_pixels.write()
    sleep(1)
    print("Test complete")