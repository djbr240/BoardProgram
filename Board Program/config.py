from machine import I2C, ADC, Pin
import neopixel
from mfrc522 import MFRC522

################################################################
#   Configuration

# Brightness stuff
PANEL1_BRIGHTNESS = 100

LED_COLORS = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "White": (255, 255, 255)
}

# This is the only place where Pins, number of LEDs, threshold values, etc are defined.

# Board LED config
Board_LED_num_pixels = 42 # 42 Board LEDs
Board_LED_pin = Pin(22, Pin.OUT)
Board_pixels = neopixel.NeoPixel(Board_LED_pin, Board_LED_num_pixels)

# Spinner LED config
Spinner_LED_num_pixels = 6
Spinner_LED_pin = Pin(26, Pin.OUT)
Spinner_pixels = neopixel.NeoPixel(Spinner_LED_pin, Spinner_LED_num_pixels)

# Panel LED config (there's 6 panels)
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

PanelLED6_num_pixels = 26
PanelLED6_pin = Pin(16, Pin.OUT)
Panel6_pixels = neopixel.NeoPixel(PanelLED6_pin, PanelLED6_num_pixels)

# This is a list of for the panels so we can index them
panel = {
    1: Panel1_pixels,
    2: Panel2_pixels,
    3: Panel3_pixels,
    4: Panel4_pixels,
    5: Panel5_pixels,
    6: Panel6_pixels
}

# Initialize I2C buses for four PCF8575 boards
# All PCF boards are connected to a hub, so they all use the same pins and port
i2c_buses = [
    I2C(0, scl=Pin(9), sda=Pin(8), freq=400000), 
    I2C(0, scl=Pin(9), sda=Pin(8), freq=400000), 
    I2C(0, scl=Pin(9), sda=Pin(8), freq=400000), 
    # I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)  
]

# PCF8575 I2C addresses - Note: This is configured using the solder pads on the back of the board (0x20 has none, 0x21 has the +1 pad soldered, and so on)
PCF8575_ADDRESSES = [0x20, 0x21, 0x22, 0x23]

# This is for reading the Potentiometers on the panels
# Initialize ADC for MUX SIG output
ADC0_MUX = ADC(Pin(28))  # ADC pin connected to the MUX SIG output

# GPIO pins for MUX select lines
MUX_select_pins = [
    Pin(10, Pin.OUT),  # S0
    Pin(11, Pin.OUT),  # S1
    Pin(12, Pin.OUT),  # S2
    Pin(13, Pin.OUT),  # S3
]

# RFID configuration
RFIDreader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=5,rst=1)

################################################################
# Piece identification, graph, and LED locations on the board and panels

# Graph represented as an adjacency list
# Left side is the source, in [] is the source's neighbors
graph = {
    0: [9],
    1: [2, 8],
    2: [1, 8, 14],
    3: [7],
    4: [6],
    5: [15],
    6: [15],
    7: [3, 19],
    8: [1, 2, 13],
    9: [12, 13],
    10: [12],
    11: [12],
    12: [9, 10, 13, 22],
    13: [8, 9, 12, 14, 20],
    14: [2, 13, 19],
    15: [5, 6, 18, 19],
    16: [5, 6, 16, 19],
    17: [17, 18],
    18: [15, 16, 17, 28],
    19: [7, 14, 15, 28],
    20: [13, 26],
    21: [12, 22, 23, 25],
    22: [12, 21, 23],
    23: [21, 22, 25],
    24: [25],
    25: [21, 23, 26],
    26: [20, 25, 27, 36],
    27: [26, 28, 34, 35],
    28: [18, 19, 27, 29, 33],
    29: [28],
    30: [29],
    31: [41],
    32: [33, 41],
    33: [28, 32, 34],
    34: [27, 33, 35, 39],
    35: [27, 34, 39],
    36: [26, 38],
    37: [38],
    38: [36, 37],
    39: [34, 35],
    40: [33],
    41: [31, 32]
}

# Yellow spaces positions
yellow_space = [1, 5, 10, 23, 39, 31]

# White spaces positions
white_space = [3, 17, 37]

# Start spaces
# A dictionary where the character and the position is linked together
character_start_spaces = {
    "Blue": 0,
    "Purple": 4,
    "Red": 30,
    "Yellow": 40,
    "Pink" : 24,
    "Green" : 11
}

# Furniture spaces
furniture_spaces = {
    "pooltable": 1,
    "desk": 5,
    "chair": 31,
    "piano": 23,
    "plant": 10,
    "diningtable": 39
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
