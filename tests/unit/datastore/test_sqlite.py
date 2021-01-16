import os
import sqlite3
import uuid
import random

import pprint
import pytest
from inspect import currentframe, getframeinfo

import src.utils.datastore.sqlite


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_HDR_FLDS_RAW_ = {'strFld1': str, 'strFld2': str, 'strFld3': str, 'floatFld': float, 'intFld': int}
_HDR_FLDS_SQL_ = {'strFld1': 'TEXT|idx', 'strFld2': 'TEXT|idx', 'strFld3': 'TEXT', 'floatFld': 'REAL', 'intFld': 'INT'}
_VALID_DATA_ROW_ = {'strFld1': 'val1', 'strFld2': 'val2', 'strFld3': 'val3', 'floatFld': 4.0, 'intFld': 5}
_TRUNCATED_DATA_ROW_ = {'strFld1': 'val1', 'strFld2': 'val2', 'floatFld': 4.0, 'intFld': 5, 'fruit': 'banana'}
_INVALID_DATA_ROW_ = {'strFld1': 'val1', 'fruit': 'banana', 'strFld3': 'val3', 'floatFld': 'NOT FLOAT', 'intFld': 5}

_EVEN_DATA_4xROWS_5xFLDS = [
    {"strFld1": "r1Val1","strFld2": "r1Val2","strFld3": "r1Val3","floatFld": "1.1","intFld": 10},
    {"strFld1": "r2Val1","strFld2": "r2Val2","strFld3": "r2Val3","floatFld": "2.2","intFld": 20},
    {"strFld1": "r3Val1","strFld2": "r3Val2","strFld3": "r3Val3","floatFld": "3.3","intFld": 30},
    {"strFld1": "r4Val1","strFld2": "r4Val2","strFld3": "r4Val3","floatFld": "4.4","intFld": 40}
]

_UNEVEN_DATA_5xROWS_NxFLDS = [
    {"strFld1": "r1Val1","strFld2": "r1Val2","floatFld": "1.1","intFld": 10},
    {"strFld1": "r2Val1","strFld2": "r2Val2","strFld3": "r2Val3","floatFld": "2.2"},
    {"strFld1": "r3Val1","strFld2": "r3Val2"},
    {"strFld1": "r4Val1","strFld2": "r4Val2","strFld3": "r4Val3","floatFld": "4.4","intFld": 40,"foo": "bar","fizz": "buzz"}
]


@pytest.fixture()
def binary_data_file(tmpdir_factory):
    """Create a binary data file."""
    testDir = tmpdir_factory.mktemp('test')
    dataFile = testDir.join(uuid.uuid4().hex + '.bin')
    
    with open(str(dataFile),'wb') as fp:
        fp.write(bytes('First line\n2nd line\na third line', encoding="utf-8"))
    
    return str(dataFile)


@pytest.fixture()
def empty_data_file(tmpdir_factory):
    """Create an empty data file."""
    testDir = tmpdir_factory.mktemp('test')
    dataFile = testDir.join(uuid.uuid4().hex + '.sqlite')
    
    dataFile.write('')
    
    return str(dataFile)


@pytest.fixture()
def new_data_file(tmpdir_factory):
    """Only create the filename, but not the actual file."""
    testDir = tmpdir_factory.mktemp('test')
    dataFile = testDir.join(uuid.uuid4().hex + '.sqlite')
    
    return str(dataFile)


    
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
  
  
def pp(capsys, data, frame=None):  
    with capsys.disabled():
        _PP_ = pprint.PrettyPrinter(indent=4)
        print('\n')
        if frame is not None:
            print('LINE #: {}\n'.format(getframeinfo(frame).lineno))
        _PP_.pprint(data)

    
# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
def test_save_data(capsys, faker, sample_data_fields, new_data_file):
    """Happy path! Save data to database."""
    random.seed()
    dataOut = [valid_sample_data(faker) for i in range(random.randint(1,10))]
    dataHdrs = sample_data_fields
    dataFName = new_data_file
    tblName = '_TEST_TABLE_'

    src.utils.datastore.sqlite.save_data(dataOut, dataFName, dataHdrs['sql'], tblName, True)
    
    dbConn = src.utils.datastore.sqlite._connect_server(dataFName, False)
    dbCur = dbConn.cursor()
    tableExists = src.utils.datastore.sqlite._exist_table(dbCur, tblName)
    assert tableExists
    

