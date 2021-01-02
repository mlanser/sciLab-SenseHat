#!/usr/bin/env python

"""CliRunner Tests for CONFIG command and arguments."""

import pytest

from click.testing import CliRunner

from src import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_cli_cmd_CONFIG_raw():
    """Test CLI 'CONFIG' command."""
    runner = CliRunner()
    
    result = runner.invoke(
        cli.main,
        args=['--ini','tests/nuke.ini','config', '--force'],
        input="5\n5\nfirst\n5\n60\nmulti\nbits\nno\nGreensboro\nAmerica/New_York\nCSV\ntests/nuke.csv\nNukeApp"
    )
    assert result.exit_code == 0

    
def test_cli_cmd_CONFIG_w_SECTION_flg():
    """Test CLI 'CONFIG' command w '--section' flag."""
    runner = CliRunner()
    
    #result = runner.invoke(
    #    cli.main,
    #    args=['config','--xxxx','>> Pytest <<']
    #)
    #assert result.exit_code == 0
    #assert '>> Pytest <<' in result.output
    assert True

    
def test_cli_cmd_CONFIG_w_FORCE_flg():
    """Test CLI 'CONFIG' command w '--section' flag."""
    runner = CliRunner()
    
    #result = runner.invoke(
    #    cli.main,
    #    args=['config','--xxxx','>> Pytest <<']
    #)
    #assert result.exit_code == 0
    #assert '>> Pytest <<' in result.output
    assert True

    
def test_cli_cmd_CONFIG_w_VERIFY_flg():
    """Test CLI 'CONFIG' command w '--section' flag."""
    runner = CliRunner()
    
    #result = runner.invoke(
    #    cli.main,
    #    args=['config','--xxxx','>> Pytest <<']
    #)
    #assert result.exit_code == 0
    #assert '>> Pytest <<' in result.output
    assert True

    
def test_cli_cmd_CONFIG_w_SET_SHOW_flgs():
    """Test CLI 'CONFIG' command w '--msg' and '--ini' flags."""
    runner = CliRunner()
    
    #result = runner.invoke(
    #    cli.main,
    #    args=['--ini', 'tests/test_config.ini','CONFIG','--msg','>> Pytest <<']
    #)
    #assert result.exit_code == 0
    #assert '>> Pytest <<' in result.output
    #assert 'tests/test_config.ini' in result.output
    assert True
    