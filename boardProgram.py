# Clue Jr Main Board Program
# Programmer: Daniel Breidenbach
# University of Kentucky College of Engineering
# Electrical and Computer Engineering Department
# Started: November 2024, Finalized: TBD

# This program is meant to be run on the Raspberry Pi Pico 2

from machine import ADC, Pin
import neopixel
from utime import sleep
import utime
from mfrc522 import MFRC522
import random

################################################################
#   Configuration

# This is the only place where Pins, number of LEDs, threshold values, etc are defined.

# Board LED config
Board_Spinner_LED_num_pixels = 48 # 42 Board LEDs and 6 Spinner LEDs = 48
Board_Spinner_LED_pin = Pin(22, Pin.OUT)
Board_Spinner_pixels = neopixel.NeoPixel(Board_Spinner_LED_pin, Board_Spinner_LED_num_pixels)

# Panel LED config (there's 6 panels, with only room for 5 of them)
PanelLED1_num_pixels = 26
PanelLED1_pin = Pin(21, Pin.OUT)
Panel1_pixels = neopixel.NeoPixel(PanelLED1_pin, PanelLED1_num_pixels)

PanelLED2_num_pixels = 26
PanelLED2_pin = Pin(20, Pin.OUT)
Panel2_pixels = neopixel.NeoPixel(PanelLED2_pin, PanelLED2_num_pixels)

PanelLED3_num_pixels = 26
PanelLED3_pin = Pin(19, Pin.OUT)
Panel3_pixels = neopixel.NeoPixel(PanelLED3_pin, PanelLED3_num_pixels)

PanelLED4_num_pixels = 26
PanelLED4_pin = Pin(18, Pin.OUT)
Panel4_pixels = neopixel.NeoPixel(PanelLED4_pin, PanelLED4_num_pixels)

# We currently don't have a solution for having a 5th panel (out of pins)
#PanelLED5_num_pixels = 26
#PanelLED5_pin = Pin(17, Pin.OUT)
#Panel5_pixels = neopixel.NeoPixel(PanelLED5_pin, PanelLED5_num_pixels)

# We currently don't have a solution for having a 6th panel (out of pins)
#PanelLED6_num_pixels = 26
#PanelLED6_pin = Pin(26, Pin.OUT)
#Panel6_pixels = neopixel.NeoPixel(PanelLED6_pin, PanelLED6_num_pixels)


# Mux configuration

hall_sensor_threshold = 500
button_threshold = 500

# Initialize ADC for MUX SIG output
ADC0_MUX1 = ADC(Pin(26))  # ADC pin connected to the MUX SIG output
ADC1_MUX2 = ADC(Pin(27))
ADC2_MUX3 = ADC(Pin(28))

# GPIO pins for MUX select lines
MUX1_select_pins = [
    Pin(4, Pin.OUT),  # S0
    Pin(5, Pin.OUT),  # S1
    Pin(6, Pin.OUT),  # S2
    Pin(7, Pin.OUT),  # S3
]

MUX2_select_pins = [
    Pin(8, Pin.OUT),  # S0
    Pin(9, Pin.OUT),  # S1
    Pin(10, Pin.OUT),  # S2
    Pin(11, Pin.OUT),  # S3
]

MUX3_select_pins = [
    Pin(12, Pin.OUT),  # S0
    Pin(13, Pin.OUT),  # S1
    Pin(14, Pin.OUT),  # S2
    Pin(15, Pin.OUT),  # S3
]

# RFID configuration
RFIDreader = MFRC522(spi_id=0,sck=2,miso=0,mosi=3,cs=1,rst=16)

################################################################
# Piece identification, graph, and LED locations on the board and panels

# Graph represented as an adjacency list
# Left side is the source, in [] is the source's neighbors
graph = {
    0: [10],
    1: [9],
    2: [3, 8],
    3: [2, 8],
    4: [7],
    5: [6],
    6: [7],
    7: [4, 6, 8, 15],
    8: [2, 3, 7, 14],
    9: [14],
    10: [0, 11],
    11: [10, 13],
    12: [13],
    13: [11, 14, 20],
    14: [8, 9, 13, 15, 21],
    15: [7, 14, 16, 19],
    16: [15, 17],
    17: [16],
    18: [19, 28, 29],
    19: [15, 18, 27],
    20: [13, 21, 22, 23],
    21: [14, 20, 22, 25],
    22: [20, 21, 23],
    23: [20, 22],
    24: [25, 38],
    25: [21, 24, 26, 37],
    26: [25, 27],
    27: [19, 26, 28, 31, 33],
    28: [18, 27, 29],
    29: [18, 28],
    30: [31],
    31: [27, 33],
    32: [33],
    33: [27, 31, 32, 35],
    34: [35, 37],
    35: [33, 34, 36],
    36: [35, 37],
    37: [25, 34, 36],
    38: [24, 39],
    39: [38],
    40: [37],
    41: [33]
}