def test_save_data_w_bad_params(capsys, faker, sample_data_fields, empty_data_file, new_data_file):
    """Test with invalid parameters."""
    random.seed()
    dataOut = [invalid_sample_data(faker) for i in range(random.randint(1,10))]
    dataHdrs = sample_data_fields
    dataFName = new_data_file
    tblName = '_TEST_TABLE_'

    # Test writing to 'None' as filename
    with pytest.raises(TypeError) as excinfo:
        src.utils.datastore.sqlite.save_data(dataOut, None, dataHdrs['sql'], tblName, False)
    exMsg = excinfo.value.args[0]
    assert 'path should be string, bytes, os.PathLike or integer' in exMsg

    # Test writing to non-existant file with incorrect 'force' flag
    with pytest.raises(OSError) as excinfo:
        src.utils.datastore.sqlite.save_data(dataOut, '--INVALID--', dataHdrs['sql'], tblName, False)
    exMsg = excinfo.value.args[0]
    assert exMsg == "SQLite data file '--INVALID--' does not exist!"

    # Test bad data headers   
    with pytest.raises(AttributeError) as excinfo:
        src.utils.datastore.sqlite.save_data(dataOut, dataFName, None, tblName, True)
    exMsg = excinfo.value.args[0]
    assert exMsg == "'NoneType' object has no attribute 'items'"
    
    
def test_get_data(capsys, faker, sample_data_fields, new_data_file):
    """Happy path! Get data from databse."""
    random.seed()
    numRecs = random.randint(1,10)
    dataOut = [valid_sample_data(faker) for i in range(numRecs)]
    dataHdrs = sample_data_fields
    dataFName = new_data_file
    tblName = '_TEST_TABLE_'

    src.utils.datastore.sqlite.save_data(dataOut, dataFName, dataHdrs['sql'], tblName, True)
    dataIn = src.utils.datastore.sqlite.get_data(dataFName, dataHdrs['sql'], tblName, None, numRecs)

    assert len(dataIn) == len(dataOut)
    assert len(dataIn[0]) == len(dataOut[0])
    
    allExist = True
    for rec in dataOut:
        if rec not in dataIn:
            allExist = False
    assert allExist

    dataIn = src.utils.datastore.sqlite.get_data(dataFName, _HDR_FLDS_RAW_, tblName, None, 0)
    assert len(dataIn) == 0

    dataIn = src.utils.datastore.sqlite.get_data(dataFName, _HDR_FLDS_RAW_, tblName, None, 999)
    assert len(dataIn) == numRecs


def test_get_data_w_bad_params(capsys, faker, sample_data_fields, new_data_file):
    """Test with invalid parameters."""
    random.seed()
    numRecs = random.randint(1,10)
    dataOut = [invalid_sample_data(faker) for i in range(numRecs)]
    dataHdrs = sample_data_fields
    dataFName = new_data_file
    tblName = '_TEST_TABLE_'

    src.utils.datastore.sqlite.save_data(dataOut, dataFName, dataHdrs['sql'], tblName, True)
    
    # Test reading from non-existant file
    with pytest.raises(OSError) as excinfo:
        dataIn = src.utils.datastore.sqlite.get_data('DOES_NOT_EXIST.sqlite', dataHdrs['sql'], tblName, None, numRecs)
    exMsg = excinfo.value.args[0]
    assert exMsg == "SQLite data file 'DOES_NOT_EXIST.sqlite' does not exist!"

    # Test invalid table name
    with pytest.raises(OSError) as excinfo:
        dataIn = src.utils.datastore.sqlite.get_data(dataFName, dataHdrs['sql'], 'INVALID_TABLE', None, numRecs)
    exMsg = excinfo.value.args[0]
    assert "Failed to retrieve data from SQLite database" in exMsg
    
    # Test invalid headers/field names
    with pytest.raises(OSError) as excinfo:
        dataIn = src.utils.datastore.sqlite.get_data(dataFName, {'foo':'bar'}, tblName, None, numRecs)
    exMsg = excinfo.value.args[0]
    assert "Failed to retrieve data from SQLite database" in exMsg
