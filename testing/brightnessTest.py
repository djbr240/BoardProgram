from machine import Pin, ADC
import time
import neopixel
import _thread

def set_mux_channel(channel):
    """Sets the multiplexer channel by controlling the select pins."""
    binary_channel = [(channel >> i) & 1 for i in range(3, -1, -1)]
    for pin, value in zip(select_pins, binary_channel):
        pin.value(value)

def read_pot():
    """Reads the potentiometer value from the multiplexer and scales it to 1-100."""
    set_mux_channel(0)  # Only one component is connected on channel 0
    raw_value = adc.read_u16()  # Read the ADC value (0-65535)
    return round((raw_value / 65535) * 99 + 1)  # Scale to 1-100

def set_neopixel_brightness(value):
    """Sets the brightness of all NeoPixels based on the potentiometer reading."""
    brightness = int((value / 100) * 255)  # Scale to 0-255 range
    for i in range(26):
        np[i] = (brightness, brightness, brightness)  # Set to white with scaled brightness
    np.write()

def led_control_task():
    """Runs on the second core to control LED brightness based on potentiometer reading."""
    while True:
        pot_value = read_pot()
        print("Potentiometer Value:", pot_value)
        set_neopixel_brightness(pot_value)
        time.sleep(0.1)

# Define the select pins for the multiplexer
select_pins = [Pin(pin, Pin.OUT) for pin in [13, 12, 11, 10]]

# Define ADC0 for reading values from the multiplexer
adc = ADC(26)  # ADC0 is connected to GPIO26 on the Pi Pico 2

# Define 26 NeoPixel LEDs on GPIO23
np = neopixel.NeoPixel(Pin(22), 26)  # 26 NeoPixel LEDs

# Start LED control task on the second core
_thread.start_new_thread(led_control_task, ())

# Main program runs on core 0 and changes an LED color
color_index = 0
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

while True:
    np[0] = colors[color_index]  # Change first LED to a new color
    np.write()
    color_index = (color_index + 1) % len(colors)
    print("Main program changing LED color...")
    time.sleep(1)
