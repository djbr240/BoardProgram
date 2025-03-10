from machine import Pin, I2C
import time

# Define the I2C buses (as per your configuration)
i2c_buses = [
    I2C(0, scl=Pin(5), sda=Pin(4), freq=400000),  # I2C on GP0 and GP1
    I2C(1, scl=Pin(7), sda=Pin(6), freq=400000),  # I2C on GP2 and GP3
    #I2C(0, scl=Pin(9), sda=Pin(8), freq=400000),  # I2C on GP4 and GP5
    #I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)  # I2C on GP6 and GP7
]

# Define the I2C addresses for the PCF8575 boards (can be adjusted depending on your setup)
addresses = [0x20, 0x20, 0x20, 0x20]  # Example addresses for four PCF8575 boards

# Initialize the PCF8575 expanders on the different I2C buses
def init_pcf8575(i2c_bus, address):
    # Perform a simple read to check communication (read the 16-bit GPIO state)
    try:
        data = i2c_bus.readfrom(address, 2)
        print(f"PCF8575 at address 0x{address:02X} is responding.")
        return True
    except Exception as e:
        print(f"Error communicating with PCF8575 at address 0x{address:02X}: {e}")
        return False

# Function to set or clear GPIO pins on the PCF8575 (16-bit control)
def set_pcf8575(i2c_bus, address, value):
    try:
        # Send a 16-bit value to the PCF8575 to control GPIO pins
        i2c_bus.writeto(address, bytearray([value & 0xFF, (value >> 8) & 0xFF]))
        print(f"PCF8575 at address 0x{address:02X} set to value: {value:04X}")
    except Exception as e:
        print(f"Error setting PCF8575 at address 0x{address:02X}: {e}")

# Test the communication with each PCF8575 on all I2C buses
for i, bus in enumerate(i2c_buses):
    print(f"Testing I2C bus {i}...")
    for address in addresses:
        if init_pcf8575(bus, address):
            # Set all pins on the PCF8575 to high (0xFFFF)
            set_pcf8575(bus, address, 0xFFFF)
            time.sleep(1)
            # Set all pins on the PCF8575 to low (0x0000)
            set_pcf8575(bus, address, 0x0000)
            time.sleep(1)
