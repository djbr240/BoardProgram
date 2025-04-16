# Clue Jr Main Board Program
# Programmer: Daniel Breidenbach
# University of Kentucky College of Engineering
# Electrical and Computer Engineering Department
# Started: November 2024, Finalized: TBD

# This program is meant to be run on the Raspberry Pi Pico 2

from machine import I2C, ADC, Pin
import neopixel
import utime
from utime import sleep
from mfrc522 import MFRC522
from pcf7585 import *
import random
from Player import Player
# from Panel import Panel
from config import *
from _thread import start_new_thread

class Panel:
    def __init__(self, panelID):
        self.panelID = panelID

    def lightLED(self, clue, panelID):
        ledPos = cluePanelLED.get(clue)
        print(ledPos)

        if ledPos is None:
            print(f"Invalid clue: '{clue}' — not found in cluePanelLED")

        # Get potentiometer position from the mux
        for i, pin in enumerate(MUX_select_pins):
            pin.value((panelID >> i) & 1)  # Set the pin value based on the channel bits
        
        #Check the reading of the potentiometer from the mux
        # adc_value = ADC0_MUX.read_u16()  # Read ADC 
        # percentage = (adc_value / 65535) * 100 # convert to percent 
        # brightness = readPotentiometer(panelID)
        # color = (255, 255, 255)
        # apply_brightness = tuple(int(c * brightness) for c in (255,255,255))
        panel[panelID][ledPos] = (255,255,255)
        panel[panelID].write()

    def turn_off(self, panelID):
        panel[self.panelID].fill((0, 0, 0))
        panel[self.panelID].write()

    def test_panel(self):
        # Turn on all the LEDs on the panel for 2 seconds and then turn them off
        panel[self.panelID].fill((255, 255, 255))
        panel[self.panelID].write()
        sleep(2)
        panel[self.panelID].fill((0, 0, 0))
        panel[self.panelID].write()

    def _apply_brightness(self):
        """Reapply brightness scaling to all lit LEDs."""
        for i, base_color in enumerate(self.led_colors):
            self.strip[i] = self._scale_color(base_color)
        self.strip.write()

    # TODO: This hasn't been tested. Not sure if this would work.
    # This function will read the states of the first 6 pins from the fourth PCF board. Return the panel number corresponding to that panel.
def detectPanels():
    detectedPanels = []
    for pin in range(6):
        # Read the state of the current pin
        state = read_pcf()[pin + 58]
        # If the pin is high, it means a panel is present
        if state:
            detectedPanels.append(pin + 1)
            print(f"Panel {pin + 1} detected")
    return detectedPanels

pot_values = {}  # Global or shared dictionary to store readings

def pot_reader_loop():
    """Runs on Core 1: reads potentiometers & updates brightness for each panel."""
    while True:
        for panel in range(6):  # Assuming panels is a list of 6 Panel objects
            panel_num = panel.panel_num  # Each panel knows its MUX channel
            # Set MUX select lines
            for i, pin in enumerate(MUX_select_pins):
                pin.value((panel_num >> i) & 1)
            
            adc_value = ADC0_MUX.read_u16()
            brightness = int((adc_value / 65535) * 100)
            panel.set_brightness(brightness)

        sleep(0.1)  # Prevent hammering the MUX
    

# The following functions are LED animations

# Define LED colors for the sequence on the spinner
SPINNER_LED_COLORS = {
    0: (255, 255, 255),  # White
    1: (0, 0, 255),      # Blue
    2: (0, 0, 255),      # Blue
    3: (255, 255, 0),    # Yellow
    4: (0, 0, 255),      # Blue
    5: (0, 0, 255)       # Blue
}

def is_spinner_button_pressed():
    pin_state = read_pin(i2c_buses[2], 0x23, 8) # PCF board 4 pin 8
    # print(pin_state)
    if pin_state == 0:
        print("Pressed")
        return True

