import os
import uuid
import random

import pytest
from inspect import currentframe

from tests.unit.helpers import pp
import src.sensors.sensehat

# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
def test_init_sensor(capsys, mocker, recwarn):
    mocker.patch('sense_emu.SenseHat', return_value='foo')
    sensor = src.sensors.sensehat.init_sensor()
    pp(capsys, os.name, currentframe())
    assert sensor is not None
    
    
def test_get_humidity(capsys, mocker, recwarn):
    #data = src.sensors.sensehat.get_humidity(src.sensors.sensehat.init_sensor())
    #pp(capsys, data, currentframe())
    assert True

    
def test_get_data(capsys, mocker, recwarn):
    mocker.patch('src.sensors.sensehat.get_temperature', return_value=100)
    mocker.patch('src.sensors.sensehat.get_humidity', return_value=50)
    mocker.patch('src.sensors.sensehat.get_pressure', return_value=10)
    
    data = src.sensors.sensehat.get_data(src.sensors.sensehat.init_sensor())
    #pp(capsys, data, currentframe())

    assert data == {'temperature': 100, 'humidity': 50, 'pressure': 10}
    #assert len(recwarn) == 1
