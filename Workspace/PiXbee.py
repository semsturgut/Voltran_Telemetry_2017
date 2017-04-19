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
a = 0

if ser.isOpen:
    while True:
        a = a + 1
        ser.writelines('#' + temp1 + ',' + coctemp + ',' +
                       cur + ',' + volt + ',' + speed + '?')
        print 'sel :' + str(a)
        time.sleep(0.5)