def set_turn_light(player_index):
    """
    Lights the turn indicator for the given player's panel.
    Only one turn light is active at a time (on PCF board 3, pins 10-15).
    """
    base_pin = 10  # PCF 3 pins 10–15 are used
    for i in range(6):
        pin_num = base_pin + i
        if i == player_index:
            write_pin(i2c_buses, 0x23, pin_num, 1)  # Turn ON
        else:
            write_pin(i2c_buses, 0x23, pin_num, 0)  # Turn OFF


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
            Spinner_pixels[j] = (0, 0, 0)

        # Light up the current spinner LED using the color from SPINNER_LED_COLORS
        Spinner_pixels[current_led] = SPINNER_LED_COLORS.get(current_led, (255, 0, 0))  # Default red
        Spinner_pixels.write()
        sleep(delay)

        # Move to the next spinner LED
        current_led = (current_led + 1) % total_spinner_leds

        # Gradually increase the delay
        delay += slowing_factor

    # Ensure the spinner stops at the random position
    while current_led != random_stop:
        # Turn off all spinner LEDs
        for j in range(total_spinner_leds):
            Spinner_pixels[j] = (0, 0, 0)

        # Light up the current spinner LED
        Spinner_pixels[current_led] = SPINNER_LED_COLORS.get(current_led, (255, 0, 0))  # Default red
        Spinner_pixels.write()
        sleep(delay)

        # Move to the next spinner LED
        current_led = (current_led + 1) % total_spinner_leds

    # Handle the final spinner stop actions
    for j in range(total_spinner_leds):
        Spinner_pixels[j] = (0, 0, 0)  # Turn off all LEDs

    # Determine behavior based on the stopping position
    final_led_index = random_stop
    if random_stop == 0:
        # Make LED white and return "white"
        Spinner_pixels[final_led_index] = SPINNER_LED_COLORS[random_stop]
        Spinner_pixels.write()
        return "white"
    elif random_stop == 1:
        # Make LED blue and blink 3 times, return 3
        for _ in range(3):
            Spinner_pixels[final_led_index] = SPINNER_LED_COLORS[random_stop]
            Spinner_pixels.write()
            sleep(0.3)
            Spinner_pixels[final_led_index] = (0, 0, 0)
            Spinner_pixels.write()
            sleep(0.3)
        return 3
    elif random_stop == 2 or 5:
        # Make LED blue and blink 4 times, return 4
        for _ in range(2):
            Spinner_pixels[final_led_index] = SPINNER_LED_COLORS[random_stop]
            Spinner_pixels.write()
            sleep(0.3)
            Spinner_pixels[final_led_index] = (0, 0, 0)
            Spinner_pixels.write()
            sleep(0.3)
        return 2
    elif random_stop == 3:
        # Make LED yellow and return "yellow"
        Spinner_pixels[final_led_index] = SPINNER_LED_COLORS[random_stop]
        Spinner_pixels.write()
        return "yellow"
    elif random_stop == 4:
        # Make LED blue and blink 3 times, return 3
        for _ in range(4):
            Spinner_pixels[final_led_index] = SPINNER_LED_COLORS[random_stop]
            Spinner_pixels.write()
            sleep(0.3)
            Spinner_pixels[final_led_index] = (0, 0, 0)
            Spinner_pixels.write()
            sleep(0.3)
        return 4

################################################################

def write_port(value):
    data = bytearray([value & 0xFF, (value >> 8) & 0xFF])
    i2c_buses.writeto(PCF8575_ADDRESSES, data)

# This function goes through every channel in the PCF Boards and checks all readings from the Magnet Switches
# It then returns a list of all the Magnet Switches that detected a magnetic presence
# This function will need to be called every time the position needs to be updated
        
def read_magnet_switches():
    # We have 42 magnet switches across 3 pcf boards
    # Board 1 is full, board 2 is full, board 3 contains 10 of the magnet switches
    # To properly read all the magnet switches, we need to filter out what's on board 3 pins 10-14 and the entire of board 4
    # This means that we use read_pcf() to read all pcf boards and remove the states from board 3 10-14 and board 4

    positions = []
    
    # Read all states from the 4 pcf boards
    positions = read_pcf()

    # After read_pcf() is called, the positions list will be populated with 64 values, we only want the first 42 states
    # So just return the first 42 states
    return positions[:41]

