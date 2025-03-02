import serial
ser = serial.Serial("COM10", 115200, timeout=1)
ser.write(b'Hello Pico\n')
print(ser.readline().decode())
ser.close()