# Yellow spaces positions
yellow_space = [0, 4, 23, 29, 32, 36]

# White spaces positions
white_space = [2, 17, 39]

# Start spaces
# A dictionary where the character and the position is linked together
character_start_spaces = {
    "Blue": 30,
    "Purple": 5,
    "Red": 1,
    "Yellow": 12,
    "Pink" : 40,
    "Green" : 41
}

# Furniture spaces
furniture_start_spaces = {
    "pooltable": 29,
    "desk": 4,
    "chair": 0,
    "piano": 36,
    "plant": 32,
    "diningtable": 23
}

# Dictionary for the character pieces and the RFID links
# All zeros as a placeholder for now
pieceRFID = {
    "Blue": 40551758664916996,
    "Purple": 40551758664917252,
    "Red": 40551758664917508,
    "Yellow": 40551758664917764,
    "Pink": 40551758664918020,
    "Green": 40551758664847108,
}

furnitureRFID = {
    "pooltable": 40551758664847364,
    "desk": 40551758664847620,
    "chair":40551758664847876,
    "piano": 40551758664848132,
    "plant": 40551758664856068,
    "diningtable": 40551758664856324
}

# The LED position for the clue panels
cluePanelLED = {
    #characters
    "Yellow": 19,
    "Red": 20,
    "Green": 21,
    "Blue": 22,
    "Pink": 23,
    "Purple": 24,
    
    #toys
    "trex": 18,
    "racecar": 17,
    "teddybear": 16,
    "mr_potatohead": 15,
    "xylophone": 14,
    "ball": 13,
    
    #furniture
    "pooltable": 7,
    "desk": 8,
    "chair": 9,
    "piano": 10,
    "plant": 11,
    "diningtable": 12,
    
    #time
    "11": 6,
    "12": 5,
    "1": 4,
    "2": 3,
    "3": 2,
    "4": 1,
    "5": 0
}

################################################################

# This is the Player class, where all of the information for each player is created
class Player:
    def __init__(self, pieceID, position=0, panel=None):
        """
        Initialize a player.
        :param pieceID: The identifier for the player's piece.
        :param position: The starting position of the player on the board.
        :param panel: The LED panel assigned to the player.
        """
        self.pieceID = pieceID  # The piece the player is using
        self.position = position  # Tracks the player's current position on the board
        self.clues_found = []  # List of clues collected by the player
        self.panel = panel  # The LED panel assigned to the player
        self.panel_leds_lit = []  # List of LEDs lit on the panel

    def assign_panel(self, panel):
        """Assign a panel to the player."""
        self.panel = panel

    def set_piece(self, piece):
        """Set the player's piece after the first move."""
        if self.pieceID is None:  # Piece can only be set once
            self.pieceID = piece

    def collect_clue(self, clue):
        """Add a clue to the player's collection."""
        self.clues_found.append(clue)

    def add_clue(self, clue):
        """Add a clue (integer) to the player's list of cluesFound and update the panel."""
        self.clues_found.append(clue)
        self.update_panel()

    def move(self, new_position):
        """Update the player's position."""
        self.position = new_position
        self.update_panel()  # Light up the new position on the panel

    def update_position(self, new_position=None):
        """
        Move the player to a new position and update the panel.
        :param new_position: The new position to move to, optional if using sensor_reader.
        """
        if new_position is not None:
            self.position = new_position
        else:
            print("Error: No new position provided.")
        
        self.update_panel()  # Update the LED panel after moving

    def get_position(self):
        """Get the player's current position."""
        return self.position

    def update_panel(self):
        """Update the player's panel by lighting up the player's current position."""
        if self.panel is not None:
            # Ensure we only light up the player's position on the panel
            if self.position not in self.panel_leds_lit:
                self.panel_leds_lit.append(self.position)
                # Light up the position on the panel
                light_up_position(self.position)  # Use your existing function to light up the position
        else:
            print("No panel assigned to this player.")

    def display_panel_status(self):
        """Display the status of the player's panel."""
        print(f"Player {self.pieceID}'s panel LEDs: {self.panel_leds_lit}")

    def __str__(self):
        return f"Player {self.pieceID} is at position {self.position} with clues {self.clues_found}"

    
    # End player class
################################################################

################################################################
# The following functions are LED animations

# Define LED colors for the sequence on the spinner
LED_COLORS = {
    0: (255, 255, 255),  # White
    1: (0, 0, 255),      # Blue
    2: (0, 0, 255),      # Blue
    3: (255, 255, 0),    # Yellow
    4: (0, 0, 255),      # Blue
    5: (0, 0, 255)       # Blue
}

def is_spinner_button_pressed():
    select_mux_channel(MUX3_select_pins, 15)  # Select Channel 15
    #print(ADC2_MUX3.read_u16())
    return ADC2_MUX3.read_u16() < button_threshold

