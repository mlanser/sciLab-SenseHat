import os
import time
from configparser import ConfigParser, ExtendedInterpolation, Error

#from sense_hat import SenseHat
from sense_emu import SenseHat

import click

_FAHRENHEIT_: str = 'F'
_KELVIN_:     str = 'K'
_CELSIUS_:    str = 'C'
  
_TEMP_CONVERTER_ = {
    'C2F': lambda t: ((t * 9/5) + 32),
    'F2C': lambda t: ((t - 32) * 5/9),
    'C2K': lambda t: (t + 273.15),
    'K2C': lambda t: (temp - 273.15),
}  

  
# =========================================================
#              H E L P E R   F U N C T I O N S
# =========================================================
def _process_data():
    pass

  
def _celsius_to_fahrenheit(temp):
    return _TEMP_CONVERTER_['C2F'](temp)
    #return ((temp * 9/5) + 32)

  
def _fahrenheit_to_celsius(temp):
    return _TEMP_CONVERTER_['F2C'](temp)
    #return ((temp - 32) * 5/9)
  
  
def _celsius_to_kelvin(temp):
    return _TEMP_CONVERTER_['C2K'](temp)
    #return (temp + 273.15)

  
def _kelvin_to_celsius(temp):
    return _TEMP_CONVERTER_['K2C'](temp)
    #return (temp - 273.15)

  


# =========================================================
#               C O R E   F U N C T I O N S
# =========================================================
def init_sensor():
    return SenseHat()

def get_temperature(sensor: SenseHat, unit=None):
    if not isinstance(sensor, SenseHat):
        raise TypeError("'sensor' must be of type 'SenseHat'")
    
    if unit == _FAHRENHEIT_:
        return _TEMP_CONVERTER_['C2F'](sensor.get_temperature())        
      
    elif unit == _KELVIN_:
        return _TEMP_CONVERTER_['C2K'](sensor.get_temperature())
    
    return sensor.get_temperature()
  

def get_humidity(sensor: SenseHat):
    if not isinstance(sensor, SenseHat):
        raise TypeError("'sensor' must be of type 'SenseHat'")
    
    return sensor.get_humidity()

  
def get_pressure(sensor: SenseHat):
    if not isinstance(sensor, SenseHat):
        raise TypeError("'sensor' must be of type 'SenseHat'")
    
    return sensor.get_pressure()  

  
def get_orientation(sensor: SenseHat, raw=False):
    if not isinstance(sensor, SenseHat):
        raise TypeError("'sensor' must be of type 'SenseHat'")
    
    pass
  
  
def get_compass(sensor: SenseHat, raw=False):
    if not isinstance(sensor, SenseHat):
        raise TypeError("'sensor' must be of type 'SenseHat'")
    
    pass
  

def get_accelerometer(sensor: SenseHat, raw=False):
    if not isinstance(sensor, SenseHat):
        raise TypeError("'sensor' must be of type 'SenseHat'")
    
    pass
  
  
def get_gyroscope(sensor: SenseHat, raw=False):
    if not isinstance(sensor, SenseHat):
        raise TypeError("'sensor' must be of type 'SenseHat'")
    
    pass
  
def get_data(sensor: SenseHat):
    if not isinstance(sensor, SenseHat):
        raise TypeError("'sensor' must be of type 'SenseHat'")
    
    return {
      'temperature': get_temperature(sensor),
      'humidity': get_humidity(sensor),
      'pressure': get_pressure(sensor),
    }
  
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
if False:
    """

      Sense HAT Sensors Display

      Select Temperature, Pressure, or Humidity  with the Joystick
      to visualize the current sensor values on the LED.

      Note: Requires sense_hat 2.2.0 or later

    """

    sense = SenseHat()

    green = (0, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)


    def show_t():
      sense.show_letter("T", back_colour = red)
      time.sleep(.5)

    def show_p():
      sense.show_letter("P", back_colour = green)
      time.sleep(.5)

    def show_h():
      sense.show_letter("H", back_colour = blue)
      time.sleep(.5)

    def update_screen(mode, show_letter = False):
      if mode == "temp":
        if show_letter:
          show_t()
        temp = sense.temp
        temp_value = temp / 2.5 + 16
        pixels = [red if i < temp_value else white for i in range(64)]

      elif mode == "pressure":
        if show_letter:
          show_p()
        pressure = sense.pressure
        pressure_value = pressure / 20
        pixels = [green if i < pressure_value else white for i in range(64)]

      elif mode == "humidity":
        if show_letter:
          show_h()
        humidity = sense.humidity
        humidity_value = 64 * humidity / 100
        pixels = [blue if i < humidity_value else white for i in range(64)]

      sense.set_pixels(pixels)

    ####
    # Intro Animation
    ####

    show_t()
    show_p()
    show_h()

    update_screen("temp")

    index = 0
    sensors = ["temp", "pressure", "humidity"]

    ####
    # Main game loop
    ####

    while True:
      selection = False
      events = sense.stick.get_events()
      for event in events:
        # Skip releases
        if event.action != "released":
          if event.direction == "left":
            index -= 1
            selection = True
          elif event.direction == "right":
            index += 1
            selection = True
          if selection:
            current_mode = sensors[index % 3]
            update_screen(current_mode, show_letter = True)

      if not selection:      
        current_mode = sensors[index % 3]
        update_screen(current_mode)
