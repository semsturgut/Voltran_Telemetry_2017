import serial
import time

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.5)

temp1 = 25
coctemp = 35
cur = 90
volt = 12
speed = 60

if ser.isOpen:
    while True:
        print('#' + ',' + str(temp1) + ',' +
              str(coctemp) + ',' +
              str(cur) + ',' + str(volt) + ',' +
              str(speed) + ',' + '?')

        ser.writelines('#' + ',' + str(temp1) + ',' +
                       str(coctemp) + ',' +
                       str(cur) + ',' + str(volt) + ',' +
                       str(speed) + ',' + '?')

        time.sleep(1)
