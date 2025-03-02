from machine import Pin
import neopixel
from utime import sleep
import random  # Import random for selecting a random stopping position

# Board LED config
Board_Spinner_LED_num_pixels = 48  # Total LEDs (42 Board + 6 Spinner LEDs)
Board_Spinner_LED_pin = Pin(22, Pin.OUT)
Board_Spinner_pixels = neopixel.NeoPixel(Board_Spinner_LED_pin, Board_Spinner_LED_num_pixels)

def playSpinnerSpinAndStop():
    delay = 0.01  # Starting delay
    spinner_start = 42  # Index where spinner LEDs start
    total_spinner_leds = 6  # Number of spinner LEDs
    random_stop = random.randint(0, total_spinner_leds - 1)  # Choose a random stopping position
    slowing_factor = 0.01  # How much to increase the delay each time
    current_led = 0  # Start at the first spinner LED

    while delay < 0.5:  # Gradually slow down
        # Turn off all spinner LEDs
        for j in range(total_spinner_leds):
            Board_Spinner_pixels[spinner_start + j] = (0, 0, 0)

        # Light up the current spinner LED
        Board_Spinner_pixels[spinner_start + current_led] = (round(255/4), 0, 0)
        Board_Spinner_pixels.write()
        sleep(delay)

        # Move to the next spinner LED
        current_led = (current_led + 1) % total_spinner_leds

        # Gradually increase the delay
        delay += slowing_factor

    # After slowing down, ensure it stops at the random position
    while current_led != random_stop:
        # Turn off all spinner LEDs
        for j in range(total_spinner_leds):
            Board_Spinner_pixels[spinner_start + j] = (0, 0, 0)

        # Light up the current spinner LED
        Board_Spinner_pixels[spinner_start + current_led] = (round(255/4), 0, 0)
        Board_Spinner_pixels.write()
        sleep(delay)

        # Move to the next spinner LED
        current_led = (current_led + 1) % total_spinner_leds

    # Keep the final spinner LED lit to indicate the stop
    for j in range(total_spinner_leds):
        Board_Spinner_pixels[spinner_start + j] = (0, 0, 0)
    Board_Spinner_pixels[spinner_start + random_stop] = (0, round(255/4), 0)  # Final LED is green
    Board_Spinner_pixels.write()

    return random_stop  # Return the stopping position


def main():
    print("Spinning...")
    stopping_position = playSpinnerSpinAndStop()
    print(f"Spinner stopped at position: {stopping_position}")


main()
