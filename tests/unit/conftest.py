import os
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


# =========================================================
#  U N I T   T E S T I N G   P Y T E S T   F I X T U R E S
# =========================================================
@pytest.fixture(scope='module')
def valid_config_string():
    return _VALID_CONFIG_DATA_


@pytest.fixture(scope='module')
def invalid_config_string():
    return _INVALID_CONFIG_DATA_


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
