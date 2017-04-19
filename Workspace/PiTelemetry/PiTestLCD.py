import Adafruit_CharLCD as LCD

lcd_rs = 18
lcd_en = 23
lcd_d4 = 12
lcd_d5 = 16
lcd_d6 = 20
lcd_d7 = 21
lcd_bl = 4

# LCD parametreleri
lcd_columns = 20
lcd_rows = 4

lcd = LCD.Adafruit_CharLCD(
    lcd_rs, lcd_en, lcd_d4,
    lcd_d5, lcd_d6, lcd_d7,
    lcd_columns, lcd_rows, lcd_bl)

lcd.clear()

lcd.clear()
lcd.set_cursor(1, 0)
lcd.message('Handling data.')
