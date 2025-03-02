import sys
import select
from machine import UART, Pin

uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))

while True:
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        uart1.write(sys.stdin.read(1))
    if uart1.any():
        sys.stdout.write(uart1.read(1).decode())
