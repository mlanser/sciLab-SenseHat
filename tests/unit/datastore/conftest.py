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
_DATA_FLDS_ = {
    'raw':    {'strFld1': str, 'strFld2': str, 'strFld3': str, 'floatFld': float, 'intFld': int},
    'csv':    {'strFld1': None, 'strFld2': None, 'strFld3': None, 'floatFld': None, 'intFld': None},
    'json':   {'strFld1': None, 'strFld2': None, 'strFld3': None, 'floatFld': None, 'intFld': None},
    'sql':    {'strFld1': 'TEXT|idx', 'strFld2': 'TEXT|idx', 'strFld3': 'TEXT', 'floatFld': 'REAL', 'intFld': 'INT'},
}

_VALID_DATA_ROW_ = {'strFld1': 'val1', 'strFld2': 'val2', 'strFld3': 'val3', 'floatFld': 4.0, 'intFld': 5}
_TRUNCATED_DATA_ROW_ = {'strFld1': 'val1', 'strFld2': 'val2', 'floatFld': 4.0, 'intFld': 5, 'fruit': 'banana'}
_INVALID_DATA_ROW_ = {'strFld1': 'val1', 'fruit': 'banana', 'strFld3': 'val3', 'floatFld': 'NOT FLOAT', 'intFld': 5}


# =========================================================
#     D A T A S T O R E   P Y T E S T   F I X T U R E S
# =========================================================
@pytest.fixture(scope='module')
def sample_data_fields():
    return _DATA_FLDS_

  
@pytest.fixture(scope='module')
def valid_data_row():
    return _VALID_DATA_ROW_

  
@pytest.fixture(scope='module')
def invalid_data_row():
    return _INVALID_DATA_ROW_

  
@pytest.fixture(scope='module')
def truncated_data_row():
    return _TRUNCATED_DATA_ROW_

  
  