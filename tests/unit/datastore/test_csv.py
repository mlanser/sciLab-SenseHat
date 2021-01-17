import os
import csv
import uuid
import random

import pytest
from inspect import currentframe

from tests.unit.helpers import pp
from tests.unit.datastore.helpers import valid_sample_data, invalid_sample_data

import src.utils.datastore.csv


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_HDR_FLDS_RAW_ = {'strFld1': str, 'strFld2': str, 'strFld3': str, 'floatFld': float, 'intFld': int}
_HDR_FLDS_CSV_ = {'strFld1': None, 'strFld2': None, 'strFld3': None, 'floatFld': None, 'intFld': None}

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


@pytest.fixture()
def even_row_data_file(tmpdir_factory):
    """Create CSV data file with even rows (i.e. every row has same number of fields)."""
    testDir = tmpdir_factory.mktemp('test')
    dataFile = testDir.join('even_row.csv')
    
    dataFile.write(_EVEN_DATA_4xROWS_5xFLDS)
    
    return str(dataFile)

  
@pytest.fixture()
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


def test__process_row(sample_data_fields, valid_data_row, truncated_data_row):
    """Happy path! Process data rows."""
    hdrs = sample_data_fields
    data = valid_data_row
    row = src.utils.datastore.csv._process_row(data, hdrs['raw'])
    assert len(row) == 5

    data = truncated_data_row
    row = src.utils.datastore.csv._process_row(data, hdrs['raw'])
    assert len(row) == 4


def test__process_row_w_bad_params(sample_data_fields,valid_data_row):
    """Test with invalid parameters."""
    hdrs = sample_data_fields
    data = valid_data_row
    
    with pytest.raises(AttributeError) as excinfo:
        row = src.utils.datastore.csv._process_row('--INVALID--', hdrs['raw'])
    exMsg = excinfo.value.args[0]
    assert exMsg == "'str' object has no attribute 'items'"

    with pytest.raises(TypeError) as excinfo:
        row = src.utils.datastore.csv._process_row(data, None)
    exMsg = excinfo.value.args[0]
    assert exMsg == "argument of type 'NoneType' is not iterable"

    with pytest.raises(AttributeError) as excinfo:
        row = src.utils.datastore.csv._process_row(None, None)
    exMsg = excinfo.value.args[0]
    assert exMsg == "'NoneType' object has no attribute 'items'"

    
def test_save_data(faker, sample_data_fields, new_data_file):
    """Happy path! Save data to file."""
    random.seed()
    dataOut = [valid_sample_data(faker) for i in range(random.randint(1,10))]
    hdrs = sample_data_fields['csv']
    dataFName = new_data_file

    src.utils.datastore.csv.save_data(dataOut, dataFName, hdrs, True)

    dataIn = []
    hdrs = sample_data_fields['raw']
    with open(dataFName, 'r', newline='') as dataFile:
        dataReader = csv.DictReader(dataFile, hdrs.keys())

        for i, row in enumerate(dataReader, 0):
            if i < 1:       # Skip first line which holds header names
                continue;
            else:    
                dataIn.append(src.utils.datastore.csv._process_row(row, hdrs))

    assert len(dataIn) == len(dataOut)

    
def test_save_data_w_bad_params(faker, sample_data_fields, empty_data_file, new_data_file):
    """Test with invalid parameters."""
    random.seed()
    hdrs = sample_data_fields['csv']
    dataOut = [invalid_sample_data(faker) for i in range(random.randint(1,10))]
    dataFName = new_data_file
    existFName = empty_data_file

    # Test writing to non-existant file with incorrect 'force' flag
    with pytest.raises(TypeError) as excinfo:
        src.utils.datastore.csv.save_data(dataOut, None, hdrs, False)
    exMsg = excinfo.value.args[0]
    assert 'path should be string, bytes, os.PathLike or integer' in exMsg

    # Test writing to non-existant file with incorrect 'force' flag
    with pytest.raises(OSError) as excinfo:
        src.utils.datastore.csv.save_data(dataOut, dataFName, hdrs, False)
    exMsg = excinfo.value.args[0]
    assert 'does not exist!' in exMsg

    # Test bad data headers   
    with pytest.raises(AttributeError) as excinfo:
        src.utils.datastore.csv.save_data(dataOut, dataFName, None, True)
    exMsg = excinfo.value.args[0]
    assert exMsg == "'NoneType' object has no attribute 'keys'"
    
    
def test_get_data(faker, sample_data_fields, new_data_file, valid_data_row):
    """Happy path! Save data to file."""
    dataFName = new_data_file
    dataOut = valid_data_row

    with open(dataFName, 'a+', newline='') as dataFile:
        dataWriter = csv.DictWriter(dataFile, _HDR_FLDS_CSV_.keys(), extrasaction='ignore')
        dataWriter.writeheader()
        dataWriter.writerow(dataOut)
    
    dataIn = src.utils.datastore.csv.get_data(dataFName, _HDR_FLDS_RAW_, 1, True)

    assert len(dataIn[0]) == len(dataOut)
    assert dataIn[0] == dataOut
    
    
def test_get_data_w_bad_params(faker, sample_data_fields, new_data_file, valid_data_row):
    """Test with invalid parameters."""
    dataFName = new_data_file
    dataOut = valid_data_row

    # Test reading from non-existant file
    with pytest.raises(OSError) as excinfo:
        dataIn = src.utils.datastore.csv.get_data('_DOES_NOT_EXIST_.CSV.', _HDR_FLDS_RAW_, 1, True)
    exMsg = excinfo.value.args[0]
    assert exMsg == "Data file '_DOES_NOT_EXIST_.CSV.' does not exist!"
    
    # Test reading zero lines (will read at least 1 line) ...
    with open(dataFName, 'a+', newline='') as dataFile:
        dataWriter = csv.DictWriter(dataFile, _HDR_FLDS_CSV_.keys(), extrasaction='ignore')
        dataWriter.writeheader()
        dataWriter.writerow(dataOut)

    dataIn = src.utils.datastore.csv.get_data(dataFName, _HDR_FLDS_RAW_, 0, True)
    assert len(dataIn[0]) == len(dataOut)
    
    # ... and try to read too many lines (will read 1 line in this case)
    dataIn = src.utils.datastore.csv.get_data(dataFName, _HDR_FLDS_RAW_, 999, True)
    assert len(dataIn[0]) == len(dataOut)
    