# Randomly generate a number, while also making a spinning animation. Return what the spinner lands on
def playSpinnerSpinAndStop():
    delay = 0.01  # Starting delay
    spinner_start_index = 42  # First index of spinner LEDs
    total_spinner_leds = 6  # Total spinner LEDs
    random_stop = random.randint(0, total_spinner_leds - 1)  # Random stopping position within spinner LEDs
    slowing_factor = 0.01  # How much to increase the delay each time
    current_led = 0  # Start at the first spinner LED

    # Gradually slow down while spinning
    while delay < 0.2:
        # Turn off all spinner LEDs
        for j in range(total_spinner_leds):
            Board_Spinner_pixels[spinner_start_index + j] = (0, 0, 0)

        # Light up the current spinner LED using the color from LED_COLORS
        Board_Spinner_pixels[spinner_start_index + current_led] = LED_COLORS.get(current_led, (255, 0, 0))  # Default red
        Board_Spinner_pixels.write()
        sleep(delay)

        # Move to the next spinner LED
        current_led = (current_led + 1) % total_spinner_leds

        # Gradually increase the delay
        delay += slowing_factor

    # Ensure the spinner stops at the random position
    while current_led != random_stop:
        # Turn off all spinner LEDs
        for j in range(total_spinner_leds):
            Board_Spinner_pixels[spinner_start_index + j] = (0, 0, 0)

        # Light up the current spinner LED
        Board_Spinner_pixels[spinner_start_index + current_led] = LED_COLORS.get(current_led, (255, 0, 0))  # Default red
        Board_Spinner_pixels.write()
        sleep(delay)

        # Move to the next spinner LED
        current_led = (current_led + 1) % total_spinner_leds

    # Handle the final spinner stop actions
    for j in range(total_spinner_leds):
        Board_Spinner_pixels[spinner_start_index + j] = (0, 0, 0)  # Turn off all LEDs

    # Determine behavior based on the stopping position
    final_led_index = spinner_start_index + random_stop
    if random_stop == 0:
        # Make LED white and return "white"
        Board_Spinner_pixels[final_led_index] = LED_COLORS[random_stop]
        Board_Spinner_pixels.write()
        return "white"
    elif random_stop in {1, 4}:
        # Make LED blue and blink 2 times, return 2
        for _ in range(2):
            Board_Spinner_pixels[final_led_index] = LED_COLORS[random_stop]
            Board_Spinner_pixels.write()
            sleep(0.3)
            Board_Spinner_pixels[final_led_index] = (0, 0, 0)
            Board_Spinner_pixels.write()
            sleep(0.3)
        return 2
    elif random_stop == 2:
        # Make LED blue and blink 4 times, return 4
        for _ in range(4):
            Board_Spinner_pixels[final_led_index] = LED_COLORS[random_stop]
            Board_Spinner_pixels.write()
            sleep(0.3)
            Board_Spinner_pixels[final_led_index] = (0, 0, 0)
            Board_Spinner_pixels.write()
            sleep(0.3)
        return 4
    elif random_stop == 3:
        # Make LED yellow and return "yellow"
        Board_Spinner_pixels[final_led_index] = LED_COLORS[random_stop]
        Board_Spinner_pixels.write()
        return "yellow"
    elif random_stop == 5:
        # Make LED blue and blink 3 times, return 3
        for _ in range(3):
            Board_Spinner_pixels[final_led_index] = LED_COLORS[random_stop]
            Board_Spinner_pixels.write()
            sleep(0.3)
            Board_Spinner_pixels[final_led_index] = (0, 0, 0)
            Board_Spinner_pixels.write()
            sleep(0.3)
        return 3

################################################################

# This function goes through every channel in the MUXs and checks all readings from the Hall Sensors
# It then returns a list of all the Hall Sensors that detected a magnetic presence
# This function will need to be called every time the position needs to be updated
# Function to select a channel on a MUX

def select_mux_channel(mux_pins, channel):
    for i, pin in enumerate(mux_pins):
        pin.value((channel >> i) & 1)  # Set the pin value based on the channel bits
        
def read_hall_sensors():
    """
    Reads all 42 Hall sensors (across 3 MUXs), checks if their ADC value is below the threshold, 
    and returns a list of sensor indices where a magnetic presence is detected.
    """
    
    detected_positions = []  # List to store detected positions

    # Iterate through MUX1 channels (0–15)
    for channel in range(16):
        select_mux_channel(MUX1_select_pins, channel)
        adc_value = ADC0_MUX1.read_u16()  # Read ADC value
        if adc_value < hall_sensor_threshold:
            detected_positions.append(channel)
    
    # Iterate through MUX2 channels (16–31)
    for channel in range(16):
        select_mux_channel(MUX2_select_pins, channel)
        adc_value = ADC1_MUX2.read_u16()  # Read ADC value
        if adc_value < hall_sensor_threshold:
            detected_positions.append(channel + 16)  # Offset by 16 for MUX2

    # Iterate through MUX3 channels (32–41)
    for channel in range(10):  # Only process channels 0–9 on MUX3
        select_mux_channel(MUX3_select_pins, channel)
        adc_value = ADC2_MUX3.read_u16()  # Read ADC value
        if adc_value < hall_sensor_threshold:
            detected_positions.append(channel + 32)  # Offset by 32 for MUX3

    return detected_positions  # Return the list of detected positions


