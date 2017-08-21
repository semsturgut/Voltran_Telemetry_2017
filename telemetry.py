import Adafruit_CharLCD as LCD
import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO
from time import gmtime, strftime, sleep
import serial
from math import pi
import os
from time import sleep
from datetime import datetime
from datetime import timedelta

# Sems Turgut 09.03.2017 20:56
# Modullerin akim degerleri deger asimi var mi diye kontrol edilecek.

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

# BMS degiskenleri belirleniyor.
htemp_bms = ''
atemp_bms = ''
cur_bms = ''
hvolt_bms = ''
batper_bms = ''

# Sensorlerden gelen degiskenler belirleniyor.
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

# Hiz sensoru degiskenleri belirlleniyor.
GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.IN)
a = 1
hiz = 0
hiz1 = 0
eski_zaman = 0
yeni_zaman = 0
zaman = 0

# millis () fonksiyonu icin degisken tanimi
start_time = datetime.now()
dt = 0
ms = 0
count_next_millis = 0
count_past_millis = 1

# Sleep fonksiyonu yerine kullandigimiz millis fonksiyonu


def millis():
    dt = datetime.now() - start_time
    global ms
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * \
        1000 + dt.microseconds / 1000
    return ms

# USB Portlar acik mi diye test ediliyor


def portCheck():
    sleep(0.5)
    '''
    if os.path.exists('/dev/ttyUSB0') and os.path.exists('/dev/ttyS0'):
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
        lcd.message('Check connections')

        lcd.set_cursor(0, 1)
        lcd.message('BMS:')
        if os.path.exists('/dev/ttyUSB0'):
            lcd.set_cursor(6, 0)
            lcd.message(' OK')

        lcd.set_cursor(0, 2)
        lcd.message('Xbee:')
        if os.path.exists('/dev/ttyS0'):
            lcd.set_cursor(7, 2)
            lcd.message(' OK')

        portCheck()

    ser_bms = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5)
    '''
    ser_xbee = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5)

    sleep(1)
    welcome_Voltran()
    lcd.clear()
    main(ser_xbee)


# Ana fonksiyon
def main(ser_xbee):
    while True:

        global count_next_millis
        global count_past_millis

        if millis() % 1000 == 0:
            count_next_millis += 1
            sleep(.01)

        yeni_zaman = ms
        light_sensor = GPIO.input(8)

        if light_sensor == 1:
            global zaman
            global hiz
            global eski_zaman
            if a == 0:
                try:
                    zaman = yeni_zaman - eski_zaman
                    hiz = (4596.12) / (zaman)
                except ArithmeticError as e:
                    print e
                    hiz = 0
                zaman = yeni_zaman - eski_zaman
                if zaman:
                    hiz = (4596) / (zaman)
                    hiz1 = hiz
                else:
                    hiz = hiz1
            # global eski_zaman
            eski_zaman = yeni_zaman
            a = 1
        if light_sensor == 0:
            a = 0

        if count_next_millis > count_past_millis:
            print strftime("Date :%Y-%m-%d Time :%H:%M:%S", gmtime())
        log = []
        line = []
        # BMS den gelen veriler parse ediliyor.
        '''
        if count_next_millis > count_past_millis:
            if ser_bms.isOpen():
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

        # TODO: Bu degiskenler BMS acildiginda silinecek!!
        htemp_bms = '0'
        atemp_bms = '0'
        cur_bms = '0'
        hvolt_bms = '0'
        batper_bms = '0'
        # Sensorlerden gelen verileri degiskenlere aktariyor.
        if count_next_millis > count_past_millis:
            if str(BMP085_sensor) != '':
                try:
                    speed_eng = hiz
                    battemp_eng = format(BMP085_sensor.read_temperature())
                    battemp_eng_str = format(BMP085_sensor.read_temperature())
                    cotemp_eng = format(BMP085_sensor.read_temperature())
                    if float(battemp_eng) >= 60:
                        GPIO.output(buzzer_pin, True)
                    else:
                        GPIO.output(buzzer_pin, False)
                except (IndexError, ValueError) as e:
                    print e
                    speed_eng = '0'
                    battemp_eng = 0
                    battemp_eng_str = '0'
                    cotemp_eng = '0'
            else:
                print 'BMP085|ENG:Handling data problem. Please check connections.'

        # Veriler 20x4 LCD ekrana yazdiriliyor.
        if count_next_millis > count_past_millis:
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

        # Parse edilen veriler Xbee ile pit'e gonderiliyor.
        if count_next_millis > count_past_millis:
            if ser_xbee.isOpen():
                if str(speed_eng) != '':
                    print('Speed :' + str(speed_eng) + 'KM/H | CTemp :' +
                          str(cotemp_eng) + 'C | BTemp :' +
                          str(battemp_eng_str) + 'C | Battery:' +
                          str(batper_bms) + '%'
                          )

                    print('Telemetry Data: #' + ',' +
                          str(battemp_eng_str) + ',' +
                          str(cotemp_eng) + ',' +
                          str(cur_bms) + ',' + str(hvolt_bms) + ',' +
                          str(speed_eng) + ',' +
                          str(batper_bms) + ',' + '?' + '\n')

                    ser_xbee.writelines('#' + ',' + str(battemp_eng_str) + ',' +
                                        str(cotemp_eng) + ',' +
                                        str(cur_bms) + ',' + str(hvolt_bms) + ',' +
                                        str(speed_eng) + ',' +
                                        str(batper_bms) + ',' + '?')
            else:
                print 'XBee|Comm:Sending data problem. Please check connections.'

        # Telemtri sisteminin log kaydi tutuluyor.

        if count_next_millis > count_past_millis:
            with open('/home/pi/TELEMETRY_LOG.txt', 'a') as file:
                file.write(
                    strftime("Date :%Y-%m-%d Time :%H:%M:%S", gmtime()) + '\n')
                # TODO:BMS kodu acildiginda burasi da acilacak.
                file.write('htemp_bms :' + htemp_bms + ' atemp_bms :' + atemp_bms +
                           ' cur_bms :' + cur_bms + ' hvolt_bms :' + hvolt_bms +
                           ' batper_bms :' + batper_bms + '\n')
                file.write('speed_eng :' + str(speed_eng) + ' battemp_eng_str :' +
                           str(battemp_eng_str) + ' cotemp_eng :' + str(cotemp_eng) + '\n')
                file.close()

        count_past_millis = count_next_millis


# Hos geldiniz fonksiyonu.
def welcome_Voltran():
    lcd.clear()
    lcd.set_cursor(0, 0)
    lcd.message('<--BULENT ECEVIT-->')
    lcd.set_cursor(0, 1)
    lcd.message('   MUH. FAKULTESI   ')
    lcd.set_cursor(0, 2)
    lcd.message('    ROBOT KULUBU    ')
    lcd.set_cursor(0, 3)
    lcd.message('>---VOLTRAN-2017---<')
    sleep(3)

    cnt = 3
    while True:
        lcd.clear()
        lcd.set_cursor(0, cnt)
        lcd.message('--MERHABA OZGURBEY--')
        print '--MERHABA OZGURBEY--'
        cnt = cnt - 1
        if cnt < 0:
            break
        sleep(.5)


try:
    portCheck()
except KeyboardInterrupt:
    print 'Interrupted. LCD is clear now.'
    lcd.clear()
