import os
import csv
import uuid
import random

import pprint
import pytest
from inspect import currentframe, getframeinfo

import src.utils.datastore.csv


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_HDR_FLDS_RAW_ = {'strFld1': str, 'strFld2': str, 'strFld3': str, 'floatFld': float, 'intFld': int}
_HDR_FLDS_CSV_ = {'strFld1': None, 'strFld2': None, 'strFld3': None, 'floatFld': None, 'intFld': None}
_VALID_DATA_ROW_ = {'strFld1': 'val1', 'strFld2': 'val2', 'strFld3': 'val3', 'floatFld': 4.0, 'intFld': 5}
_TRUNCATED_DATA_ROW_ = {'strFld1': 'val1', 'strFld2': 'val2', 'floatFld': 4.0, 'intFld': 5, 'fruit': 'banana'}
_INVALID_DATA_ROW_ = {'strFld1': 'val1', 'fruit': 'banana', 'strFld3': 'val3', 'floatFld': 'NOT FLOAT', 'intFld': 5}

_EVEN_DATA_4xROWS_5xFLDS = """\
r1Val1,r1Val2,r1Val3,1.1,10,
r2Val1,r2Val2,r2Val3,2.2,20,
r3Val1,r3Val2,r3Val3,3.3,30,
r4Val1,r4Val2,r4Val3,4.4,40,
"""

_UNEVEN_DATA_5xROWS_NxFLDS = """\
r1Val1,r1Val2,1.1,10,
r2Val1,r2Val2,r2Val3,2.2,
r3Val1,r3Val2,
r4Val1,r4Val2,r4Val3,4.4,40,r4Val6,r4Val7
r5Val1,
"""

@pytest.fixture(scope='module')
def even_row_data_file(tmpdir_factory):
    """Create CSV data file with even rows (i.e. every row has same number of fields)."""
    testDir = tmpdir_factory.mktemp('test')
    dataFile = testDir.join('even_row.csv')
    
    dataFile.write(_EVEN_DATA_4xROWS_5xFLDS)
    
    return str(dataFile)

  
@pytest.fixture(scope='module')
def uneven_row_data_file(tmpdir_factory):
    """Create CSV data file with uneven rows (i.e. row have different number of fields)."""
    testDir = tmpdir_factory.mktemp('test')
    dataFile = testDir.join('uneven_row.csv')
    
    dataFile.write(_UNEVEN_DATA_5xROWS_NxFLDS)
    
    return str(dataFile)


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
    dataFile = testDir.join(uuid.uuid4().hex + '.csv')
    
    dataFile.write('')
    
    return str(dataFile)


@pytest.fixture()
def new_data_file(tmpdir_factory):
    """Only create the filename, but not the actual file."""
    testDir = tmpdir_factory.mktemp('test')
    dataFile = testDir.join(uuid.uuid4().hex + '.csv')
    
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
def test__row_counter(even_row_data_file, uneven_row_data_file, new_data_file):
    """Happy path! Count rows in actual text files."""
    
    # Try file where each row has same number of fields
    with open(even_row_data_file, 'r', newline='') as dataFile:
        numRows = src.utils.datastore.csv._row_counter(dataFile)
    assert numRows == 3  # NOTE: we start counter at 0 (zero)
    
    # Try file where each row has diff number of fields
    with open(uneven_row_data_file, 'r', newline='') as dataFile:
        numRows = src.utils.datastore.csv._row_counter(dataFile)
    assert numRows == 4  # NOTE: we start counter at 0 (zero)


def test__row_counter_w_bad_params(binary_data_file, new_data_file, empty_data_file):
    """Test with invalid file pointers, etc."""

    # Try blank file with no rows
    with pytest.raises(UnboundLocalError) as excinfo:
        with open(empty_data_file, 'r', newline='') as dataFile:
            numRows = src.utils.datastore.csv._row_counter(dataFile)
    exMsg = excinfo.value.args[0]
    assert exMsg == "local variable 'cntr' referenced before assignment"

    # Try invalid file pointers
    with pytest.raises(AttributeError) as excinfo:
        with open(empty_data_file, 'r', newline='') as dataFile:
            numRows = src.utils.datastore.csv._row_counter('string')
    exMsg = excinfo.value.args[0]
    assert exMsg == "'str' object has no attribute 'seek'"
    
    with pytest.raises(TypeError) as excinfo:
        with open(empty_data_file, 'r', newline='') as dataFile:
            numRows = src.utils.datastore.csv._row_counter(None)
    exMsg = excinfo.value.args[0]
    assert exMsg == "'NoneType' object is not iterable"


def test__process_row(sample_data_fields):
    """Happy path! Process data rows."""
    dataHdrs = sample_data_fields
    dataRow = src.utils.datastore.csv._process_row(_VALID_DATA_ROW_, dataHdrs['raw'])
    assert len(dataRow) == 5

    dataRow = src.utils.datastore.csv._process_row(_TRUNCATED_DATA_ROW_, dataHdrs['raw'])
    assert len(dataRow) == 4


