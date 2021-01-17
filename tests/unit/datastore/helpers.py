import random

import pprint
import pytest


# =========================================================
#       L I T T L E   H E L P E R   F U N C T I O N S
# =========================================================
def valid_sample_data(faker):
    """Create list with valid sample data."""
    
    random.seed()
    data = {
        'strFld1':  faker.word(),           # strFld1
        'strFld2':  faker.word(),           # strFld2
        'strFld3':  faker.word(),           # strFld3
        'floatFld': random.random(),        # floadFld
        'intFld':   random.randint(0,100),  # intFld
    }
    
    return data
  
  
def invalid_sample_data(faker):
    """Create list with invalid sample data."""
    
    random.seed()
    data = {
        'strFld1':  faker.word(),           # strFld1
        'strFld2':  faker.word(),           # strFld2
        'strFld3':  faker.word(),           # strFld3
        'floatFld': faker.word(),           # floadFld -- data not float
        'intFld':   faker.word(),           # intFld   -- data not int
    }
    
    return data
