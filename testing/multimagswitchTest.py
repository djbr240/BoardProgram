from machine import I2C, Pin
import utime

# Initialize a single I2C bus for all PCF8575 boards
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)  # I2C on GP4 and GP5

# PCF8575 I2C addresses
PCF8575_ADDRESSES = [0x20, 0x21, 0x22, 0x23]

# Read data from a specific PCF8575
def read_port(i2c, address):
    data = bytearray(2)
    i2c.readfrom_into(address, data)
    return data[0] | (data[1] << 8)

# Write data to a specific PCF8575
def write_port(i2c, address, value):
    data = bytearray([value & 0xFF, (value >> 8) & 0xFF])
    i2c.writeto(address, data)

# Read a specific pin state (0-15) from a specific PCF8575
def read_pin(i2c, address, pin):
    port_value = read_port(i2c, address)
    return (port_value >> pin) & 1

# Initialize all pins to low state on all PCF8575 boards
for address in PCF8575_ADDRESSES:
    write_port(i2c, address, 0x0000)

# Continuously read and print the pin states of all PCF8575 boards
while True:
    for i, address in enumerate(PCF8575_ADDRESSES):
        try:
            port_value = read_port(i2c, address)
            print(f"PCF8575 Board {i} (Address {address:#02x}) Raw Value: {bin(port_value)}")

            for pin in range(16):
                pin_state = read_pin(i2c, address, pin)
                print(f"Board {i} Pin {pin}: {'HIGH' if pin_state else 'LOW'}")
        except OSError as e:
            print(f"Error reading from PCF8575 at address {address:#02x}: {e}")
    utime.sleep(1)
