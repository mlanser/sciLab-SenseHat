import os

import sqlite3
import csv
import json
import random
import string

import pytest


# =========================================================
#                      G L O B A L S
# =========================================================
_VALID_CONFIG_DATA_ = """\
[data]
retain = -1
history = 1
sort = first

[main]
count = 1
sleep = 60
threads = multi
unit = bits
share = False
location = Some City, US
locationtz = America/New_York
host = {host}
ssl = False
dbtable = TestApp
storage = {storage}
"""

_INVALID_CONFIG_DATA_ = """\
[foo]
retain = -1
history = 1
sort = first

[bar]
count = 1
sleep = 60
threads = multi
unit = bits
share = False
location = Some City, US
locationtz = America/New_York
host = some_long_filename.abc
ssl = False
dbtable = TestApp
storage = FOOBAR
"""

_INVALID_CONFIG_FILE_FORMAT_ = """\
This is not
a valid INI
file format.
"""

_DATA_FLDS_ = {
    'raw':    {'strFld1': str, 'strFld2': str, 'strFld3': str, 'floatFld': float, 'intFld': int},
    'csv':    {'strFld1': None, 'strFld2': None, 'strFld3': None, 'floatFld': None, 'intFld': None},
    'json':   {'strFld1': None, 'strFld2': None, 'strFld3': None, 'floatFld': None, 'intFld': None},
    'sql':    {'strFld1': 'TEXT|idx', 'strFld2': 'TEXT|idx', 'strFld3': 'TEXT', 'floatFld': 'REAL', 'intFld': 'INT'},
}


# =========================================================
#              P Y T E S T   F I X T U R E S
# =========================================================
@pytest.fixture(scope='module')
def author_file_json(tmpdir_factory):
    """Write some authors to a data file."""
    authorData = {
        'Ned': {'City': 'Boston'},
        'Brian': {'City': 'Portland'},
        'Luciano': {'City': 'Sau Paulo'}
    }
    
    authorFile = tmpdir_factory.mktemp('data').join('author_file.json')
    print('file:{}'.format(str(authorFile)))

    with authorFile.open('w') as f:
        json.dump(authorData, f)
        
    return authorFile
  
  
@pytest.fixture(scope='module')
def valid_config_string():
    return _VALID_CONFIG_DATA_
  
@pytest.fixture(scope='module')
def invalid_config_string():
    return _INVALID_CONFIG_
  
@pytest.fixture(scope='module')
def valid_config_ini(tmpdir_factory):
    """Create valid 'config.ini' file for use with tests."""
    testDir = tmpdir_factory.mktemp('test')
    configFile = testDir.join('valid.ini')
    
    dataHost = 'test_data.csv'
    dataStorageType = 'CSV'
    
    configFile.write(_VALID_CONFIG_DATA_.format(host = dataHost, storage = dataStorageType))
    
    return str(configFile)

  
@pytest.fixture(scope='module')
def invalid_config_ini(tmpdir_factory):
    """Create invalid 'config.ini' file for use with tests."""
    testDir = tmpdir_factory.mktemp('test')
    configFile = testDir.join('invalid.ini')
    
    configFile.write(_INVALID_CONFIG_DATA_)
    
    return str(configFile)

  
@pytest.fixture(scope='module')
def invalid_config_ini_fomat(tmpdir_factory):
    """Create 'config.ini' with invalid INI file format for use with tests."""
    testDir = tmpdir_factory.mktemp('test')
    configFile = testDir.join('invalid_fmt.ini')
    
    configFile.write(_INVALID_CONFIG_FILE_FORMAT_)
    
    return str(configFile)

  
@pytest.fixture(scope='module')
def sample_data_fields():
    """Create list with data field headers."""
    
    return _DATA_FLDS_
    

@pytest.fixture()
def valid_sample_data():
    """Create list with valid sample data."""
    
    def _random_string(numChar=5):
        random.seed()
        return ''.join(random.choice(string.ascii_letters) for i in range(numChar))
    
    random.seed()
    data = {
        'strFld1':  _random_string(random.randint(3,7)),    # strFld1
        'strFld2':  _random_string(random.randint(3,7)),    # strFld2
        'strFld3':  _random_string(random.randint(3,7)),    # strFld3
        'floatFld': random.random(),                        # floadFld
        'intFld':   random.randint(0,100),                  # intFld
    }
    
    return data
