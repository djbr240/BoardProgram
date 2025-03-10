from machine import Pin, I2C

# Function to scan I2C devices
def scan_i2c_bus(i2c_bus):
    devices = i2c_bus.scan()
    if devices:
        print(f"Devices found on bus: {devices}")
    else:
        print("No devices found on bus")

# Define I2C buses
i2c_buses = [
    I2C(0, scl=Pin(5), sda=Pin(4), freq=400000),  # I2C on GP0 and GP1
    I2C(1, scl=Pin(7), sda=Pin(6), freq=400000),  # I2C on GP2 and GP3
    I2C(0, scl=Pin(9), sda=Pin(8), freq=400000),  # I2C on GP4 and GP5
    I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)  # I2C on GP6 and GP7
]

# Scan each I2C bus for connected devices
for i, bus in enumerate(i2c_buses):
    print(f"Scanning I2C bus {i}...")
    scan_i2c_bus(bus)
