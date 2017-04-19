import Adafruit_CharLCD as LCD
import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO
from time import gmtime, strftime, sleep
import serial
from math import pi
import os

# Sems Turgut 09.03.2017 20:56
# Contrast sensoru ile bulunan rpm degeri ile hiz hesabi yapilacak.
# XBee ile verilerin pite gonderilmesi yapilacak. ttyS0 a gore tekrar duzenlenecek
# Restart atildiginda usb portlarini otomatik gorup tekrar baslatilmasi yapilacak. ttyS0 a gore tekrar duzenlenecek
# Modullerin akim degerleri deger asimi var mi diye kontrol edilecek.
# Edit.
# Canim edit.
# GPIO Pinleri belirleniyor.
'''lcd_rs = 18
lcd_en = 23
lcd_d4 = 12
lcd_d5 = 16
lcd_d6 = 20
lcd_d7 = 21
lcd_bl = 4
lcd_cols = 20
lcd_rows = 4'''

# BMS degiskenleri belirleniyor.
htemp_bms = ''
atemp_bms = ''
cur_bms = ''
hvolt_bms = ''
batper_bms = ''

# Arduino dan gelen degiskenler belirleniyor.
BMP085_sensor = BMP085.BMP085()
speed_eng = ''
battemp_eng = 0
battemp_eng_str = ''
cotemp_eng = ''

# LCD ozellikleri belirleniyor.
lcd = LCD.Adafruit_CharLCD(
    lcd_rs, lcd_en, lcd_d4,
    lcd_d5, lcd_d6, lcd_d7,
    lcd_cols, lcd_rows, lcd_bl)

# Buzzer degiskenleri belirleniyor.
buzzer_pin = 17
GPIO.setmode(GPIO.BCM)  # Use the Broadcom method for naming the GPIO pins
GPIO.setup(buzzer_pin, GPIO.OUT)  # Set pin 18 as an output pin


# USB Portlar acik mi diye test ediliyor
def portCheck():
    '''sleep(0.5)
    if os.path.exists('/dev/ttyUSB0'):
        print 'USB ports are OK.'
        lcd.clear()
        lcd.set_cursor(0, 1)
        lcd.message("Butun USB'ler tamam.")
        lcd.set_cursor(0, 2)
        lcd.message('>----Basliyoruz----<')
    else:
        print 'Please check USB ports.'
        lcd.clear()
        lcd.set_cursor(0, 0)
        lcd.message('Lutfen USB yi takin')

        lcd.set_cursor(0, 1)
        lcd.message('BMS:')
        if os.path.exists('/dev/ttyUSB0'):
            lcd.set_cursor(6, 0)
            lcd.message(' OK')
        portCheck()

    ser_bms = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5)'''
    sleep(1)
    lcd.clear()
    # main(ser_bms)
    main()


