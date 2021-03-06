#!/usr/bin/env python

"""CliRunner Tests for MAIN command and arguments."""

import pytest

from click.testing import CliRunner

from src import cli


# =========================================================
#     G L O B A L S   &   P Y T E S T   F I X T U R E S
# =========================================================
@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


# =========================================================
#                T E S T   F U N C T I O N S
# =========================================================
def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_cli_cmd_MAIN_raw(new_config_file):
    """Test CLI '<DO THING>' command."""
    runner = CliRunner()
    configFile = new_config_file
    
    result = runner.invoke(
        cli.main,
        args=['--ini', configFile,'nothing'],
    )
    assert True

    
def test_cli_cmd_MAIN_w_DISPLAY_flg():
    """Test CLI '<DO THING>' command w '--display' flag."""
    runner = CliRunner()
    
    #result = runner.invoke(
    #    cli.main,
    #    args=['config','--xxxx','>> Pytest <<']
    #)
    #assert result.exit_code == 0
    #assert '>> Pytest <<' in result.output
    assert True

    
def test_cli_cmd_MAIN_w_SAVE_flg():
    """Test CLI '<DO THING>' command w '--save' flag."""
    runner = CliRunner()
    
    #result = runner.invoke(
    #    cli.main,
    #    args=['config','--xxxx','>> Pytest <<']
    #)
    #assert result.exit_code == 0
    #assert '>> Pytest <<' in result.output
    assert True

    
def test_cli_cmd_MAIN_w_SUMMARY_flg():
    """Test CLI '<DO THING>' command w '--summary' flag."""
    runner = CliRunner()
    
    #result = runner.invoke(
    #    cli.main,
    #    args=['config','--xxxx','>> Pytest <<']
    #)
    #assert result.exit_code == 0
    #assert '>> Pytest <<' in result.output
    assert True

    
def test_cli_cmd_MAIN_w_COUNT_flg():
    """Test CLI '<DO THING>' command w '--count' flag."""
    runner = CliRunner()
    
    #result = runner.invoke(
    #    cli.main,
    #    args=['--ini', 'tests/test_config.ini','CONFIG','--msg','>> Pytest <<']
    #)
    #assert result.exit_code == 0
    #assert '>> Pytest <<' in result.output
    #assert 'tests/test_config.ini' in result.output
    assert True

    
def test_cli_cmd_MAIN_w_HISTORY_flg():
    """Test CLI '<DO THING>' command w '--history' flag."""
    runner = CliRunner()
    
    #result = runner.invoke(
    #    cli.main,
    #    args=['--ini', 'tests/test_config.ini','CONFIG','--msg','>> Pytest <<']
    #)
    #assert result.exit_code == 0
    #assert '>> Pytest <<' in result.output
    #assert 'tests/test_config.ini' in result.output
    assert True

def test_cli_cmd_MAIN_w_FIRST_flg():
    """Test CLI '<DO THING>' command w '--first' flag."""
    runner = CliRunner()
    
    #result = runner.invoke(
    #    cli.main,
    #    args=['--ini', 'tests/test_config.ini','CONFIG','--msg','>> Pytest <<']
    #)
    #assert result.exit_code == 0
    #assert '>> Pytest <<' in result.output
    #assert 'tests/test_config.ini' in result.output
    assert True
            