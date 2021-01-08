import os
import csv
import uuid
import random

import pprint

import pytest

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
r1Val1,r1Val2,r1Val3,4.0,5,
r2Val1,r2Val2,r2Val3,4.0,5,
r3Val1,r3Val2,r3Val3,4.0,5,
r4Val1,r4Val2,r4Val3,4.0,5,
"""

_UNEVEN_DATA_5xROWS_NxFLDS = """\
r1Val1,r1Val2,4.0,5,
r2Val1,r2Val2,r2Val3,4.0,
r3Val1,r3Val2,
r4Val1,r4Val2,r4Val3,4.0,5,r4Val6,r4Val7
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
def empty_data_file(tmpdir_factory):
    testDir = tmpdir_factory.mktemp('test')
    dataFile = testDir.join(uuid.uuid4().hex + '.csv')
    
    dataFile.write('')
    
    return str(dataFile)


@pytest.fixture()
def new_data_file(tmpdir_factory):
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


def test__row_counter_w_bad_info(new_data_file, empty_data_file):
    """Test with invalid file pointers, etc."""

    # Try blank file with no rows
    with pytest.raises(UnboundLocalError) as excinfo:
        with open(empty_data_file, 'r', newline='') as dataFile:
            numRows = src.utils.datastore.csv._row_counter(dataFile)
    exMsg = excinfo.value.args[0]
    assert exMsg == "local variable 'cntr' referenced before assignment"

    #numRows = src.utils.datastore.csv._row_counter(None)
    #'NoneType' object is not iterable

    #numRows = src.utils.datastore.csv._row_counter([None])
    #'list' object has no attribute 'seek'

    #with open(even_row_data_file, 'rb') as dataFile:
    #    numRows = src.utils.datastore.csv._row_counter(dataFile)

    # @TO-DO: test binary file, invalid fp(?), "None", etc. 
    #with pytest.raises(ValueError) as excinfo:
    #    dataRow = src.utils.datastore.csv._process_row(_INVALID_DATA_ROW_, dataHdrs['raw'])

    #exMsg = excinfo.value.args[0]
    #assert exMsg == "could not convert string to float: 'NOT FLOAT'"


def test__process_row(capsys, sample_data_fields):
    dataHdrs = sample_data_fields
    dataRow = src.utils.datastore.csv._process_row(_VALID_DATA_ROW_, dataHdrs['raw'])
    assert len(dataRow) == 5

    dataRow = src.utils.datastore.csv._process_row(_TRUNCATED_DATA_ROW_, dataHdrs['raw'])
    assert len(dataRow) == 4

    with pytest.raises(ValueError) as excinfo:
        dataRow = src.utils.datastore.csv._process_row(_INVALID_DATA_ROW_, dataHdrs['raw'])

    exMsg = excinfo.value.args[0]
    assert exMsg == "could not convert string to float: 'NOT FLOAT'"


def test_save_data(capsys, sample_data_fields, valid_sample_data, new_data_file):
    random.seed()
    dataOut = [valid_sample_data for i in range(random.randint(1,10))]
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

    
def test_get_data(capsys, sample_data_fields, new_data_file):
    dataFName = new_data_file

    with open(dataFName, 'a+', newline='') as dataFile:
        dataWriter = csv.DictWriter(dataFile, _HDR_FLDS_CSV_.keys(), extrasaction='ignore')
        dataWriter.writeheader()
        dataWriter.writerow(_VALID_DATA_ROW_)
    
    dataIn = src.utils.datastore.csv.get_data(dataFName, _HDR_FLDS_RAW_, 1, True)

    assert len(dataIn[0]) == len(_VALID_DATA_ROW_)
    #with capsys.disabled():
    #    _PP_ = pprint.PrettyPrinter(indent=4)
    #    print('\n')
    #    _PP_.pprint(_VALID_DATA_ROW_)
    #    _PP_.pprint(dataIn)
    #    #_PP_.pprint(dataFile)
        