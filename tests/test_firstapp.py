#!/usr/bin/env python

"""Tests for `firstapp` package."""

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


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Usage: ' in result.output
    assert '[OPTIONS] COMMAND [ARGS]...' in result.output
    
    result_flg_help = runner.invoke(cli.main, ['--help'])
    assert result_flg_help.exit_code == 0
    assert '--help' in result_flg_help.output
    
    result_cmd_debug = runner.invoke(cli.main, ['debug'])
    assert result_cmd_debug.exit_code == 0
    assert 'Testing 1-2-3' in result_cmd_debug.output
    
    result_cmd_debug = runner.invoke(cli.main, ['debug --msg ">> Pytest <<"'])
    assert result_cmd_debug.exit_code == 0
    assert '>> Pytest <<' in result_cmd_debug.output

    

    #result_cmd_config = runner.invoke(cli.main, ['--config'])
    #assert result_cmd_help.exit_code == 0
    #assert '  --help         Show this message and exit.' in result_cmd_help.output

    #result_cmd_help = runner.invoke(cli.main, ['--help'])
    #assert result_cmd_help.exit_code == 0
    #assert '  --help         Show this message and exit.' in result_cmd_help.output