# This function takes the previous reading from read_hall_sensors(), calls read_hall_sensors() again and compares them to find the difference from the last reading

    
                
# Since for MUX3 channels 10-15, we are using those for Potentiometer and Button readings, we need a function to go through those MUX3 Channels
# We want to have Potentiometer and Buttons separated since they're doing significantly different functions
# This is a map of those assignments:
# MUX3 Channel 10 = Potentiometer
# MUX3 Channel 11 = Button1
# MUX3 Channel 12 = Button2
# MUX3 Channel 13 = Button3
# MUX3 Channel 14 = Button4
# MUX3 Channel 15 = Spinner Button
def readPotentiometer():
    # Read MUX3 Channel 15
    select_mux_channel(MUX3_select_pins, 10)
    adc_value = ADC2_MUX3.read_u16()  # Read ADC value
    return adc_value  # Return the Potentiometer value

# Reads MUX3 Channels 10-15 to see if a button is pressed. Return the button number pressed
def readButtons():
    # Read MUX3 Channels 11-15
    select_mux_channel(MUX3_select_pins, 11)
    button1_pressed = bool(ADC2_MUX3.read_u16() < button_threshold)
    
    select_mux_channel(MUX3_select_pins, 12)
    button2_pressed = bool(ADC2_MUX3.read_u16() < button_threshold)
    
    select_mux_channel(MUX3_select_pins, 13)
    button3_pressed = bool(ADC2_MUX3.read_u16() < button_threshold)
    
    select_mux_channel(MUX3_select_pins, 14)
    button4_pressed = bool(ADC2_MUX3.read_u16() < button_threshold)
    

    # This is for the spinner button
    #select_mux_channel(MUX3_select_pins, 15)
    #button5_pressed = bool(ADC2_MUX3.read_u16() < button_threshold)
    
    buttonPressed = 0
    if button1_pressed: buttonPressed = 1
    if button2_pressed: buttonPressed = 2
    if button3_pressed: buttonPressed = 3
    if button4_pressed: buttonPressed = 4
    #if button5_pressed: buttonPressed = 5
    
    
    return buttonPressed

def readRFID():
    while True:
        # Read RFID and print to console
        RFIDreader.init()
        (stat, tag_type) = RFIDreader.request(RFIDreader.REQIDL)
        if stat == RFIDreader.OK:
            (stat, uid) = RFIDreader.SelectTagSN()
            if stat == RFIDreader.OK:
                card = int.from_bytes(bytes(uid),"little",False)
                print("CARD ID: "+str(card))
                return card
                break

def identify_rfid(card, pieceRFID, furnitureRFID):
    # Check character pieces
    for name, rfid_value in pieceRFID.items():
        if card == rfid_value:
            return name

    # Check furniture pieces
    for name, rfid_value in furnitureRFID.items():
        if card == rfid_value:
            return name

    # If not found in either dictionary
    return None




