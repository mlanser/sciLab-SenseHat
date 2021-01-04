import os
import re
from configparser import ConfigParser, ExtendedInterpolation, Error
from sys import modules as sysmods

import pprint

import pytest
import src.utils.settings

_HDR_DATA_ = '[Settings: data]'
_HDR_MAIN_ = '[Settings: main]'
_CONFIG_DATA_ = """\
[foo]
bar = 1
fizz = buzz
sort
"""

@pytest.fixture()
def create_valid_settings(valid_config_string):
    config = configparser.ConfigParser()
    config.read_string(valid_config_string)
    return config

  
@pytest.fixture()
def create_invalid_settings(invalid_config_string):
    config = configparser.ConfigParser()
    config.read_string(invalid_config_string)
    return config

  
def test_is_valid_settings():
    assert True

    
def test_read_settings(valid_config_ini):
    configFName = valid_config_ini
    config = src.utils.settings.read_settings({'configFName':configFName})
    
    assert config.has_section('data')
    assert config.has_option('data', 'sort')
    assert 'first' == config.get('data', 'sort')
    
    assert not(config.has_section('foo'))
    assert not(config.has_option('foo', 'bar'))

    
def test_read_settings_invalid_file_name():
    configFName = "--INVALID--"
    
    with pytest.raises(OSError) as excinfo:
        src.utils.settings.read_settings({'configFName':configFName})
    
    exMsg = excinfo.value.args[0]
    assert exMsg == "Config file '--INVALID--' does NOT exist or cannot be accessed!"    

    
def test_read_settings_invalid_file_format(invalid_config_ini_fomat):
    configFName = invalid_config_ini_fomat
    
    with pytest.raises(ValueError) as excinfo:
        src.utils.settings.read_settings({'configFName':configFName})
    
    exMsg = excinfo.value.args[0]
    assert "Invalid configuration settings!" in exMsg

    
def test_save_settings():
    assert True

    
def test_show_settings_sctn_DATA_no_verify(capsys, valid_config_ini):
    configFName = valid_config_ini
    ctxGlobals = {'configFName':configFName}

    src.utils.settings.show_settings(ctxGlobals, src.utils.settings._SCTN_DATA_)
    out, err = capsys.readouterr()
    
    assert _HDR_DATA_ in out
    assert 'Default Sort:       first' in out

    
def test_show_settings_sctn_MAIN_no_verify(capsys, valid_config_ini):
    configFName = valid_config_ini
    ctxGlobals = {'configFName':configFName}

    src.utils.settings.show_settings(ctxGlobals, src.utils.settings._SCTN_MAIN_)
    out, err = capsys.readouterr()
    
    assert _HDR_MAIN_ in out
    assert 'Test Run Count:   1' in out

    
def test_show_settings_sctn_ALL_no_verify(capsys, valid_config_ini):
    configFName = valid_config_ini
    ctxGlobals = {'configFName':configFName}

    src.utils.settings.show_settings(ctxGlobals, src.utils.settings._SCTN_ALL_)
    out, err = capsys.readouterr()
    
    assert _HDR_DATA_ in out
    assert 'Default Sort:       first' in out
    assert _HDR_MAIN_ in out
    assert 'Test Run Count:   1' in out

    
def test_show_settings_invalid_sctn(capsys, valid_config_ini):
    configFName = valid_config_ini
    ctxGlobals = {'configFName':configFName}

    with pytest.raises(ValueError) as excinfo:
        src.utils.settings.show_settings(ctxGlobals, '--INVALID--')
    
    exMsg = excinfo.value.args[0]
    assert exMsg == "Invalid section '--INVALID--'"    

    
def test_show_settings_sctn_MAIN_w_verify(capsys, valid_config_ini, invalid_config_ini):
    configFName = valid_config_ini
    ctxGlobals = {'configFName':configFName}

    src.utils.settings.show_settings(ctxGlobals, src.utils.settings._SCTN_MAIN_, True)
    out, err = capsys.readouterr()
    
    assert _HDR_DATA_ in out
    assert 'Default Sort:       first' in out
    assert _HDR_MAIN_ in out
    assert 'Test Run Count:   1' in out

    configFName = invalid_config_ini
    ctxGlobals = {'configFName':configFName}

    with capsys.disabled:
      src.utils.settings.show_settings(ctxGlobals, src.utils.settings._SCTN_MAIN_, True)
    #out, err = capsys.readouterr()
    
    #assert _HDR_DATA_ in out
    #'- Invalid setting! -'
    