# Ana fonksiyon.def main(ser_bms)
def main():
    #    print 'Successfully connected to:' + ser_bms.portstr
    while True:
        sleep(.3)
        print strftime("Date :%Y-%m-%d Time :%H:%M:%S", gmtime())
        log = []
        line = []
        # BMS den gelen veriler parse ediliyor.
        '''        if ser_bms.isOpen():
                    while True:
                        try:
                            line = ser_bms.readline().split(',')
                            if ':' not in line[0]:
                                if line[0] == 'BT3':
                                    htemp_bms = str(
                                        (int(line[3], 16) + (-100)) * 1)
                                    atemp_bms = str(
                                        (int(line[4], 16) + (-100)) * 1)
                                if line[0] == 'CV1':
                                    hvolt_bms = str(
                                        int(line[1], 16) * 1 / 100)
                                    cur_bms = str(
                                        int(line[2], 16) * 1 / 10
                                    )
                                if line[0] == 'BC1':
                                    batper_bms = str(
                                        int(line[3], 16) / 100)
                                    line = []
                                    break
                            else:
                                if line[2] == 'BT3':
                                    htemp_bms = str(
                                        (int(line[3], 16) + (-100)) * 1)
                                    atemp_bms = str(
                                        (int(line[4], 16) + (-100)) * 1)
                                if line[2] == 'CV1':
                                    hvolt_bms = str(
                                        int(line[3], 16) * 1 / 100)
                                    cur_bms = str(int(line[4], 16) / 10)
                                if line[2] == 'BC1':
                                    batper_bms = str(
                                        int(line[5], 16) / 100)
                                    line = []
                                    break
                        except (IndexError, ValueError) as e:
                            print e
                            htemp_bms = '0'
                            atemp_bms = '0'
                            cur_bms = '0'
                            hvolt_bms = '0'
                            batper_bms = '0'

                else:
                    print 'BMS|USB0:Handling data problem. Please check connections.'
                    '''
        htemp_bms = '0'
        atemp_bms = '0'
        cur_bms = '0'
        hvolt_bms = '0'
        batper_bms = '0'
        # Sensorlerden gelen verileri degiskenlere aktariyor.
        if str(BMP085_sensor) != '':
            try:
                speed_eng = format(BMP085_sensor.read_pressure())
                battemp_eng = format(BMP085_sensor.read_temperature())
                battemp_eng_str = format(BMP085_sensor.read_temperature())
                cotemp_eng = format(BMP085_sensor.read_altitude())
                if float(battemp_eng) >= 60:
                    GPIO.output(buzzer_pin, True)
                else:
                    GPIO.output(buzzer_pin, False)
                # Tekerlek capina gore hiz hesabi.
                # speed_eng = str(
                #    int(((int(line[1]) * (21 * pi)) / 60) * 0.09144))
            except (IndexError, ValueError) as e:
                print e
                speed_eng = '0'
                battemp_eng = 0
                battemp_eng_str = '0'
                cotemp_eng = '0'
        else:
            print 'BMP085|ENG:Handling data problem. Please check connections.'

        # Veriler 20x4 LCD ekrana yazdiriliyor.
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
            lcd.message(str(speed_eng) + '  KM/H')
            lcd.set_cursor(0, 1)
            lcd.message('CTemp  :')
            lcd.set_cursor(8, 1)
            lcd.message(str(cotemp_eng) + '   C')
            lcd.set_cursor(0, 2)
            lcd.message('BTemp  :')
            lcd.set_cursor(8, 2)
            lcd.message(str(battemp_eng_str) + '   C')
            lcd.set_cursor(0, 3)
            lcd.message('Battery:')
            lcd.set_cursor(8, 3)
            lcd.message('%' + str(batper_bms))
            '''
                    # Parse edilen veriler Xbee ile pit'e gonderiliyor.
                    if ser_xbee.isOpen():
                        if str(speed_eng) != '':
                            print('Speed :' + str(speed_eng) + 'KM/H | CTemp :' +
                                  str(cotemp_eng) + 'C | BTemp :' +
                                  str(battemp_eng_str) + 'C | Battery:' +
                                  str(batper_bms) + '%'
                                  )

                            print('#' + ',' + str(battemp_eng_str) + ',' +
                                  str(cotemp_eng) + ',' +
                                  str(cur_bms) + ',' + str(hvolt_bms) + ',' +
                                  str(speed_eng) + ',' +
                                  str(batper_bms) + ',' + '?')

                            ser_xbee.writelines('#' + ',' + str(battemp_eng_str) + ',' +
                                                str(cotemp_eng) + ',' +
                                                str(cur_bms) + ',' + str(hvolt_bms) + ',' +
                                                str(speed_eng) + ',' +
                                                str(batper_bms) + ',' + '?')
                    else:
                        print 'XBee|Comm:Sending data problem. Please check connections.'
            '''
'''
        with open('/home/pi/TELEMETRY_LOG.txt', 'a') as file:
            file.write(
                strftime("Date :%Y-%m-%d Time :%H:%M:%S", gmtime()) + '\n')
            file.write('htemp_bms :' + htemp_bms + 'atemp_bms :' + atemp_bms +
                       'cur_bms :' + cur_bms + 'hvolt_bms :' + hvolt_bms +
                       'batper_bms :' + batper_bms + '\n')
            file.write('speed_eng :' + speed_eng + 'battemp_eng_str :' +
                       battemp_eng_str + 'cotemp_eng' + cotemp_eng + '\n')
            file.close()
'''


def splash():
    lcd.clear()
    while True:
        lcd.set_cursor(0, 3)
        lcd.message("USB'leri cikariniz.")
        lcd.set_cursor(0, 0)
        lcd.message('USB0 :')
        if not os.path.exists('/dev/ttyUSB0'):
            lcd.set_cursor(6, 0)
            lcd.message(' OK')

        lcd.set_cursor(0, 1)
        lcd.message('USB1 :')
        if not os.path.exists('/dev/ttyUSB1'):
            lcd.set_cursor(6, 1)
            lcd.message(' OK')

        lcd.set_cursor(0, 2)
        lcd.message('USB2 :')
        if not os.path.exists('/dev/ttyUSB2'):
            lcd.set_cursor(6, 2)
            lcd.message(' OK')

        if not os.path.exists('/dev/ttyUSB0'):
            if not os.path.exists('/dev/ttyUSB1'):
                if not os.path.exists('/dev/ttyUSB2'):
                    sleep(.3)
                    break

        sleep(0.2)

    lcd.clear()
    lcd.set_cursor(0, 0)
    lcd.message('<--BULENT ECEVIT-->')
    lcd.set_cursor(0, 1)
    lcd.message('   MUH. FAKULTESI   ')
    lcd.set_cursor(0, 2)
    lcd.message('    ROBOT KULUBU    ')
    lcd.set_cursor(0, 3)
    lcd.message('>-----VOLTRAN-----<')
    sleep(3)

    cnt = 3
    while True:
        lcd.clear()
        lcd.set_cursor(0, cnt)
        lcd.message('<----YUKLENIYOR---->')
        print '<----YUKLENIYOR---->'
        cnt = cnt - 1
        if cnt < 0:
            break
        sleep(.5)


try:
    splash()
    portCheck()
except KeyboardInterrupt:
    print 'Interrupted. LCD is clear now.'
    lcd.clear()