def test__process_row_w_bad_params(sample_data_fields):
    """Test with invalid parameters."""
    dataHdrs = sample_data_fields
    with pytest.raises(AttributeError) as excinfo:
        dataRow = src.utils.datastore.csv._process_row('--INVALID--', dataHdrs['raw'])
    exMsg = excinfo.value.args[0]
    assert exMsg == "'str' object has no attribute 'items'"

    with pytest.raises(TypeError) as excinfo:
        dataRow = src.utils.datastore.csv._process_row(_VALID_DATA_ROW_, None)
    exMsg = excinfo.value.args[0]
    assert exMsg == "argument of type 'NoneType' is not iterable"

    with pytest.raises(AttributeError) as excinfo:
        dataRow = src.utils.datastore.csv._process_row(None, None)
    exMsg = excinfo.value.args[0]
    assert exMsg == "'NoneType' object has no attribute 'items'"

    
def test_save_data(faker, sample_data_fields, new_data_file):
    """Happy path! Save data to file."""
    random.seed()
    dataOut = [valid_sample_data(faker) for i in range(random.randint(1,10))]
    dataHdrs = sample_data_fields['csv']
    dataFName = new_data_file

    src.utils.datastore.csv.save_data(dataOut, dataFName, dataHdrs, True)

    dataIn = []
    dataHdrs = sample_data_fields['raw']
    with open(dataFName, 'r', newline='') as dataFile:
        dataReader = csv.DictReader(dataFile, dataHdrs.keys())

        for i, row in enumerate(dataReader, 0):
            if i < 1:       # Skip first line which holds header names
                continue;
            else:    
                dataIn.append(src.utils.datastore.csv._process_row(row, dataHdrs))

    assert len(dataIn) == len(dataOut)

    
def test_save_data_w_bad_params(faker, sample_data_fields, empty_data_file, new_data_file):
    """Test with invalid parameters."""
    random.seed()
    dataOut = [invalid_sample_data(faker) for i in range(random.randint(1,10))]
    dataHdrs = sample_data_fields['csv']
    dataFName = new_data_file
    existFName = empty_data_file

    # Test writing to non-existant file with incorrect 'force' flag
    with pytest.raises(TypeError) as excinfo:
        src.utils.datastore.csv.save_data(dataOut, None, dataHdrs, False)
    exMsg = excinfo.value.args[0]
    assert 'path should be string, bytes, os.PathLike or integer' in exMsg

    # Test writing to non-existant file with incorrect 'force' flag
    with pytest.raises(OSError) as excinfo:
        src.utils.datastore.csv.save_data(dataOut, dataFName, dataHdrs, False)
    exMsg = excinfo.value.args[0]
    assert 'does not exist!' in exMsg

    # Test bad data headers   
    with pytest.raises(AttributeError) as excinfo:
        src.utils.datastore.csv.save_data(dataOut, dataFName, None, True)
    exMsg = excinfo.value.args[0]
    assert exMsg == "'NoneType' object has no attribute 'keys'"
    
    
def test_get_data(faker, sample_data_fields, new_data_file):
    """Happy path! Save data to file."""
    dataFName = new_data_file

    with open(dataFName, 'a+', newline='') as dataFile:
        dataWriter = csv.DictWriter(dataFile, _HDR_FLDS_CSV_.keys(), extrasaction='ignore')
        dataWriter.writeheader()
        dataWriter.writerow(_VALID_DATA_ROW_)
    
    dataIn = src.utils.datastore.csv.get_data(dataFName, _HDR_FLDS_RAW_, 1, True)

    assert len(dataIn[0]) == len(_VALID_DATA_ROW_)
    assert dataIn[0] == _VALID_DATA_ROW_
    
    
def test_get_data_w_bad_params(faker, sample_data_fields, new_data_file):
    dataFName = new_data_file

    # Test reading from non-existant file
    with pytest.raises(OSError) as excinfo:
        dataIn = src.utils.datastore.csv.get_data('_DOES_NOT_EXIST_.CSV.', _HDR_FLDS_RAW_, 1, True)
    exMsg = excinfo.value.args[0]
    assert exMsg == "Data file '_DOES_NOT_EXIST_.CSV.' does not exist!"
    
    # Test reading zero lines (will read at least 1 line) ...
    with open(dataFName, 'a+', newline='') as dataFile:
        dataWriter = csv.DictWriter(dataFile, _HDR_FLDS_CSV_.keys(), extrasaction='ignore')
        dataWriter.writeheader()
        dataWriter.writerow(_VALID_DATA_ROW_)

    dataIn = src.utils.datastore.csv.get_data(dataFName, _HDR_FLDS_RAW_, 0, True)
    assert len(dataIn[0]) == len(_VALID_DATA_ROW_)
    
    # ... and try to read too many lines (will read 1 line in this case)
    dataIn = src.utils.datastore.csv.get_data(dataFName, _HDR_FLDS_RAW_, 999, True)
    assert len(dataIn[0]) == len(_VALID_DATA_ROW_)
    