def displayRFID(name,pixels):

    brightness = int(200)
    if name == "Yellow":
        item = 19
    
    if name == "Red":
        item = 20

    if name == "Green":
        item = 21

    if name == "Blue":
        item = 22

    if name == "Pink":
        item = 23

    if name == "Purple":
        item = 24

    if name == "piano":
        item = 0

    if (item == 0):

        person = 0
        toy = 0
        time = 0

        mustard = 0

        scarlett = 0

        green = 0

        peacock = 0

        orchid = 0

        plum = 0

        rex = 0

        car = 0

        bear = 0

        potato = 0

        xylophone = 0

        ball = 0

        pool = 0

        desk = 0

        chair = 0

        piano = 0

        plant = 0

        dining = 0

        time11 = 0

        time12 = 0

        time1 = 0

        time2 = 0

        time3 = 0

        time4 = 0

        time5 = 0

        pixels.fill ((0,0,0))


    # Check the input and set corresponding 
    # piece to 1 if correct person has not been found
    if (item == 1 and person == 0):
        mustard = 1

    if (item == 2 and person == 0):
        scarlett = 1

    if (item == 3 and person == 0):
        green = 1

    if (item == 4 and person == 0):
        peacock = 1

    if (item == 5 and person == 0):
        orchid = 1

    if (item == 6 and person == 0):
        plum = 1

    # Check the input and set corresponding 
    # piece to 1 if correct toy has not been found
    if (item == 7 and toy == 0):
        rex = 1

    if (item == 8 and toy == 0):
        car = 1

    if (item == 9 and toy == 0):
        bear = 1

    if (item == 10 and toy == 0):
        potato = 1

    if (item == 11 and toy == 0):
        xylophone = 1

    if (item == 12 and toy == 0):
        ball = 1

    if (item == 13):
        pool = 1

    if (item == 14):
        desk = 1

    if (item == 15):
        chair = 1

    if (item == 16):
        piano = 1

    if (item == 17):
        plant = 1

    if (item == 18):
        dining = 1

    # Check the input and set corresponding 
    # piece to 1 if correct time has not been found
    if (item == 19 and time == 0):
        time11 = 1

    if (item == 20 and time == 0):
        time12 = 1

    if (item == 21 and time == 0):
        time1 = 1

    if (item == 22 and time == 0):
        time2 = 1

    if (item == 23 and time == 0):
        time3 = 1

    if (item == 24 and time == 0):
        time4 = 1

    if (item == 25 and time == 0):
        time5 = 1


    # The following lights up each corresponding LED red
    # depending on if the item is set to 1

    if (mustard == 1):
        pixels[19] = (brightness,0,0)

    if (scarlett == 1):
        pixels[20] = (brightness,0,0)

    if (green == 1):
        pixels[21] = (brightness,0,0)

    if (peacock == 1):
        pixels[22] = (brightness,0,0)

    if (orchid == 1):
        pixels[23] = (brightness,0,0)

    if (plum == 1):
        pixels[24] = (brightness,0,0)

    if (rex == 1):
        pixels[18] = (brightness,0,0)

    if (car == 1):
        pixels[17] = (brightness,0,0)

    if (bear == 1):
        pixels[16] = (brightness,0,0)

    if (potato == 1):
        pixels[15] = (brightness,0,0)

    if (xylophone == 1):
        pixels[14] = (brightness,0,0)

    if (ball == 1):
        pixels[13] = (brightness,0,0)

    if (pool == 1):
        pixels[7] = (brightness,0,0)

    if (desk == 1):
        pixels[8] = (brightness,0,0)

    if (chair == 1):
        pixels[9] = (brightness,0,0)

    if (piano == 1):
        pixels[10] = (brightness,0,0)

    if (plant == 1):
        pixels[11] = (brightness,0,0)

    if (dining == 1):
        pixels[12] = (brightness,0,0)

    if (time11 == 1):
        pixels[6] = (brightness,0,0)

    if (time12 == 1):
        pixels[5] = (brightness,0,0)

    if (time1 == 1):
        pixels[4] = (brightness,0,0)

    if (time2 == 1):
        pixels[3] = (brightness,0,0)

    if (time3 == 1):
        pixels[2] = (brightness,0,0)

    if (time4 == 1):
        pixels[1] = (brightness,0,0)

    if (time5 == 1):
        pixels[0] = (brightness,0,0)


    # The following lights the LED green
    # when it is the last person left
    # and sets person to 1 to block previous code from making it red

    if (mustard==0 and scarlett==1 and green==1 and peacock==1 and orchid==1 and plum==1):
        pixels[19] = (0,brightness,0)
        person = 1

    if (mustard==1 and scarlett==0 and green==1 and peacock==1 and orchid==1 and plum==1):
        pixels[20] = (0,brightness,0)
        person = 1

    if (mustard==1 and scarlett==1 and green==0 and peacock==1 and orchid==1 and plum==1):
        pixels[21] = (0,brightness,0)
        person = 1

    if (mustard==1 and scarlett==1 and green==1 and peacock==0 and orchid==1 and plum==1):
        pixels[22] = (0,brightness,0)
        person = 1

    if (mustard==1 and scarlett==1 and green==1 and peacock==1 and orchid==0 and plum==1):
        pixels[23] = (0,brightness,0)
        person = 1

    if (mustard==1 and scarlett==1 and green==1 and peacock==1 and orchid==1 and plum==0):
        pixels[24] = (0,brightness,0)
        person = 1


    # The following lights the LED green
    # when it is the last toy left
    # and sets toy to 1 to block previous code from making it red
    if (rex==0 and car==1 and bear==1 and potato==1 and xylophone==1 and ball==1):
        pixels[18] = (0,brightness,0)
        toy = 1

    if (rex==1 and car==0 and bear==1 and potato==1 and xylophone==1 and ball==1):
        pixels[17] = (0,brightness,0)
        toy = 1

    if (rex==1 and car==1 and bear==0 and potato==1 and xylophone==1 and ball==1):
        pixels[16] = (0,brightness,0)
        toy = 1

    if (rex==1 and car==1 and bear==1 and potato==0 and xylophone==1 and ball==1):
        pixels[15] = (0,brightness,0)
        toy = 1

    if (rex==1 and car==1 and bear==1 and potato==1 and xylophone==0 and ball==1):
        pixels[14] = (0,brightness,0)
        toy = 1

    if (rex==1 and car==1 and bear==1 and potato==1 and xylophone==1 and ball==0):
        pixels[13] = (0,brightness,0)
        toy = 1


    # The following lights the LED green
    # when it is the last time left
    # and sets time to 1 to block previous code from making it red
    if (time11==0 and time12==1 and time1==1 and time2==1 and time3==1 and time4==1 and time5==1):
        pixels[6] = (0,brightness,0)
        time = 1

    if (time11==1 and time12==0 and time1==1 and time2==1 and time3==1 and time4==1 and time5==1):
        pixels[5] = (0,brightness,0)
        time = 1

    if (time11==1 and time12==1 and time1==0 and time2==1 and time3==1 and time4==1 and time5==1):
        pixels[4] = (0,brightness,0)
        time = 1

    if (time11==1 and time12==1 and time1==1 and time2==0 and time3==1 and time4==1 and time5==1):
        pixels[3] = (0,brightness,0)
        time = 1

    if (time11==1 and time12==1 and time1==1 and time2==1 and time3==0 and time4==1 and time5==1):
        pixels[2] = (0,brightness,0)
        time = 1

    if (time11==1 and time12==1 and time1==1 and time2==1 and time3==1 and time4==0 and time5==1):
        pixels[1] = (0,brightness,0)
        time = 1

    if (time11==1 and time12==1 and time1==1 and time2==1 and time3==1 and time4==1 and time5==0):
        pixels[0] = (0,brightness,0)
        time = 1

    #playerturn = False

    item = 100
    pixels.write()  # Send the data to the NeoPixels
    sleep(0.1)  # Delay before updating colors again



    

