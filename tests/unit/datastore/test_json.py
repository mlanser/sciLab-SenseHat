import os
import json
import uuid
import random

import pytest
from inspect import currentframe

from tests.unit.helpers import pp
from tests.unit.datastore.helpers import valid_sample_data, invalid_sample_data

import src.utils.datastore.json


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
_HDR_FLDS_RAW_ = {'strFld1': str, 'strFld2': str, 'strFld3': str, 'floatFld': float, 'intFld': int}
_HDR_FLDS_JSON_ = {'strFld1': None, 'strFld2': None, 'strFld3': None, 'floatFld': None, 'intFld': None}

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
def even_row_data_file(tmpdir_factory):
    """Create JSON data file with even rows (i.e. every row has same number of fields)."""
    testDir = tmpdir_factory.mktemp('test')
    dataFile = testDir.join('even_row.json')
    
    with open(dataFile, "w") as dbFile:
        json.dump(_EVEN_DATA_4xROWS_5xFLDS, dbFile)
        
    return str(dataFile)

  
@pytest.fixture()
def uneven_row_data_file(tmpdir_factory):
    """Create JSON data file with uneven rows (i.e. row have different number of fields)."""
    testDir = tmpdir_factory.mktemp('test')
    dataFile = testDir.join('uneven_row.json')
    
    with open(dataFile, "w") as dbFile:
        json.dump(_UNEVEN_DATA_5xROWS_NxFLDS, dbFile)
        
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
    dataFile = testDir.join(uuid.uuid4().hex + '.json')
    
    dataFile.write('')
    
    return str(dataFile)


@pytest.fixture()
def new_data_file(tmpdir_factory):
    """Only create the filename, but not the actual file."""
    testDir = tmpdir_factory.mktemp('test')
    dataFile = testDir.join(uuid.uuid4().hex + '.json')
    
    return str(dataFile)

    
# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
def test__process_data(faker, sample_data_fields, truncated_data_row):
    """Happy path! Process data rows."""
    random.seed()
    hdrs = sample_data_fields
    dataIn = [valid_sample_data(faker) for i in range(random.randint(1,10))]
    dataOut = src.utils.datastore.json._process_data(dataIn, hdrs['raw'])
    assert len(dataOut[0]) == 5

    dataIn = [truncated_data_row]
    dataOut = src.utils.datastore.json._process_data(dataIn, hdrs['raw'])
    assert len(dataOut[0]) == 4


def test__process_data_w_bad_params(sample_data_fields, valid_data_row):
    """Test with invalid parameters."""
    hdrs = sample_data_fields
    dataIn = [valid_data_row]
    
    with pytest.raises(AttributeError) as excinfo:
        dataOut = src.utils.datastore.json._process_data('--INVALID--', hdrs['raw'])
    exMsg = excinfo.value.args[0]
    assert exMsg == "'str' object has no attribute 'keys'"

    with pytest.raises(TypeError) as excinfo:
        dataOut = src.utils.datastore.json._process_data(dataIn, None)
    exMsg = excinfo.value.args[0]
    assert exMsg == "'NoneType' object is not iterable"

    with pytest.raises(AttributeError) as excinfo:
        dataOut = src.utils.datastore.json._process_data([None], None)
    exMsg = excinfo.value.args[0]
    assert exMsg == "'NoneType' object has no attribute 'keys'"


def test__read_json(even_row_data_file, uneven_row_data_file):
    """Happy path! Read JSON file."""
    dataFName = even_row_data_file
    data = src.utils.datastore.json._read_json(dataFName)
    assert len(data) == 4

    dataFName = uneven_row_data_file
    data = src.utils.datastore.json._read_json(dataFName)
    assert len(data) == 4

    
def test__read_json_w_bad_params(binary_data_file, empty_data_file, new_data_file):
    """Test with invalid parameters."""
    with pytest.raises(FileNotFoundError) as excinfo:
        data = src.utils.datastore.json._read_json('--INVALID--')
    exMsg = excinfo.value.args[0]
    assert exMsg == 2
    
    with pytest.raises(TypeError) as excinfo:
        data = src.utils.datastore.json._read_json(None)
    exMsg = excinfo.value.args[0]
    assert exMsg == "expected str, bytes or os.PathLike object, not NoneType"
    
    dataFName = new_data_file
    with pytest.raises(FileNotFoundError) as excinfo:
        data = src.utils.datastore.json._read_json(dataFName)
    exMsg = excinfo.value.args[0]
    assert exMsg == 2

    dataFName = empty_data_file
    with pytest.raises(OSError) as excinfo:
        data = src.utils.datastore.json._read_json(dataFName)
    exMsg = excinfo.value.args[0]
    assert "Failed to read data from" in exMsg

    dataFName = binary_data_file
    with pytest.raises(OSError) as excinfo:
        data = src.utils.datastore.json._read_json(dataFName)
    exMsg = excinfo.value.args[0]
    assert "Failed to read data from" in exMsg

    
