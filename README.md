# Gravity DFRobot DFR0645-G DFR0645-R TM1650
Software I2C micropython implementation driver for 4 digit 8 segment LED display for ESP32.

## tm1650 library

source file: [tm1650.py](./tm1650.py)


### Initialise display

```
from tm1650 import TM1650
disp = TM1650(sda_pin, scl_pin)
```
parameters:

**sda_pin** - esp32 pin number where display SDA pin is connected.

**scl_pin** - esp32 pin number where display SDA pin is connected.


### Turn on display

```
function display_on()
```

### Turn off display

```
function display_off()
```

### Clear display

```
function display_clear()
```

### Display integer

Display integer number with right align on display (without trailing zeroes). If number is out of range display shows **Err**.
```
function display_integer(num)
```

parameters:

**num** - integer number to display from range [-999,9999].


### Display float

Display float number.  If number is out of range display shows **Err**. Displayed number is always aligned to left side of display.
```
function display_float(num)
```

parameters:

**num** - float number to display from range [-999.0,9999.0]


First is displayed sign (if exists), integer part of number, decimal point (always displayed) and the fractional part.
So if integer part of number has 4 digit including sign then fractional part won't be displayed

Example:

| parameter  | output  |
|------------|---------|
| -1         | -1.00   |
| 1.0        | 1.000   |
| -2.202     | -2.20   |
| 23.45      | 23.45   |
| -23.45     | -23.4   |
| -999.123   | -999.   |

### Display string

```
function display_string(s)
```

Display the first four characters of `s`.

Only certain characters can be displayed. If a character is not recognised it will display as "-". Add your own in `SEGMENT_MAP`.

## Example

```
from tm1650 import TM1650

SDA_PIN = 0
SCL_PIN = 1
disp = TM1650(SDA_PIN, SCL_PIN)

disp.display_on()

def scroll_string(s):
  s = s.upper()
  doublemsg = s + s
  for i in range(len(s) - 3):
    disp.display_string(doublemsg[i:4+i])
    sleep(0.5)

scroll_string("Hello Python")

for i in range(10000):
  disp.display_integer(i)

disp.display_clear()
disp.display_off()
```