# The pathfinder is basically a Breadth First Search algorithm.
# The only difference is that instead of finding the entire graph,
# we stop at the roll number.
def pathfinder(graph, start_node, roll_number):
    visited = set()  # To avoid revisiting nodes
    queue = [(start_node, 0)]  #store (node, depth)
    
    reachable = []  # List to append results from each loop
    
    while queue:
        current, depth = queue.pop(0)  # Dequeue
        if current not in visited:
            visited.add(current)
            if depth <= roll_number:
                reachable.append(current)
                # Add neighbors to the queue with incremented depth
                queue.extend((neighbor, depth + 1) for neighbor in graph.get(current, []))
    
    return reachable

# Use the pathfinder function to light up the path
def light_up_path(start_node, roll_number):
    # Find reachable spaces 
    reachable_spaces = pathfinder(graph, start_node, roll_number)
    print("Possible spaces:", reachable_spaces)

    # Display the reachable spaces with white pixels on the NeoPixels
    for i in range(len(reachable_spaces)):
        Board_Spinner_pixels[reachable_spaces[i]] = (0, 5, 0)
    Board_Spinner_pixels.write()  # Update the NeoPixels

# When this function is called, light up all the Yellow spaces.
# Loop through the yellow_space list and light up that LED
def light_up_yellow_spaces():
    for yellow_space in yellow_space:
        Board_Spinner_pixels[yellow_space] = (25, 25, 0)
    Board_Spinner_pixels.write()

# Same as light_up_yellow_spaces() but with the white spaces
def light_up_white_spaces():
    for white_space in white_space:
        Board_Spinner_pixels[white_space] = (25, 25, 25)
    Board_Spinner_pixels.write()
    
# For the setup process, this function lights up one of the LED positions
def light_up_position(position):
    if 0 <= position < len(Board_Spinner_pixels):
        # Turn off all LEDs first
        for i in range(len(Board_Spinner_pixels)):
            Board_Spinner_pixels[i] = (0, 0, 0)  # RGB values for "off"

        # Light up the specified position
        Board_Spinner_pixels[position] = (255, 255, 255)  # RGB values for "white" or a bright color
        Board_Spinner_pixels.write()  # Function to send data to the LED strip
        print(f"Position {position} lit up.")
    else:
        print(f"Error: Position {position} is out of range.")


def accusationSystem():
    # TODO

    # General structure of the accusation system

    # Wait for RFID scan 1
    # Wait for RFID scan 2
    # Wait for RFID scan 3
    # (make sure in general the the kinds of cards scanned are right, but it doesn't matter what order the cards are scanned in)
    # Check result and compare it to the answer
    # If correct
        # Break from function, return player number
    # If incorrect
        # Remove player from the game
        # Break from function, return 0

    print("Accusation System functional called...")
        
# When the device is turned on, test all of the LEDs on the board
def StartupProcess():
    # In sequence, from the first LED on the board, to the last LED on the board, then the final 6 LEDs in the spinner.
    # To do this, in a loop going through all Board_Spinner_pixels, turn on each Board_Spinner_pixels individually, then turn that pixel off.
    for i in range(len(Board_Spinner_pixels)):
        Board_Spinner_pixels[i] = (25, 25, 25)
        Board_Spinner_pixels.write()
        sleep(0.3)
        Board_Spinner_pixels[i] = (0, 0, 0)
        Board_Spinner_pixels.write()
        
    # This comment is a placeholder for other LED tests... TODO
    
        