def test__write_json(new_data_file):
    """Happy path! Write JSON file."""
    dataFName = new_data_file
    src.utils.datastore.json._write_json(dataFName, _EVEN_DATA_4xROWS_5xFLDS)
    data = src.utils.datastore.json._read_json(dataFName)
    assert len(data) == 4

    dataFName = new_data_file
    src.utils.datastore.json._write_json(dataFName, _UNEVEN_DATA_5xROWS_NxFLDS)
    data = src.utils.datastore.json._read_json(dataFName)
    assert len(data) == 4

    
def test__write_json_w_bad_params(new_data_file):
    """Test with invalid parameters."""
    with pytest.raises(TypeError) as excinfo:
        src.utils.datastore.json._write_json(None, _EVEN_DATA_4xROWS_5xFLDS)
    exMsg = excinfo.value.args[0]
    assert exMsg == "expected str, bytes or os.PathLike object, not NoneType"
    
    
def test_save_data(capsys, faker, sample_data_fields, new_data_file):
    """Happy path! Save data to JSON file."""
    random.seed()
    hdrs = sample_data_fields
    dataOut = [valid_sample_data(faker) for i in range(random.randint(1,10))]
    dataFName = new_data_file

    src.utils.datastore.json.save_data(dataOut, dataFName, hdrs['raw'], True)

    with open(dataFName, 'r') as dataFile:
        dataIn = json.load(dataFile)

    assert len(dataIn) == len(dataOut)
    assert dataIn == dataOut


def test_save_data_w_bad_params(capsys, faker, sample_data_fields, empty_data_file, new_data_file):
    """Test with invalid parameters."""
    random.seed()
    hdrs = sample_data_fields
    dataOut = [invalid_sample_data(faker) for i in range(random.randint(1,10))]
    dataFName = new_data_file
    existFName = empty_data_file

    # Test writing to 'None' as filename
    with pytest.raises(TypeError) as excinfo:
        src.utils.datastore.json.save_data(dataOut, None, hdrs['json'])
    exMsg = excinfo.value.args[0]
    assert 'path should be string, bytes, os.PathLike or integer' in exMsg
    
    # Test writing to non-existant file with incorrect 'force' flag
    with pytest.raises(OSError) as excinfo:
        src.utils.datastore.json.save_data(dataOut, '--INVALID--', hdrs['raw'], False)
    exMsg = excinfo.value.args[0]
    assert exMsg == "JSON data file '--INVALID--' does not exist!"

    # Test bad data headers   
    with pytest.raises(TypeError) as excinfo:
        src.utils.datastore.json.save_data(dataOut, dataFName, None, True)
    exMsg = excinfo.value.args[0]
    assert exMsg == "'NoneType' object is not iterable"


def test_get_data(capsys, faker, sample_data_fields, new_data_file):
    """Happy path! Get data from JSON file."""
    random.seed()
    hdrs = sample_data_fields
    numRecs = random.randint(1,10)
    dataOut = [valid_sample_data(faker) for i in range(numRecs)]
    dataFName = new_data_file
    
    with open(dataFName, 'w') as dataFile:
        json.dump(dataOut, dataFile)

    dataIn = src.utils.datastore.json.get_data(dataFName, hdrs['raw'], numRecs, True)
    assert len(dataIn) == len(dataOut)
    assert len(dataIn[0]) == len(dataOut[0])
    assert dataIn == dataOut

    dataIn = src.utils.datastore.json.get_data(dataFName, hdrs['raw'], 0, True)
    assert len(dataIn) == 0

    dataIn = src.utils.datastore.json.get_data(dataFName, hdrs['raw'], 999, True)
    assert len(dataIn) == numRecs
    assert len(dataIn) == len(dataOut)
    assert len(dataIn[0]) == len(dataOut[0])

    
def test_get_data_w_bad_params(capsys, faker, sample_data_fields, new_data_file, valid_data_row):
    """Test with invalid parameters."""
    random.seed()
    numRecs = random.randint(1,10)
    dataOut = [invalid_sample_data(faker) for i in range(numRecs)]
    hdrs = sample_data_fields
    dataFName = new_data_file

    # Test reading from non-existant file
    dataIn = src.utils.datastore.json.get_data('_DOES_NOT_EXIST_.JSON.', _HDR_FLDS_RAW_, 1, True)
    assert dataIn == []

    # Test invalid headers/field names
    dataOut = [valid_data_row]
    with open(dataFName, 'w') as dataFile:
        json.dump(dataOut, dataFile)

    with pytest.raises(TypeError) as excinfo:
        dataIn = src.utils.datastore.json.get_data(dataFName, None, 1, True)
    exMsg = excinfo.value.args[0]
    assert exMsg == "'NoneType' object is not iterable"
