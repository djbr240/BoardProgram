from machine import ADC, Pin
from neopixel import NeoPixel
from time import sleep

# Initialize ADC for MUX SIG output
adc = ADC(Pin(28))  # ADC pin connected to the MUX SIG output

# GPIO pins for MUX select lines
select_pins = [
    Pin(10, Pin.OUT),  # S0
    Pin(11, Pin.OUT),  # S1
    Pin(12, Pin.OUT),  # S2
    Pin(13, Pin.OUT),  # S3
]

# NeoPixel configuration
NUM_PIXELS = 8  # Number of LEDs
np_pin = Pin(28, Pin.OUT)  # Pin connected to NeoPixel data line
np = NeoPixel(np_pin, NUM_PIXELS)

# ADC reference voltage (default is 3.3V)
V_REF = 3.3

def select_mux_channel(channel):
    """Set the MUX to the desired channel."""
    for i, pin in enumerate(select_pins):
        pin.value((channel >> i) & 1)  # Set each select pin to the correct bit

while True:
    for channel in range(8):  # Loop through channels 0 to 7
        select_mux_channel(channel)  # Select the current channel
        raw_value = adc.read_u16()  # Read ADC value
        
        # Turn on LED if voltage is 0, otherwise turn it off
        if raw_value < 500:
            np[channel] = (50, 50, 50)  # Example: Turn LED red when the sensor reading is 0
        else:
            np[channel] = (0, 0, 0)  # Turn off the corresponding LED
        
        print(f"Channel {channel}: Value = {raw_value}")
    
    np.write()  # Update NeoPixel LEDs
    sleep(0.1)  # Short delay for stable readings