def read_pcf():
    # Initialize the PCF8575 boards
    #write_port(i2c_buses, PCF8575_ADDRESSES, 0x0000)
    sensorStates = []
    for i, (i2c, address) in enumerate(zip(i2c_buses, PCF8575_ADDRESSES)):
        port_value = read_port(i2c, address)
        # print(f"PCF8575 Board {i} (Address {address:#02x}) Raw Value: {bin(port_value)}")

        for pin in range(16):
            pin_state = read_pin(i2c, address, pin)
            sensorStates.append(pin_state)
            # print(f"Board {i} Pin {pin}: {'HIGH' if pin_state else 'LOW'}")
    return sensorStates
         
# Since for MUX3 channels 10-15, we are using those for Potentiometer and Button readings, we need a function to go through those MUX3 Channels
# We want to have Potentiometer and Buttons separated since they're doing significantly different functions
# This is a map of those assignments:
# MUX Channel 0 = Panel 1 Potentiometer
# MUX Channel 1 = Panel 2 Potentiometer
# MUX Channel 2 = Panel 3 Potentiometer
# MUX Channel 3 = Panel 4 Potentiometer
# MUX Channel 4 = Panel 5 Potentiometer
# MUX Channel 5 = Panel 6 Potentiometer

# def select_mux_channel(mux_pins, channel):
#     for i, pin in enumerate(mux_pins):
#         pin.value((channel >> i) & 1)  # Set the pin value based on the channel bits
        
def readPotentiometer(panel):
    # Get potentiometer position from the mux
    for i, pin in enumerate(MUX_select_pins):
        pin.value((panel >> i) & 1)  # Set the pin value based on the channel bits
    
    adc_value = ADC0_MUX.read_u16()  # Read ADC 
    percentage = (adc_value / 65535) * 100 # convert to percent 
    return int(percentage)  # Return the Potentiometer value in percentage

# Reads PCF Pins 10-15 to see if a button is pressed. Return the button number pressed
def readButtons():
    # The buttons are going to be connected to the last 6 pins on the pcf board, so we use read_pcf to get all the states
    # We then remove everything else

    values = []

    values = read_pcf()  # Read GPIO state from PCF8575
    #print(values)
    # Remove the non-button states
    values = values[58:64]
    #print(values)

    # Check specific pins (P10-P14) for button presses
    button1_pressed = values[0]
    button2_pressed = values[1]
    button3_pressed = values[2]
    button4_pressed = values[3]
    button5_pressed = values[4]
    button6_pressed = values[5]
    
    buttonPressed = 0
    if button1_pressed: buttonPressed = 1
    if button2_pressed: buttonPressed = 2
    if button3_pressed: buttonPressed = 3
    if button4_pressed: buttonPressed = 4
    if button5_pressed: buttonPressed = 5
    if button6_pressed: buttonPressed = 6
    
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

def identify_rfid(card):
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
        Board_pixels[reachable_spaces[i]] = (255, 255, 255)
    Board_pixels.write()  # Update the NeoPixels

# When this function is called, light up all the Yellow spaces.
# Loop through the yellow_space list and light up that LED
def light_up_yellow_spaces():
    for space in yellow_space:
        Board_pixels[space] = (255, 255, 0)
    Board_pixels.write()

# Same as light_up_yellow_spaces() but with the white spaces
def light_up_white_spaces():
    for space in white_space:
        Board_pixels[space] = (255, 255, 255)
    Board_pixels.write()
    
# For the setup process, this function lights up one of the LED positions
def light_up_position(position):
    if 0 <= position < len(Board_pixels):
        # Turn off all LEDs first
        for i in range(len(Board_pixels)):
            Board_pixels[i] = (0, 0, 0)  # RGB values for "off"

        # Light up the specified position
        Board_pixels[position] = (255, 255, 255)  # RGB values for "white" or a bright color
        Board_pixels.write()  # Function to send data to the LED strip
        print(f"Position {position} lit up.")
    else:
        print(f"Error: Position {position} is out of range.")

# Get the LED position of the clue and light up that LED on the panel
# def light_up_panel_led(clue, panelID):
#     ledPos = cluePanelLED.get(clue, None)
#     print(ledPos)
#     if ledPos is not None:
#         brightness = readPotentiometer(panelID)
#         color = LED_COLORS("White")
#         apply_brightness = tuple(int(c * brightness) for c in color)
#         panel[panelID][ledPos] = apply_brightness
#         panel[panelID].write()

