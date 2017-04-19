import Adafruit_CharLCD as LCD
import time
import serial

# Sems Turgut 30.07.2016 22:22

# Scrpitle baslatma eklenecek.
# Tekrar deneme eklenecek.
# Hatalar duzeltilecek.


# GPIO Pinleri belirleniyor.
lcd_rs = 18
lcd_en = 23
lcd_d4 = 12
lcd_d5 = 16
lcd_d6 = 20
lcd_d7 = 21
lcd_bl = 4
lcd_cols = 20
lcd_rows = 4

htemp_bms = '-1'
atemp_bms = '-1'
cur_bms = '-1'
hvolt_bms = '-1'

speed_eng = '-1'
battemp_eng = '-1'
cotemp_eng = '-1'

lcd = LCD.Adafruit_CharLCD(
    lcd_rs, lcd_en, lcd_d4,
    lcd_d5, lcd_d6, lcd_d7,
    lcd_cols, lcd_rows, lcd_bl)


try:

    ser_bms = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5)

    ser_eng = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5)

    ser_xbee = serial.Serial(
        port='/dev/ttyUSB2',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5)

except serial.SerialException as e:
    print e


def main():
    lcd.clear()
    cnt = 0
    print 'Connected to:' + ser_bms.portstr
    print 'Connected to:' + ser_eng.portstr
    print 'Connected to:' + ser_xbee.portstr

    while True:
        print time.localtime()
        log = []
        line = []
        if ser_bms.isOpen():
            while True:
                try:
                    line = ser_bms.readline().split(',')
                    if ':' not in line[0]:
                        if line[0] == 'BT3':
                            htemp_bms = str((int(line[3], 16) + (-100)) * 1)
                            atemp_bms = str((int(line[4], 16) + (-100)) * 1)
                            # Duzeltilecek ACIL !!!!!@@@@
                            log.append(htemp_bms)
                            log.append(atemp_bms)
                        if line[0] == 'CV1':
                            hvolt_bms = str(
                                (int(line[1], 16) + (-0)) * 1 / 100)
                            cur_bms = str((int(line[2], 16) + (-0)) *
                                          1 / 10)  # list index out of range
                            # Duzeltilecek ACIL !!!!!@@@@
                            log.append(hvolt_bms)
                            log.append(cur_bms)
                            line = []
                            break
                    else:
                        if line[2] == 'BT3':
                            htemp_bms = str((int(line[3], 16) + (-100)) * 1)
                            atemp_bms = str((int(line[4], 16) + (-100)) * 1)
                            # Duzeltilecek ACIL !!!!!@@@@
                            log.append(htemp_bms)
                            log.append(atemp_bms)
                        if line[2] == 'CV1':
                            hvolt_bms = str(
                                (int(line[3], 16) + (-0)) * 1 / 100)
                            cur_bms = str(int(line[4], 16) *
                                          1 / 10)  # list index out of range
                            # Duzeltilecek ACIL !!!!!@@@@
                            log.append(hvolt_bms)
                            log.append(cur_bms)
                            line = []
                            break
                except IndexError as e:
                    print e
                    htemp_bms = '-1'
                    atemp_bms = '-1'
                    cur_bms = '-1'
                    hvolt_bms = '-1'

        else:
            print 'USB0|BMS:Handling data problem. Please check connections.'

        if ser_eng.isOpen():  # Parse sistemi degisecek
            try:
                line = []
                line = ser_eng.readline().split(',')
                speed_eng = line[1]
                battemp_eng = line[2]
                cotemp_eng = line[3]  # index out of range
                # Duzeltilecek ACIL !!!!!@@@@
                log.append(speed_eng)
                log.append(battemp_eng)
                log.append(cotemp_eng)
            except IndexError as e:
                print e
                speed_eng = ''
                battemp_eng = ''
                cotemp_eng = ''

        else:
            print 'USB1|ENG:Handling data problem. Please check connections.'

        if str(speed_eng) != '':

            lcd.set_cursor(8, 0)
            lcd.message('    ')
            lcd.set_cursor(8, 1)
            lcd.message('    ')
            lcd.set_cursor(8, 2)
            lcd.message('    ')
            lcd.set_cursor(8, 3)
            lcd.message('    ')

            lcd.set_cursor(0, 0)
            lcd.message('Speed  :')
            lcd.set_cursor(8, 0)
            lcd.message(str(speed_eng))
            lcd.set_cursor(0, 1)
            lcd.message('Temper1:')
            lcd.set_cursor(8, 1)
            lcd.message(str(battemp_eng))
            lcd.set_cursor(0, 2)
            lcd.message('Temper2:')
            lcd.set_cursor(8, 2)
            lcd.message(str(cotemp_eng))
            lcd.set_cursor(0, 3)
            lcd.message('Current:')
            lcd.set_cursor(8, 3)
            lcd.message(str(cur_bms))

        if ser_xbee.isOpen():
            if str(speed_eng) != '':
                print('#' + ',' + str(battemp_eng) + ',' +
                      str(cotemp_eng) + ',' +
                      str(cur_bms) + ',' + str(hvolt_bms) + ',' +
                      str(speed_eng) + ',' + '?')

                ser_xbee.writelines('#' + ',' + str(battemp_eng) + ',' +
                                    str(cotemp_eng) + ',' +
                                    str(cur_bms) + ',' + str(hvolt_bms) + ',' +
                                    str(speed_eng) + ',' + '?')
        else:
            print 'USB2|XBEE:Sending data problem. Please check connections.'

        # with open('BMS_LOG.txt', 'a') as file:
        #    file.write(log)


try:
    main()
except KeyboardInterrupt:
    print 'Interrupted.'
