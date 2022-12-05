# stonatm@gmail.com
# Gravity DFRobot DFR0645-R DFR0645-G
# TM1650 4 digit 8 segment led display
# i2c software implementation
# esp32 micropython driver

from machine import Pin, SoftI2C

class TM1650():

  def __init__(self, sda_pin, scl_pin):
    self.dbuf = bytearray(4)
    self.tbuf = bytearray(1)
    self.i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100000)
    self.display_on()

  def display_on(self):
    self.i2c.writeto(0x24, b'0x81')

  def display_off(self):
    self.i2c.writeto(0x24, b'0x80')

  def __clear_all(self):
    self.tbuf[0] = 0
    for i in range(4):
      self.dbuf[i] = self.tbuf[0]

  def __clear_digit(self, pos):
    self.tbuf[0] = 0
    self.dbuf[pos%4] = self.tbuf[0]

  def __digit(self,num):
    dig= [63, 6, 91, 79, 102, 109, 124, 7, 127, 103]
    return(dig[num%10])

  def __set_digit(self, pos, value):
    self.tbuf[0] = self.__digit(value%10)
    self.dbuf[pos%4] = self.tbuf[0]

  def __set_raw_value(self, pos, value):
    self.tbuf[0] = int(value%256)
    self.dbuf[pos%4] = self.tbuf[0]

  def __set_dp(self, pos):
    self.tbuf[0] = self.dbuf[pos%4]|0x80
    self.dbuf[pos%4] = self.tbuf[0]

  def __clear_dp(self, pos):
    self.tbuf[0] = self.dbuf[pos%4]&0x7f
    self.dbuf[pos%4] = self.tbuf[0]

  def __send_buf(self):
    for i in range(4):
      self.tbuf[0] = self.dbuf[i]
      self.i2c.writeto(0x34+i, self.tbuf)

  def __display_error(self):
    self.__clear_all()
    self.__set_raw_value(0,121)
    self.__set_raw_value(1,80)
    self.__set_raw_value(2,80)
    self.__send_buf()

  def display_integer(self, num):
    if (num >= 0) and (num <= 9999):
      t = str(int(num))
      self.__clear_all()
      for i in range(len(t)):
        digit = int(str( t[len(t)-1-i] ))
        self.__set_digit(3-i, digit)
    elif (num < 0) and (num >= -999):
      t = str(int(-num))
      self.__clear_all()
      for i in range(len(t)):
        digit = int(str( t[len(t)-1-i] ))
        self.__set_digit(3-i, digit)
      self.__set_raw_value(0,64)
    else:
      self.__display_error()
    self.__send_buf()

  def display_float(self, num):
    self.__clear_all()
    number = str(num)
    dot_pos= number.find('.',0)
    sign = ( number[0] == '-')
    if dot_pos>=0:
      int_part = number[0:dot_pos]
      fract_part = number[dot_pos+1:]
    else:
      int_part = number
      fract_part = ''
      dot_pos = len(int_part)
    if sign:
      int_part = int_part[1:]
      dot_pos = dot_pos-1
    if len(int_part)>4:
      self.__display_error()
      return
    if sign and (len(int_part)>3):
      self.__display_error()
      return
    fract_part = fract_part+'0000'
    out = int_part + fract_part
    if sign:
      for i in range(1,4):
        self.__set_digit(i, int(out[i-1]))
      self.__set_raw_value(0, 64)
      self.__set_dp(dot_pos)
    else:
      for i in range(4):
        self.__set_digit(i, int(out[i]))
        self.__set_dp(dot_pos-1)      
    self.__send_buf()

  def display_clear(self):
    self.__clear_all()
    self.__send_buf()
