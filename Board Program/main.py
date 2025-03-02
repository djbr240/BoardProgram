# Clue Jr Main Board Program
# Programmer: Daniel Breidenbach
# University of Kentucky College of Engineering
# Electrical and Computer Engineering Department
# Started: November 2024, Finalized: TBD

# This program is meant to be run on the Raspberry Pi Pico 2

from machine import I2C, ADC, Pin
import neopixel
from utime import sleep
import utime
from mfrc522 import MFRC522
import random
from Player import Player
from config import *


# This is the Player class, where all of the information for each player is created

    
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
    for bus_index, i2c in enumerate(i2c_buses):
        value = read_pcf8575(i2c)  # Read GPIO state
        for pin in range(16):  # Check each pin (0 to 15)
            if not (value & (1 << pin)):  # Active-low button press (0 means pressed)
                print(f"Button on PCF8575 {bus_index}, Pin P{pin} is pressed")

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

# This function goes through every channel in the PCF Boards and checks all readings from the Magnet Switches
# It then returns a list of all the Magnet Switches that detected a magnetic presence
# This function will need to be called every time the position needs to be updated

# Read the outputs of the PCF8575 board
def read_pcf8575(i2c):
    data = i2c.readfrom(PCF8575_ADDRESS, 2)  # Read 2 bytes
    return (data[1] << 8) | data[0]  # Combine into a 16-bit value
        
def read_magnet_switches():
    """
    Reads all 42 Magnet Switches (across 3 PCF boards)
    and returns a list of sensor indices where a magnetic presence is detected.
    """
    
    sensor_states = []
    
    for bus_index, i2c in enumerate(i2c_buses):
        value = read_pcf8575(i2c)  # Read GPIO state
        for pin in range(16):  # Check each pin (0 to 15)
            sensor_id = bus_index * 16 + pin  # Calculate sensor index (0 to 47)
            if sensor_id < 42:  # Only check the first 42 sensors
                state = not (value & (1 << pin))  # Active-low: 0 when magnetic field detected
                sensor_states.append(state)
                if state:
                    print(f"Sensor {sensor_id} is triggered")

    return sensor_states


# This function takes the previous reading from read_hall_sensors(), calls read_hall_sensors() again and compares them to find the difference from the last reading

    
         
# Since for MUX3 channels 10-15, we are using those for Potentiometer and Button readings, we need a function to go through those MUX3 Channels
# We want to have Potentiometer and Buttons separated since they're doing significantly different functions
# This is a map of those assignments:
# MUX Channel 0 = Panel 1 Potentiometer
# MUX Channel 1 = Panel 2 Potentiometer
# MUX Channel 2 = Panel 3 Potentiometer
# MUX Channel 3 = Panel 4 Potentiometer
# MUX Channel 4 = Panel 5 Potentiometer
# MUX Channel 5 = Panel 6 Potentiometer
# MUX Channel 6 =
# MUX Channel 7 =
# MUX Channel 8 =
# MUX Channel 9 =
# MUX Channel 10 =
# MUX Channel 11 =
# MUX Channel 12 =
# MUX Channel 13 =
# MUX Channel 14 =
# MUX Channel 15 =
def select_mux_channel(mux_pins, channel):
    for i, pin in enumerate(mux_pins):
        pin.value((channel >> i) & 1)  # Set the pin value based on the channel bits
        
def readPotentiometer():
    # Read MUX3 Channel 15
    select_mux_channel(MUX_select_pins, 10)
    adc_value = ADC0_MUX.read_u16()  # Read ADC value
    return adc_value  # Return the Potentiometer value

# Reads MUX3 Channels 10-15 to see if a button is pressed. Return the button number pressed
def readButtons():
    value = read_pcf8575()  # Read GPIO state from PCF8575

    # Check specific pins (P10-P14) for button presses
    button1_pressed = not (value & (1 << 10))  # P10
    button2_pressed = not (value & (1 << 11))  # P11
    button3_pressed = not (value & (1 << 12))  # P12
    button4_pressed = not (value & (1 << 13))  # P13
    button5_pressed = not (value & (1 << 14))  # P14
    
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
            sleep(5)
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
            detected_positions = read_magnet_switches()
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