# def turn_off_panel_led(panelID):
#     panel[panelID] = (0, 0, 0)
#     panel[panelID].write()

def getPiecePosition(piece):
    if piece in character_start_spaces:
        return character_start_spaces[piece]
    if piece in furniture_spaces:
        return furniture_spaces
        

def accusationSystem(furniture_assignment, character_assignment):
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
        


def testFunction():
    # Print options for the user
    print("Clueless board options:")
    print("1: Test board LEDs")
    print("2: Test panel LEDs")
    print("3: Test pathfinder")
    print("4: RFID options")
    print("5: Magnet Switch test")
    print("6: Test spinner")
    print("7: Button test")
    
    # Get user input
    user_input = input("Enter your choice: ")
    
    # Make a switch case for each option
    if user_input == "1":
        print("Testing board LEDs (5 seconds)...")
        # Light up all board LEDs (dim white)
        Board_pixels.fill((25, 25, 25))
        Board_pixels.write()
        sleep(5)
        Board_pixels.fill((0, 0, 0))
        Board_pixels.write()
        print("Test complete")
        
    elif user_input == "2":
        user_input = input("Enter what part of the panels you want to test: \n1. Flash all leds on \n2. Light up clue")

        if user_input == "1":
            print("Testing panel LEDs...")
            # Use the test function in the panel class to test the panels. Loop through all 6 panels
            for i in range(6): # assume 6 panels
                panel_instance = Panel(i)
            for panelID in panel.keys():
                panel_instance.test_panel()
            print("Test complete")

        if user_input == "2":
            print("Which method? \n1. Text input\n2. RFID")
            if user_input == "1":
                user_input = input("Input which clue: ")
                if user_input == "help":
                        print(f"Here's all the options in the dictionary:\n{cluePanelLED.values()}\n")
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
        Board_pixels.fill((0,0,0))
        Board_pixels.write()
        print("Test complete")
        
    #Test RFID Functionality    
    elif user_input == "4":

        print("RFID Reading...")
        
        #if user_input == "1":
        while True:
            card = readRFID()

            
            # Fetch the corresponding piece and furniture from the dictionary
            item_name = identify_rfid(card)
            print(item_name)

            if item_name:
                print(f"Identified {item_name}!")
                # Light up panel LED with that clue (we'll just do all the panels I guess..)
                for i in range(1, 6):
                    panel_instance = Panel(i)
                    panel_instance.lightLED(item_name, i)
                    print(f"LED on panel {i} lit")
                    # sleep(1)
                    # panel_instance.turn_off(i)
                    # print(f"LED on panel {i} unlit")
                    

            # This is for the testing tags and cards. 
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
            print("Testing Magnet Switches...")
            # Read Magnet Switches and get detected positions
            detected_raw = read_magnet_switches()
            print("Detected positions:", detected_raw)
            # sleep(1)
            detected_positions = [i for i, val in enumerate(detected_raw) if val == 1]
            print(detected_positions)

            # Test LEDs based on detected positions
            for i in range(len(detected_positions)):
                if i not in detected_positions:
                    Board_pixels[i] = (0, 255, 0)  # Green for detected positions
                    Board_pixels.write()
                else:
                    Board_pixels[i] = (0, 0, 0)  # Off if not detected
                    Board_pixels.write()
            sleep(0.1)

    elif user_input == "6":
        print("Waiting for button press to spin...")
        while True:
            btnInput = is_spinner_button_pressed()
            # print(is_spinner_button_pressed())
            if is_spinner_button_pressed():
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

# When the device is turned on, test all of the LEDs on the board
def StartupProcess():
    # In sequence, from the first LED on the board, to the last LED on the board, then the final 6 LEDs in the spinner.
    # To do this, in a loop going through all Board_pixels, turn on each Board_pixels individually, then turn that pixel off.
    for i in range(len(Board_pixels)):
        Board_pixels[i] = (255, 255, 255)
        Board_pixels.write()
        sleep(.1)
        Board_pixels[i] = (0, 0, 0)
        Board_pixels.write()
        
    # This comment is a placeholder for other LED tests... TODO

