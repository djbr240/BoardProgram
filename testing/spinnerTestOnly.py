from machine import Pin, ADC
import neopixel
from utime import sleep
import random

# Spinner LED config
Board_Spinner_LED_num_pixels = 6  # Only 6 spinner LEDs
Board_Spinner_LED_pin = Pin(22, Pin.OUT)
Board_Spinner_pixels = neopixel.NeoPixel(Board_Spinner_LED_pin, Board_Spinner_LED_num_pixels)

# Define MUX3 select pins
MUX3_select_pins = [
    Pin(12, Pin.OUT),  # S0
    Pin(13, Pin.OUT),  # S1
    Pin(14, Pin.OUT),  # S2
    Pin(15, Pin.OUT),  # S3
]

# ADC for MUX3
ADC2_MUX3 = ADC(Pin(28))
button_threshold = 500  # Adjust as needed for your button logic

# Define LED colors
LED_COLORS = {
    0: (255, 255, 255),  # White
    1: (0, 0, 255),      # Blue
    2: (0, 0, 255),      # Blue
    3: (255, 255, 0),    # Yellow
    4: (0, 0, 255),      # Blue
    5: (0, 0, 255)       # Blue
}


# Function to select a channel on MUX
def select_mux_channel(mux_pins, channel):
    for i, pin in enumerate(mux_pins):
        pin.value((channel >> i) & 1)


# Check if the spinner button is pressed
def is_spinner_button_pressed():
    select_mux_channel(MUX3_select_pins, 15)  # Select Channel 15
    #print(ADC2_MUX3.read_u16())
    return ADC2_MUX3.read_u16() < button_threshold


# Spinner function
# Spinner function
def playSpinnerSpinAndStop():
    delay = 0.01  # Starting delay
    total_spinner_leds = Board_Spinner_LED_num_pixels  # Total spinner LEDs
    random_stop = random.randint(0, total_spinner_leds - 1)  # Choose a random stopping position
    slowing_factor = 0.01  # How much to increase the delay each time
    current_led = 0  # Start at the first spinner LED

    # Gradually slow down while spinning
    while delay < 0.2:
        # Turn off all LEDs
        for j in range(total_spinner_leds):
            Board_Spinner_pixels[j] = (0, 0, 0)

        # Light up the current spinner LED using the color from LED_COLORS
        Board_Spinner_pixels[current_led] = LED_COLORS.get(current_led, (255, 0, 0))  # Default to red if not in dict
        Board_Spinner_pixels.write()
        sleep(delay)

        # Move to the next spinner LED
        current_led = (current_led + 1) % total_spinner_leds

        # Gradually increase the delay
        delay += slowing_factor

    # Ensure the spinner stops at the random position
    while current_led != random_stop:
        # Turn off all LEDs
        for j in range(total_spinner_leds):
            Board_Spinner_pixels[j] = (0, 0, 0)

        # Light up the current spinner LED using the color from LED_COLORS
        Board_Spinner_pixels[current_led] = LED_COLORS.get(current_led, (255, 0, 0))  # Default to red if not in dict
        Board_Spinner_pixels.write()
        sleep(delay)

        # Move to the next spinner LED
        current_led = (current_led + 1) % total_spinner_leds

    # Handle the final spinner stop actions
    for j in range(total_spinner_leds):
        Board_Spinner_pixels[j] = (0, 0, 0)  # Turn off all LEDs

    # Determine behavior based on the stopping position
    if random_stop == 0:
        # Make LED white
        Board_Spinner_pixels[random_stop] = LED_COLORS[random_stop]
        Board_Spinner_pixels.write()
        return None
    elif random_stop in {1, 4}:
        # Make LED blue and blink 2 times, return 2
        for _ in range(2):
            Board_Spinner_pixels[random_stop] = LED_COLORS[random_stop]
            Board_Spinner_pixels.write()
            sleep(0.3)
            Board_Spinner_pixels[random_stop] = (0, 0, 0)
            Board_Spinner_pixels.write()
            sleep(0.3)
        return 2
    elif random_stop == 2:
        # Make LED blue and blink 4 times, return 4
        for _ in range(4):
            Board_Spinner_pixels[random_stop] = LED_COLORS[random_stop]
            Board_Spinner_pixels.write()
            sleep(0.3)
            Board_Spinner_pixels[random_stop] = (0, 0, 0)
            Board_Spinner_pixels.write()
            sleep(0.3)
        return 4
    elif random_stop == 3:
        # Make LED yellow
        Board_Spinner_pixels[random_stop] = LED_COLORS[random_stop]
        Board_Spinner_pixels.write()
        return None
    elif random_stop == 5:
        # Make LED blue and blink 3 times, return 3
        for _ in range(3):
            Board_Spinner_pixels[random_stop] = LED_COLORS[random_stop]
            Board_Spinner_pixels.write()
            sleep(0.3)
            Board_Spinner_pixels[random_stop] = (0, 0, 0)
            Board_Spinner_pixels.write()
            sleep(0.3)
        return 3


# Main function
def main():
    print("Waiting for button press to spin...")
    while True:
        if is_spinner_button_pressed():
            print("Button pressed! Spinning...")
            result = playSpinnerSpinAndStop()
            print(f"Spinner result: {result}")
            sleep(0.5)  # Debounce delay to avoid multiple spins


main()
