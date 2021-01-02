#!/usr/bin/env python

"""CliRunner Tests for DEBUG command and arguments."""

import pytest

from click.testing import CliRunner

from firstapp import cli


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


def test_cli_cmd_DEBUG_raw():
    """Test CLI 'DEBUG' command."""
    runner = CliRunner()
    
    result = runner.invoke(
        cli.main,
        args=['debug']
    )
    assert result.exit_code == 0
    assert 'Testing 1-2-3' in result.output

    
def test_cli_cmd_DEBUG_w_MSG_flg():
    """Test CLI 'DEBUG' command w '--msg' flag."""
    runner = CliRunner()
    
    result = runner.invoke(
        cli.main,
        args=['debug','--msg','>> Pytest <<']
    )
    assert result.exit_code == 0
    assert '>> Pytest <<' in result.output

    
def test_cli_cmd_DEBUG_w_MSG_INI_flgs():
    """Test CLI 'DEBUG' command w '--msg' and '--ini' flags."""
    runner = CliRunner()
    
    result = runner.invoke(
        cli.main,
        args=['--ini', 'tests/test_config.ini','debug','--msg','>> Pytest <<']
    )
    assert result.exit_code == 0
    assert '>> Pytest <<' in result.output
    assert 'tests/test_config.ini' in result.output
