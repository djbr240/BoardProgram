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

# Spinner LED config (This is part of board leds)
#SpinnerLED_num_pixels = 6
#SpinnerLED_pin = Pin(17, Pin.OUT)
#Spinner_pixels = neopixel.NeoPixel(SpinnerLED_pin, SpinnerLED_num_pixels)


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
# The following functions are LED animations

# Define LED colors for the sequence
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

# This is the Player class, where all of the information for each player is created
class Player:
    def __init__(self, pieceID, position=0, panel=None):
        """
        Initialize a player.
        :param sensor_reader: A function reference for reading hall sensors.
        """
        self.position = None  # Tracks the player's current position on the board
        self.clues_found = []  # List of clues collected by the player
        self.piece = None  # The piece that the player is using
        self.panel = None  # The LED panel assigned to the player
        self.panel_leds_lit = []  # List of LEDs lit on the panel

        
    def assign_panel(self, panel):
        """Assign a panel to the player."""
        self.panel = panel
        
    def set_piece(self, piece):
        """Set the player's piece after the first move."""
        if self.piece is None:  # Piece can only be set once
            self.piece = piece
            
    def collect_clue(self, clue):
        """Add a clue to the player's collection."""
        self.clues_found.append(clue)

    def add_clue(self, clue):
        """Add a clue (integer) to the player's list of cluesFound and update the panel."""
        self.cluesFound.append(clue)
        self.update_panel()

    def move(self, new_position):
        """Update the player's position."""
        self.position = new_position
        
    def update_position(self, new_position=None):
        """
        Move the player to a new position and read hall sensors if applicable.
        :param new_position: The new position to move to, optional if using sensor_reader.
        """
        if new_position is not None:
            self.position = new_position
        elif self.sensor_reader:
            self.position = self.sensor_reader()
        else:
            print("Error: No new position provided and no sensor_reader set.")
            
    def get_position(self):
        """Get the player's current position."""
        return self.position


    def update_panel(self, led_index):
        """Add an LED to the player's panel and update the panel."""
        if led_index not in self.leds_lit:
            self.panel_leds_lit.append(led_index)
            if self.panel:
                self.panel.set_led(led_index, "red")
            else:
                print("No panel assigned to this player.")
    
    def display_panel_status(self):
        """Display the status of the player's panel."""
        print(f"Player's panel LEDs: {self.leds_lit}")

    def __str__(self):
        return f"Player {self.pieceID} is at position {self.position} with clues {self.cluesFound}"
    
    # End player class
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
# MUX3 Channel 11 = Button2
# MUX3 Channel 12 = Button3
# MUX3 Channel 13 = Button4
# MUX3 Channel 14 = Button5
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
    
    select_mux_channel(MUX3_select_pins, 15)
    button5_pressed = bool(ADC2_MUX3.read_u16() < button_threshold)
    
    buttonPressed = 0
    if button1_pressed: buttonPressed = 1
    if button2_pressed: buttonPressed = 2
    if button3_pressed: buttonPressed = 3
    if button4_pressed: buttonPressed = 4
    if button5_pressed: buttonPressed = 5
    
    
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
        print("Testing panel LEDs...")
        # Light up all panel LEDs
        
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
                
            if card == 17611714:
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
            
    else:
        print("Invalid choice. Please try again.")

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
start_spaces = {
    "Blue": 30,
    "Purple": 5,
    "Red": 1,
    "Yellow": 12,
    "Pink" : 40,
    "Green" : 41
}

# Dictionary for the character pieces and the RFID links
# All zeros as a placeholder for now
pieceRFID = {
    "Blue": 0,
    "Purple": 0,
    "Red": 0,
    "Yellow": 0,
    "Pink": 0,
    "Green": 0,
}

# The LED position for the clue panels
cluePanelLED = {
    #characters
    "Blue": 0,
    "Purple": 0,
    "Red": 0,
    "Yellow": 0,
    "Pink": 0,
    "Green": 0,
    
    #toys
    "trex": 0,
    "racecar": 0,
    "teddybear": 0,
    "mr_potatohead": 0,
    "xylophone": 0,
    "ball": 0,
    
    #locations
    "pooltable": 0,
    "desk": 0,
    "chair": 0,
    "piano": 0,
    "plant": 0,
    "diningtable": 0,
    
    #time
    "11": 0,
    "12": 0,
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0
}

########################################################################

# Setup process

def GameSetup():
    
    # Create Player class for each player that joins the game
    Players = []  # To store players
    max_players = 4  # Set maximum number of players

    # A player joins the game by pressing the button for their panel. The button value is the player's panel
    while len(Players) < max_players or is_spinner_button_pressed == True:
        button_value = readButtons()  # Read button input
        print(button_value)
        if button_value > 0:
            if all(player.pieceID != f"Panel{button_value}" for player in Players):
                new_player = Player(f"Panel{button_value}")
                print(new_player)
                Players.append(new_player)
                print(Players)
                print(Player.panel)
                print(f"Player {button_value} joined the game!")
            else:
                print(f"Panel {button_value} is already taken.")
                break

        

# Begin main function

def main():
    # Startup process
    StartupProcess()
    
    # Game setup
    GameSetup()

    # Randomize pieces

    #while True:
    #    # Test function
    #    testFunction()

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