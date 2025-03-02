from machine import I2C, Pin
import neopixel
import time

# I2C Configuration (PCF8575 connected to GP0 (SDA) and GP1 (SCL))
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)  # 400kHz I2C speed
PCF8575_ADDRESS = 0x20  # Default I2C address of PCF8575

# NeoPixel Configuration (5 LEDs on GP15)
NUM_PIXELS = 5
neo = neopixel.NeoPixel(Pin(14), NUM_PIXELS)

# Function to read 16-bit value from PCF8575
def read_pcf8575():
    data = i2c.readfrom(PCF8575_ADDRESS, 2)  # Read 2 bytes
    return (data[1] << 8) | data[0]  # Combine into a 16-bit value

# Function to set NeoPixels to white
def set_neopixels_white():
    for i in range(NUM_PIXELS):
        neo[i] = (255, 255, 255)  # White color
    neo.write()

# Function to turn off NeoPixels
def turn_off_neopixels():
    for i in range(NUM_PIXELS):
        neo[i] = (0, 0, 0)  # Off
    neo.write()

while True:
    value = read_pcf8575()  # Read all GPIO states
    P11_state = (value >> 0) & 1  # Extract bit 11 (P11)
    
    if P11_state:
        print("P11 is HIGH - Turning ON NeoPixels")
        set_neopixels_white()
    else:
        print("P11 is LOW - Turning OFF NeoPixels")
        turn_off_neopixels()

    time.sleep(0.1)  # Wait for 500ms
