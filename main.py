from machine import Pin  # Import Pin class from machine module
import neopixel
from utime import sleep

# Board LED config
BoardLED_num_pixels = 42
BoardLED_pin = Pin(28, Pin.OUT)
Board_pixels = neopixel.NeoPixel(BoardLED_pin, BoardLED_num_pixels)

# Panel LED config
PanelLED_num_pixels = 26
PanelLED_pin = Pin(26, Pin.OUT)
Panel_pixels = neopixel.NeoPixel(PanelLED_pin, PanelLED_num_pixels)

# Spinner LED config
SpinnerLED_num_pixels = 6
SpinnerLED_pin = Pin(17, Pin.OUT)
Spinner_pixels = neopixel.NeoPixel(SpinnerLED_pin, SpinnerLED_num_pixels)

# Mux configuration

################################################################



def pathfinder(graph, start_node, roll_number):
    visited = set()  # To avoid revisiting nodes
    queue = [(start_node, 0)]  # Use a queue for BFS, storing (node, depth)
    
    reachable = []  # List to store reachable nodes
    
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
        Board_pixels[reachable_spaces[i]] = (1, 1, 1)
        Board_pixels.write()  # Update the NeoPixels
        
# Function to help everyone test out the program with hardware
def testFunction():
    # Print options for the user
    print("Clueless board options:")
    print("1: Test board LEDs")
    print("2: Test panel LEDs")
    print("3: Test pathfinder\n")
    
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
        Board_pixels.fill((0,0,0))
        Board_pixels.write()
        print("Test complete")
    else:
        print("Invalid choice. Please try again.")

# Define your graph
graph = {
    0: [10],
    1: [9],
    2: [3, 8],
    3: [2, 8],
    4: [7],
    5: [6],
    6: [5, 7],
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

# Begin main function

testFunction()