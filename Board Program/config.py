from machine import I2C, ADC, Pin
import neopixel
from mfrc522 import MFRC522

################################################################
#   Configuration

# This is the only place where Pins, number of LEDs, threshold values, etc are defined.

# Board LED config
Board_Spinner_LED_num_pixels = 25 # 42 Board LEDs and 6 Spinner LEDs = 48
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
PanelLED5_num_pixels = 26
PanelLED5_pin = Pin(17, Pin.OUT)
Panel5_pixels = neopixel.NeoPixel(PanelLED5_pin, PanelLED5_num_pixels)

# We currently don't have a solution for having a 6th panel (out of pins)
PanelLED6_num_pixels = 26
PanelLED6_pin = Pin(16, Pin.OUT)
Panel6_pixels = neopixel.NeoPixel(PanelLED6_pin, PanelLED6_num_pixels)

# Initialize I2C buses for four PCF8575 boards
i2c_buses = [
    I2C(0, scl=Pin(5), sda=Pin(4), freq=400000),  # I2C0 on pin 4 and 5
    I2C(0, scl=Pin(5), sda=Pin(4), freq=400000),  
    I2C(1, scl=Pin(7), sda=Pin(6), freq=400000),  # I2C on GP8 and GP7
    I2C(1, scl=Pin(7), sda=Pin(6), freq=400000) 
]

# PCF8575 I2C addresses
PCF8575_ADDRESSES = [0x20, 0x21, 0x22, 0x23]

#TODO: Change pin numbers here when it's figured out where everything else is connecting to
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
RFIDreader = MFRC522(spi_id=0,sck=2,miso=0,mosi=3,cs=1,rst=16)

################################################################
# Piece identification, graph, and LED locations on the board and panels

#TODO: Update graph to new config
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

#TODO: Change these based on new config (white and yellow spaces and character start spaces and furniture start spaces)
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
