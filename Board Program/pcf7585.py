from machine import I2C, Pin
import utime
from config import *

# Read data from a specific PCF8575
def read_port(i2c, address):
    data = bytearray(2)
    i2c.readfrom_into(address, data)
    return data[0] | (data[1] << 8)

# Read a specific pin state (0-15) from a specific PCF8575
def read_pin(i2c, address, pin):
    port_value = read_port(i2c, address)
    return (port_value >> pin) & 1

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

# Write data to a specific PCF8575
def write_port(i2c, address, value):
    data = bytearray([value & 0xFF, (value >> 8) & 0xFF])
    i2c.writeto(address, data)

# Set a specific pin state (0-15) on a specific PCF8575
def write_pin(i2c, address, pin, value):
    port_value = read_port(i2c, address)
    if value:
        port_value |= (1 << pin)
    else:
        port_value &= ~(1 << pin)
    write_port(i2c, address, port_value)