def shuffle(list):
    for i in range(len(list) - 1, 0, -1):
        j = random.randint(0, i)
        list[i], list[j] = list[j], list[i]


def randomizeClues():
    # Step 1: Shuffle toy clues and assign to characters
    shuffle(toy_clues)
    character_pairs = list(zip(character_clues, toy_clues))  # [(character, toy)]
    print(character_pairs)

    # Step 2: Shuffle time clues and assign to furniture (must match in count!)
    shuffle(time_clues)
    furniture_pairs = list(zip(furniture_clues, time_clues[:len(furniture_clues)]))  # [(furniture, time)]
    print(furniture_pairs)

    return character_pairs, furniture_pairs

# Setup process
def GameSetup():
    """
    Sets up the game by assigning players to their panels and initializing their positions 
    based on RFID scans. Players and furniture pieces are linked to their respective start locations.
    """

    print("Starting game setup...")

    # Store the required pieces and furniture
    required_characters = set(pieceRFID.values())
    required_furniture = set(furnitureRFID.values())

    placed_characters = set()
    placed_furniture = set()

    # Invert the RFID mappings to look up piece/furniture by scanned RFID
    rfid_to_character = {v: k for k, v in pieceRFID.items()}
    rfid_to_furniture = {v: k for k, v in furnitureRFID.items()}

    # Loop until all required pieces and furniture are placed
    while placed_characters != required_characters or placed_furniture != required_furniture:
        print("Scan a piece...")
        
        # Use the custom readRFID function to read the RFID tag
        rfid = readRFID()
        print(f"Scanned RFID: {rfid}")

        if rfid in rfid_to_character:
            name = rfid_to_character[rfid]
            position = character_start_spaces[name]
            print(f"{name} character detected. Should be at space {position}")
            Board_pixels[position] = LED_COLORS["White"]
            Board_pixels.write()

            # position = read_pcf()
            print(position)
            if not read_magnet_switches() == position:
                placed_characters.add(rfid)
                print(f"{name} correctly placed.")
            else:
                print(f"{name} not yet placed correctly.")

        elif rfid in rfid_to_furniture:
            name = rfid_to_furniture[rfid]
            position = furniture_spaces[name]
            print(f"{name} furniture detected. Should be at space {position}")
            Board_pixels[position] = LED_COLORS["White"]
            Board_pixels.write()

            if not read_magnet_switches() == position:
                placed_furniture.add(rfid)
                print(f"{name} correctly placed.")
            else:
                print(f"{name} not yet placed correctly.")

        else:
            print("Unknown piece scanned.")

        utime.sleep(0.2)

    print("All pieces placed correctly!")

    # Detect plugged-in panels using Panel.detectPanels
    detected_panels = detectPanels()

    players = []
    for idx, panel_id in enumerate(detected_panels):
        player = Player(playerNum=len(players) + 1, panel=Panel(panel_id))
        players.append(player)
        print(f"Player {player.playerNum} assigned to Panel {panel_id}")

    print("Game setup complete. Players ready!")
    return players


# Begin main function

