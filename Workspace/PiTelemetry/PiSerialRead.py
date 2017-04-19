import serial

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.5)

line = ''

if ser.isOpen():
    print 'Connected to:' + ser.portstr
    while True:
        line = ser.readline()
        print line

else:
    print 'Serial is not available.'


# for c in ser.read():
#    if c == '\r':
#        print line
#        line = []
#        break
#    else:
#        line.append(c)

ser.close()
