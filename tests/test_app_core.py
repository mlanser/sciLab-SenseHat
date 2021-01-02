#!/usr/bin/env python

"""CliRunner Tests for core app functions and arguments."""

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


def test_cli_core():
    """Test CLI core functions/commands."""
    runner = CliRunner()
    
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Usage: ' in result.output
    assert '[OPTIONS] COMMAND [ARGS]...' in result.output

    
def test_cli_core_flg_help():
    """Test CLI core w '--help' flag."""
    runner = CliRunner()
    
    result = runner.invoke(
        cli.main,
        args=['--help']
    )
    assert result.exit_code == 0
    assert '--help' in result.output
    
    
def test_cli_core_w_bad_arg():
    """Test CLI core w invalid flag."""
    runner = CliRunner()
    
    result = runner.invoke(
        cli.main,
        args=['--this-is-invalid']
    )
    assert result.exit_code == 2
    assert 'Error: no such option: --this-is-invalid' in result.output
    