def main():
    while True:
    #Test function
    #     # print(is_spinner_button_pressed())
        testFunction()
    #     character_assignments, furniture_assignments = randomizeClues()
    #     print(character_assignments)
    #     print(furniture_assignments)
    #     sleep(10)
        
    ##############################################################
    
    # Always loop checking the pot reading
    # start_new_thread(pot_reader_loop, ())

    
    
    # Main gameplay loop (needs testing)
    print("Initializing game hardware...")

    # 2. Initialize NeoPixel LED board to all off.
    # Board_pixels.fill((0, 0, 0))
    # Board_pixels.write()

    StartupProcess()

    # 3. Call GameSetup to:
    #    - Wait for all character and furniture pieces to be placed correctly
    #    - Automatically detect which panels are plugged in
    #    - Create Player instances and assign them panels
    players = GameSetup()

    # Randomize clues
    character_assignments, furniture_assignments = randomizeClues()

    # Board_pixels.fill() = (0, 0, 0)
    # Board_pixels.write()

    StartupProcess()


    # 4. Setup is complete, print a summary
    print(f"{len(players)} player(s) have joined the game.")
    for player in players:
        print(player)

    # 5. Structure of the general gameplay
    print("Starting game loop...")
    while True:
        # Start game loop

        # Get player turn
        for player in players:
            print(f"Player {player.playerNum}'s turn")
            
            # Wait for player to press spinner button
            while not is_spinner_button_pressed():
                utime.sleep(0.1)  # Wait for button press

            # If the spinner button is pressed, get the spinner value
            spinValue = playSpinnerSpinAndStop()
            print(f"Spin Value: {spinValue}")

            # If spinValue is "yellow"
            if spinValue == "yellow":
                # Light up all yellow spaces
                light_up_yellow_spaces()
                # Wait for RFID scan
                rfid = readRFID()
                print(f"RFID Scan Result: {rfid}")

                # Get clue based on RFID scan
                clue = identify_rfid(rfid)
                player.add_clue(clue)
                player.update_panel()

                # If player presses accusation button, call accusation function
                if readRFID:
                    accusationResult = accusationSystem(readRFID())
                    if accusationResult != 0:
                        print("Game Over! Player made a correct accusation.")
                        break  # Exit game loop if accusation is made
                else:
                    # Move onto next turn
                    continue

            # If spinValue is "white"
            elif spinValue == "white":
                # Light up all white spaces
                light_up_white_spaces()
                # Wait for RFID scan
                rfid = readRFID()
                print(f"RFID Scan Result: {rfid}")

                # Validate the RFID scan, make sure it's a white piece
                if rfid not in pieceRFID.values():
                    print("Error: Incorrect piece scanned (should be white).")
                    continue

                # Update player's panel
                clue = identify_rfid(rfid)
                player.add_clue(clue)
                player.update_panel()

                # If player presses accusation button, call accusation function
                if readRFID():
                    accusationResult = accusationSystem()
                    if accusationResult != 0:
                        print("Game Over! Player made an accusation.")
                        break  # Exit game loop if accusation is made
                else:
                    # Move onto next turn
                    continue

            # If spinValue is a number (i.e., a number between 1 and 6)
            elif isinstance(spinValue, int):
                # Get number from the spinner result
                print(f"Moving {spinValue} spaces.")
                # Call lightuppath function passing it the spinner value
                light_up_path(spinValue)

                # Check where player lands after moving
                if player.position in yellow_space:
                    # Wait for RFID scan
                    rfid = readRFID()
                    print(f"RFID Scan Result: {rfid}")

                    # Make sure it's a yellow piece
                    if rfid not in furnitureRFID.values():
                        print("Error: Incorrect piece scanned (should be yellow).")
                        for i in range(3):
                            light_up_yellow_spaces()
                            Board_pixels = (0, 0, 0)
                        continue

                    # Update player's panel
                    clue = identify_rfid(rfid)
                    player.add_clue(clue)
                    player.update_panel()

                    # If player presses scans a piece, call accusation function
                    if readRFID():
                        accusationResult = accusationSystem()
                        if accusationResult != 0:
                            print("Game Over! Player made an accusation.")
                            break  # Exit game loop if accusation is made
                    else:
                        # Move onto next turn
                        continue

                elif player.position in white_space:
                    # Wait for RFID scan
                    rfid = readRFID()
                    print(f"RFID Scan Result: {rfid}")

                    # Make sure it's a white piece
                    if rfid not in pieceRFID:
                        print("Error: Incorrect piece scanned (should be white).")
                        continue

                    # Update player's panel
                    clue = identify_rfid(rfid)
                    player.add_clue(clue)
                    player.update_panel()

                    # If player presses accusation button, call accusation function
                    if readRFID():
                        accusationResult = accusationSystem()
                        if accusationResult != 0:
                            print("Game Over! Player made an accusation.")
                            break  # Exit game loop if accusation is made
                    else:
                        # Move onto next turn
                        continue

                else:
                    # If player lands on a non-yellow/non-white space, wait for accusation button or end turn button press
                    if readRFID():
                        accusationResult = accusationSystem(furniture_assignments, character_assignments)
                        if accusationResult != 0:
                            print("Game Over! Player made an accusation.")
                            break  # Exit game loop if accusation is made
                    else:
                        # End player's turn and proceed
                        print("End of turn.")
                        continue
    
    ##############################################################

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