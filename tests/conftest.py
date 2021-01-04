import os

import sqlite3
import csv
import json

import pytest

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
    """Create 'config.ini' witn invalid INI file format for use with tests."""
    testDir = tmpdir_factory.mktemp('test')
    configFile = testDir.join('invalid_fmt.ini')
    
    configFile.write(_INVALID_CONFIG_FILE_FORMAT_)
    
    return str(configFile)
  