# Function to help everyone test out the program with hardware
def testFunction():
    # Print options for the user
    print("Clueless board options:")
    print("1: Test board LEDs")
    print("2: Test panel LEDs")
    print("3: Test pathfinder")
    print("4: RFID options")
    print("5: Hall Sensor test")
    print("6: Test spinner")
    print("7: Button test")
    
    # Get user input
    user_input = input("Enter your choice: ")
    
    # Make a switch case for each option
    if user_input == "1":
        print("Testing board LEDs (5 seconds)...")
        # Light up all board LEDs (dim white)
        Board_Spinner_pixels.fill((25, 25, 25))
        Board_Spinner_pixels.write()
        sleep(5)
        Board_Spinner_pixels.fill((0, 0, 0))
        Board_Spinner_pixels.write()
        print("Test complete")
        
    elif user_input == "2":
        user_input = input("Enter what part of the panels you want to test: \n1. Flash all leds on \n2. Light up clue")

        if user_input == "1":
            print("Testing panel LEDs...")
            # Light up all panel LEDs
            Panel1_pixels.fill((25, 25, 25))
            Panel2_pixels.fill((25, 25, 25))
            Panel1_pixels.write()
            Panel2_pixels.write()
            sleep(1)
            Panel1_pixels.fill((0, 0, 0))
            Panel2_pixels.fill((0, 0, 0))
            Panel1_pixels.write()
            Panel2_pixels.write()

        if user_input == "2":
            print("Which panel?")
            if user_input == "1":
                user_input = input("Input which clue: ")
                print(f"Enabling led for clue: {user_input}")
                # Determine clue from dictionary
                while True:
                    # Fetch the corresponding position from the dictionary
                    if user_input in cluePanelLED:
                        Panel1_pixels[cluePanelLED[user_input]]
                        Panel1_pixels.write()
                        print(f"The {user_input} piece is at position {cluePanelLED[user_input]}")
                    else:
                        print("Invalid input. Please enter a valid name from the dictionary.")

            if user_input == "2":
                user_input = input("Input which clue: ")
                print(f"Enabling led for clue: {user_input}")
                # Determine clue from dictionary
                while True:
                    # Fetch the corresponding position from the dictionary
                    if user_input in cluePanelLED:
                        Panel2_pixels[cluePanelLED[user_input]]
                        Panel2_pixels.write()
                        print(f"The {user_input} piece is at position {cluePanelLED[user_input]}")
                    else:
                        print("Invalid input. Please enter a valid name from the dictionary.")
                
        
    elif user_input == "3":
        print("Enter the space number: ")
        space_number = int(input())
        print("Enter the roll number: ")
        roll_number = int(input())
        
        print("Lighting path (5 seconds)...")
        light_up_path(space_number, roll_number)
        #sleep(5)
        input("Press enter to continue")
        Board_Spinner_pixels.fill((0,0,0))
        Board_Spinner_pixels.write()
        print("Test complete")
        
    #Test RFID Functionality    
    elif user_input == "4":

        print("RFID Reading...")
        
        #if user_input == "1":
        while True:
            card = readRFID()

            item_name = identify_rfid(card, pieceRFID, furnitureRFID)

            if item_name:
                print(f"Identified {item_name}!")
            
                
            elif card == 17611714:
                print("Test is Tag 1")
            elif card == 17450884:
                print("Test is Tag 2")
            elif card == 4199895683:
                print("Test is Tag 3")
            elif card == 53290530:
                print("Test is Card 1")
            elif card == 3841076787:
                print("Test is Card 2")
            elif card == 52866437:
                print("Test is Card 3")
            else:
                print("Unrecognized RFID: " + str(card))

    elif user_input == "5":
        while True:
            print("Testing Hall Sensors...")
            # Read Hall sensors and get detected positions
            detected_positions = read_hall_sensors()
            print("Detected positions:", detected_positions)

            # Test LEDs based on detected positions
            for i in range(len(Board_Spinner_pixels)):
                if i in detected_positions:
                    Board_Spinner_pixels[i] = (0, 255, 0)  # Green for detected positions
                else:
                    Board_Spinner_pixels[i] = (0, 0, 0)  # Off if not detected
            Board_Spinner_pixels.write()
            sleep(0.1)

    elif user_input == "6":
        print("Waiting for button press to spin...")
        while True:
            btnInput = readButtons()
            print(readButtons())
            if btnInput == 5:
                print("Button pressed! Spinning...")
                result = playSpinnerSpinAndStop()
                print(f"Spinner result: {result}")
                sleep(0.5)  # Debounce delay to avoid multiple spins

    elif user_input == "7":
        print("Waiting for button press to light up position...")
        
        previous_btn_state = None  # To track the previous state of the button

        while True:
            btnInput = readButtons()

            # Check for a transition from "not pressed" (None or 0) to "pressed" (non-zero value)
            if btnInput and btnInput != previous_btn_state:
                print(f"Button pressed: {btnInput}")
            
            # Update the previous button state
            previous_btn_state = btnInput


                    
            
    else:
        print("Invalid choice. Please try again.")



########################################################################

