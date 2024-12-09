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

PanelLED5_num_pixels = 26
PanelLED5_pin = Pin(17, Pin.OUT)
Panel5_pixels = neopixel.NeoPixel(PanelLED5_pin, PanelLED5_num_pixels)

# We currently don't have a solution for having a 6th panel (out of pins)
#PanelLED6_num_pixels = 26
#PanelLED6_pin = Pin(26, Pin.OUT)
#Panel6_pixels = neopixel.NeoPixel(PanelLED6_pin, PanelLED6_num_pixels)

# Spinner LED config
SpinnerLED_num_pixels = 6
SpinnerLED_pin = Pin(17, Pin.OUT)
Spinner_pixels = neopixel.NeoPixel(SpinnerLED_pin, SpinnerLED_num_pixels)


# Mux configuration

hall_sensor_threshold = 500

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

# This is the Player class, where all of the information for each player is created
class Player:
    def __init__(self, pieceID, position=0):
        self.pieceID = pieceID        # A string to represent the piece ID
        self.position = position      # An integer representing the player's position
        self.cluesFound = []          # A list to store clues that the player has found

    def add_clue(self, clue):
        """Add a clue (integer) to the player's list of cluesFound."""
        self.cluesFound.append(clue)

    def move(self, new_position):
        """Update the player's position."""
        self.position = new_position

    def __str__(self):
        return f"Player {self.pieceID} is at position {self.position} with clues {self.cluesFound}"

# Example usage:
#player1 = Player("A1")
#player1.add_clue(5)
#player1.move(10)
#print(player1)


# This function goes through every channel in the MUXs and checks all readings from the Hall Sensors
# It then returns a list of all the Hall Sensors that detected a magnetic presence
# This function will need to be called every time the position needs to be updated
def read_hall_sensors():
    """
    Reads all 42 Hall sensors (across 3 MUXs), checks if their ADC value is below the threshold, 
    and returns a list of sensor indices where a magnetic presence is detected.
    """
    
    detected_positions = []  # List to store detected positions
    
    # Function to select a channel on a MUX
    def select_mux_channel(mux_pins, channel):
        for i, pin in enumerate(mux_pins):
            pin.value((channel >> i) & 1)  # Set the pin value based on the channel bits

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
# We want to have Potentiometer and Buttons separated since they're doing significantly different functions, so we will have a function for checking the Potentiometer channel (10) and the remaining for checking the buttons
def check_pot_reading():
    # Read the Potentiometer value
    pot_reading = MUX3_select_pins[10].value
    
    # Convert the Potentiometer value to a position between 0 and 63
    position = pot_reading * (63 / 1024)
    
    # Display the Potentiometer value
    print("Potentiometer value:", pot_reading)
    print("Converted position:", position)

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
        Board_Spinner_pixels[reachable_spaces[i]] = (1, 1, 1)
    Board_Spinner_pixels.write()  # Update the NeoPixels
        
# Function to help everyone test out the program with hardware
def testFunction():
    # Print options for the user
    print("Clueless board options:")
    print("1: Test board LEDs")
    print("2: Test panel LEDs")
    print("3: Test pathfinder")
    print("4: RFID options\n")
    
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
        sleep(5)
        Board_Spinner_pixels.fill((0,0,0))
        Board_Spinner_pixels.write()
        print("Test complete")
        
    #Test RFID Functionality    
    elif user_input == "4":
        #print("Enter the option for RFID:")
        #print("1: Read RFID")
        #print("2: Write RFID (Currently not working)\n")
        #user_input = input()

        print("RFID Reading...")
        
        #if user_input == "1":
        while True:
            while True:
                # Read RFID and print to console
                RFIDreader.init()
                (stat, tag_type) = RFIDreader.request(RFIDreader.REQIDL)
                if stat == RFIDreader.OK:
                    (stat, uid) = RFIDreader.SelectTagSN()
                    if stat == RFIDreader.OK:
                        card = int.from_bytes(bytes(uid),"little",False)
                        print("CARD ID: "+str(card))
                        break
                
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
            
        #elif user_input == "2":

    elif user_input == "5":
        while True:
            for sensor_id in range(10):  # Loop through all 42 sensors
                mux_index = sensor_id // 16  # Determine which MUX (0, 1, or 2)
                channel = sensor_id % 16     # Determine the channel within the MUX

                select_mux_channel(mux_index, channel)  # Select the MUX and channel
                raw_value = adc.read_u16()  # Read ADC value
                #voltage = (raw_value / 65535) * V_REF  # Convert raw value to voltage
                
                # Turn on LED if voltage is 0, otherwise turn it off
                if voltage == 0:
                    np[sensor_id] = (255, 0, 0)  # Turn LED red for voltage 0
                else:
                    np[sensor_id] = (0, 0, 0)  # Turn off the corresponding LED
                
                print(f"Sensor {sensor_id}: Voltage = {voltage:.2f} V")
            
            np.write()  # Update NeoPixel LEDs
            sleep(0.1)  # Short delay for stable readings
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

########################################################################

# Begin main function

# Example usage:
#player1 = Player("A1")
#player1.add_clue(5)
#player1.move(10)
#print(player1)

testFunction()