from machine import ADC, Pin
from neopixel import NeoPixel
from time import sleep

# Initialize ADC for MUX SIG output
adc = ADC(Pin(28))  # ADC pin connected to the SIG pin of all MUXes

# GPIO pins for MUX select lines (shared by all MUXes)
select_pins = [
    Pin(10, Pin.OUT),  # S0
    Pin(11, Pin.OUT),  # S1
    Pin(12, Pin.OUT),  # S2
    Pin(13, Pin.OUT),  # S3
]

# NeoPixel configuration
NUM_PIXELS = 10  # Total LEDs for 42 sensors
np_pin = Pin(22, Pin.OUT)  # Pin connected to NeoPixel data line
np = NeoPixel(np_pin, NUM_PIXELS)

# ADC reference voltage (default is 3.3V)
V_REF = 3.3

def select_mux_channel(channel):
    """Select the MUX channel to read from."""
    # Set the select lines for the desired channel
    for i, pin in enumerate(select_pins):
        pin.value((channel >> i) & 1)

while True:
    for sensor_id in range(NUM_PIXELS):  # Loop through all 42 sensors
        channel = sensor_id % 16  # Determine the channel within the MUX

        select_mux_channel(channel)  # Select the channel
        raw_value = adc.read_u16()  # Read ADC value
        #voltage = (raw_value / 65535) * V_REF  # Convert raw value to voltage
        
        # Turn on LED if voltage is 0, otherwise turn it off
        if raw_value <= 14000:
            np[sensor_id] = (55, 0, 0)  # Turn LED red for voltage 0
        else:
            np[sensor_id] = (0, 0, 0)  # Turn off the corresponding LED
        
        print(f"Sensor {sensor_id}: Voltage = {raw_value:.2f} V")
    
    np.write()  # Update NeoPixel LEDs
    sleep(0.1)  # Short delay for stable readings