# Setup process
def GameSetup():
    """
    Sets up the game by assigning players to their panels and initializing their positions 
    based on RFID scans. Players and furniture pieces are linked to their respective start locations.
    """
    players = []  # List to store player objects
    assigned_rfids = set() # To track processed rfids

    # Invert dictionaries for easier RFID lookup
    rfid_to_piece = {v: k for k, v in pieceRFID.items()}
    rfid_to_furniture = {v: k for k, v in furnitureRFID.items()}

    print("Waiting for players to press their 'end turn' buttons to assign panels...")

    # Map button presses to panel assignments
    panel_assignments = {
        "Button1": Panel1_pixels,
        "Button2": Panel2_pixels,
        "Button3": Panel3_pixels,
        "Button4": Panel4_pixels,
    }

    # Test code if we don't have buttons
    # Just pretend that we did get a button press
    button_pressed = "Button1"
    panel_pixels = panel_assignments[button_pressed]
    new_player = Player(position=0, pieceID="")
    new_player.panel = panel_pixels
    players.append(new_player)
    print(f"Player assigned to {button_pressed}.")
    
    # Wait for players to press their "end turn" buttons and assign panels
    #assigned_buttons = set()
    #while len(assigned_buttons) < len(panel_assignments):
    #    button_pressed = readButtons()  # Replace with your implementation of readButtons
    #    if button_pressed in panel_assignments and button_pressed not in assigned_buttons:
    #        print(f"{button_pressed} pressed! Assigning panel...")
    #        panel_pixels = panel_assignments[button_pressed]
    #        new_player = Player(position=0, cluesFound=[], pieceID="")
    #        new_player.panel = panel_pixels
    #        players.append(new_player)
    #        assigned_buttons.add(button_pressed)
    #        print(f"Player assigned to {button_pressed}.")
    #    elif button_pressed:
    #        print(f"{button_pressed} already assigned. Waiting for other players...")


    # Assign character pieces based on RFID scans
    print("Waiting for RFID scans to assign character pieces to players...")
    while len(players) < len(panel_assignments):  # Adjust loop to allow 2–4 players
        scanned_rfid = readRFID()  # Replace with actual RFID reading function
        if scanned_rfid and scanned_rfid not in assigned_rfids:
            if scanned_rfid in rfid_to_piece:
                piece_name = rfid_to_piece[scanned_rfid]
                player = Player(pieceID=piece_name, position=character_start_spaces[piece_name])
                player.panel = panel_assignments[f"Button{len(players) + 1}"]  # Assign next available panel
                light_up_position(player.position)  # Light up initial position
                players.append(player)
                assigned_rfids.add(scanned_rfid)
                print(f"Player piece {piece_name} assigned to start position {player.position}.")
            else:
                print("Invalid RFID scan. Please try again.")

    # Setup furniture on board
    print("Setting up furniture pieces on board...")
    for rfid, piece_name in rfid_to_furniture.items():
        if rfid not in assigned_rfids:
            if piece_name in furniture_start_spaces:
                position = furniture_start_spaces[piece_name]
                light_up_position(position)  # Light up furniture position
                assigned_rfids.add(rfid)
                print(f"Furniture piece {piece_name} placed at position {position}.")
            else:
                print(f"Error: Start position for {piece_name} not found.")
        else:
            print(f"Furniture piece {piece_name} already placed.")

    print("Game setup complete. Players are ready to start!")
    return players


# Begin main function

def main():
    # Startup process
    #StartupProcess()
    
    # Game setup
    #GameSetup()

    # Randomize pieces

    while True:
        # Test function
        testFunction()

    # Structure of the general gameplay
    # Start game loop

    # Get player turn
    # Wait for player to press spinner button
    #if(is_spinner_button_pressed()):
        # Get spinner value
        #spinValue = playSpinnerSpinAndStop()
            #If spinValue is "yellow"
                #Light up all yellow spaces
                #light_up_yellow_spaces()
                # Wait for RFID scan
                # Get RFID scan and output clue result
                # Update player's panel
                # If player presses accusation button, call accusation funciton
                # Else move onto next turn
            #If spinValue is "white"
                # Light up all white spaces
                #light_up_white_spaces()
                # Wait for RFID scan
                #readRFID()
                    # Give an error message if wrong type scanned (scanned yellow instead of white)
                #Update player's panel
                # If player presses accusation button, call accusation funciton
                # Else move onto next turn
            #If spinValue is a number
                # Get number from the spinner result
                # Call lightuppath function passing it the spinner value
                # If player lands on yellow
                    # Wait for RFID
                        # Make sure it's a yellow piece
                    # Update player's panel
                    # If player presses accusation button, call accusation funciton
                    # Else move onto next turn
                # If player lands on white
                    # Wait for RFID
                        # Make sure it's a white piece
                    # Update player's panel
                    # If player presses accusation button, call accusation funciton
                    # Else move onto next turn
                # Else, wait for accusation button or end turn button press
                # If accusation button pressed
                    # Call accusationSystem()
                    # If accusationSystem returns anything other than a 0, break out of the loop

main()