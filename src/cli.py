import os
import re
import sys
import time

import click
import pytz
import requests
from dateutil import parser

from .utils.debug.debug import debug_msg
from .utils.settings import read_settings, save_settings, show_settings, isvalid_settings
# from .sensors.sensehat import init_sensor as init_SenseHat
# from .sensors.speedtest import run_speedtest, save_speed_data, get_speed_data

_APP_NAME_: str = 'pired'
_APP_CONFIG_: str = 'config.ini'
_APP_MIN_RUNS_: int = 1
_APP_MAX_RUNS_: int = 100
_APP_HISTORY_: int = 1000
_APP_SLEEP_: int = 60
_APP_BITS_: str = 'bits'

_DB_NAME_: str = 'scilab'

_SENSOR_WEATHER_: str = 'OpenWeather'
_SENSOR_SENSEHAT_: str = 'SenseHat'
_SENSOR_SPEED_: str = 'SpeedTest'


# =========================================================
#                H E L P E R   C L A S S E S
# =========================================================
class ApiKey(click.ParamType):
    name = 'api-key'

    def convert(self, value, param, ctx):
        found = re.match(r'[0-9a-f]{32}', value)

        if not found:
            self.fail(
                f'{value} is not a 32-character hexadecimal string',
                param,
                ctx,
            )

        return value


# =========================================================
#              H E L P E R   F U N C T I O N S
# =========================================================
def current_weather(location, api_key='OWM_API_KEY'):
    """-- DUMMY FUNCTION --

    Args:
        location:  blah
        api_key:   blah
    """
    url = 'https://api.openweathermap.org/data/2.5/weather'

    query_params = {
        'q': location,
        'appid': api_key,
    }

    response = requests.get(url, params=query_params)

    return response.json()['weather'][0]['description']


def _pad_list(inList, maxLen, defaultVal):
    return inList[:maxLen] + [defaultVal for _ in range(maxLen - len(inList))]


def _data_formatter(rowData, rowNum=0, isRaw=False, rateUnit=_APP_BITS_):
    def _date_maker(timestamp, timezone, fmtStr):
        dateOrig = parser.isoparse(timestamp)
        dateFinal = dateOrig if timezone is None else dateOrig.astimezone(pytz.timezone(timezone))
        return dateFinal.strftime(fmtStr)

    def _parse_timestamp(data, tz, fmtStr, defaultVal):
        return defaultVal if 'timestamp' not in data else _date_maker(data['timestamp'], tz, fmtStr)

    def _parse_ping(data, defaultVal):
        return defaultVal if 'ping' not in data else float(data['ping'])

    def _parse_speed(data, fldName, divisor, defaultVal):
        return defaultVal if fldName not in data else float(data[fldName] / divisor)

    na = '- n/a -'
    dateTimeFmtStr = '%m/%d/%y %H:%M'
    out = (str(rowNum),) if rowNum > 0 else tuple()

    # Mbit/s or MB/s
    rateUnitDivisor = 1000000 if rateUnit.lower() != 'bytes' else 8000000

    if isRaw:
        return out + (
            _parse_timestamp(rowData, None, dateTimeFmtStr, na),
            _parse_timestamp(
                rowData,
                None if 'locationTZ' not in rowData else rowData['locationTZ'],
                dateTimeFmtStr,
                na
            ),
            _parse_ping(rowData, na),
            _parse_speed(rowData, 'download', rateUnitDivisor, na),
            _parse_speed(rowData, 'upload', rateUnitDivisor, na)
        )
    else:
        return out + tuple(_pad_list(rowData, 5, na))


def show_speed_data_summary(data, isRaw=False, rateUnit=_APP_BITS_):
    """Format and display summary SpeedTest data.

    Args:
        data:     Individual data row/record as list.
        isRaw:    If TRUE, data is is 'raw' format.
        rateUnit: MB/s if 'bytes', else Mbit/s
    """

    # Mbit/s or MB/s
    rateUnitLabel = 'Mbit/s' if rateUnit.lower() != 'bytes' else 'MB/s'

    template = "DATE:    {} (UTC)\n         {} (local)\n\n"
    if isRaw:
        template += "PING: {:8.3f} ms\nDOWN: {:8.2f} " + rateUnitLabel + "\nUP:   {:8.2f} " + rateUnitLabel
    else:
        template += "PING: {:8s} ms\nDOWN: {:8s} " + rateUnitLabel + "\nUP:   {:8s} " + rateUnitLabel

    click.echo(template.format(*_data_formatter(data, 0, isRaw, rateUnit)))
    click.echo()


def show_speed_data_details(data, isRaw=False, rateUnit=_APP_BITS_):
    """Format and display detailed SpeedTest data.

    Args:
        data:     Individual data row/record as list.
        isRaw:    If TRUE, data is is 'raw' format.
        rateUnit: MB/s if 'bytes', else Mbit/s
    """

    # Use Mbit/s or MB/s
    # rateUnitLabel = 'Mbit/s' if rateUnit.lower() != 'bytes' else 'MB/s'

    show_speed_data_summary(data, isRaw=isRaw, rateUnit=rateUnit)
    # click.echo(template.format(*_data_formatter(data, 0, isRaw, rateUnit)))

    debug_msg(data, "Temp details listed below", 'SpeedTest Details')
    # _PP_.pprint(data)

    # {   'bytes_received': 366199597,
    #     'bytes_sent': 37036032,
    #     'client': {   'country': 'US',
    #                   'ip': '167.88.61.92',
    #                   'isp': 'GTHost',
    #                   'ispdlavg': '0',
    #                   'isprating': '3.7',
    #                   'ispulavg': '0',
    #                   'lat': '37.3931',
    #                   'loggedin': '0',
    #                   'lon': '-121.962',
    #                   'rating': '0'},
    #     'download': 292887701.1503456,
    #     'location': 'CodeAnywhere Test Server',
    #     'locationTZ': 'America/New_York',
    #     'ping': 5.056,
    #     'server': {   'cc': 'US',
    #                   'country': 'United States',
    #                   'd': 9.962686532913219,
    #                   'host': 'speedtest.ridgewireless.net:8080',
    #                   'id': '12818',
    #                   'lat': '37.3230',
    #                   'latency': 5.056,
    #                   'lon': '-122.0322',
    #                   'name': 'Cupertino, CA',
    #                   'sponsor': 'Ridge Wireless',
    #                   'url': 'http://speedtest.ridgewireless.net:8080/speedtest/upload.php'},
    #     'share': None,
    #     'timestamp': '2020-07-15T17:08:55.735084Z',
    #     'upload': 28967314.988596343}


def show_speed_data_table(data, showRowNum=True, isRaw=False, rateUnit=_APP_BITS_):
    """Format and display SpeedTest data.

    Args:
        data:       List of data rows/records if 'table' is TRUE. Else use individual data row/record.
        showRowNum: If TRUE, show row number in left-most column
        isRaw:      If TRUE, data is is 'raw' format.
        rateUnit:   MB/s if 'bytes', else Mbit/s
    """

    # Mbit/s or MB/s
    unitLbl = 'Mbit/s' if rateUnit.lower() != 'bytes' else 'MB/s'

    if showRowNum:
        #           |12345|123456789123456789|123456789123456789|1234567890|1234567890|1234567890|
        #           |     |                  |                  |          |          |          |
        hdr1 = "     |              Date/Time              |          |          |          "
        hdr2 = "     |        UTC       |   At Location    |   PING   |   DOWN   |    UP    "
        hdr3 = "  #  |  MM/DD/YY HH:MM  |  MM/DD/YY HH:MM  |    ms    |  {0:^6s}  |  {0:^6s}  ".format(unitLbl)
        divider = "-----|------------------|------------------|----------|----------|----------"

        col1 = " {:>3s} |  {!s:14s}  |  {!s:14s}  |" if isRaw else " {:>3s} |  {:14s}  |  {:14s}  |"
    else:
        #           |123456789012345678|123456789012345678|1234567890|1234567890|1234567890|
        #           |                  |                  |          |          |          |
        hdr1 = "              Date/Time              |          |          |          "
        hdr2 = "        UTC       |    At Location   |   PING   |   DOWN   |    UP    "
        hdr3 = "  MM/DD/YY HH:MM  |  MM/DD/YY HH:MM  |    ms    |  {0:^6s}  |  {0:^6s}  ".format(unitLbl)
        divider = "------------------|------------------|----------|----------|----------"

        col1 = "  {!s:14s}  |  {!s:14s}  |" if isRaw else "  {:14s}  |  {:14s}  |"

    colN = " {:8.3f} | {:8.2f} | {:8.2f} " if isRaw else " {:8s} | {:8s} | {:8s} "

    template = col1 + colN
    rowNum = 0

    click.echo()
    click.echo(hdr1)
    click.echo(hdr2)
    click.echo(divider)
    click.echo(hdr3)
    click.echo(divider)

    for row in data:
        if showRowNum:
            rowNum += 1
        click.echo(template.format(*_data_formatter(row, rowNum, isRaw, rateUnit)))

    click.echo()


def historic_speed_data(settings, numRecs, unit, first: bool):
    """Retrieve historic SpeedTest data.

    Args:
        settings: List with data store settings
        numRecs:  Number of records to retrieve
        unit:     Unit string.
        first:    Flag to indicate whether to retrieve first or last ## records.
    """

    try:
        data = get_speed_data(settings, numRecs, first)

        if len(data):
            show_speed_data_table(data, showRowNum=True, isRaw=True, rateUnit=unit)
        else:
            click.echo('-- No data records found! --')

    except OSError as e:
        raise click.ClickException(e)


def new_speed_data(settings, numRuns, unit, display, summary: bool, save: bool):
    """Retrieve new SpeedTest data.

    Args:
        settings: List with data store settings
        numRuns:  Number of times to run SpeedTest to retrieve
        unit:     Unit string.
        display:  Which display to use
        summary:  If true, only show summary info of SpeedTest data
        save:     If true, then save SpeedTest data to data store
    """

    data = []
    for i in range(0, numRuns):
        try:
            data.append(run_speedtest(settings))

        except OSError as e:
            raise click.ClickException(e)

        if display.lower() == 'stdout':
            click.echo('-- Internet Speed Test {} of {} --'.format(str(i + 1), str(numRuns)))

            if summary:
                show_speed_data_summary(data[i], isRaw=True, rateUnit=unit)
            else:
                show_speed_data_details(data[i], isRaw=True, rateUnit=unit)

        elif display.lower() == 'epaper':
            #
            #
            click.echo('-- PRINT TO EPAPER CODE HERE --')
            #
            #

        if (i + 1) < numRuns:
            time.sleep(_APP_SLEEP_)

    if save:
        try:
            save_speed_data(settings, data)

        except OSError as e:
            raise click.ClickException(e)


# =========================================================
#                C L I C K   C O M M A N D S
# =========================================================
#                  M A I N   C o m m a n d
# ---------------------------------------------------------
@click.group()
@click.option(
    '--ini',
    type=click.Path(),
    default=os.path.join(click.get_app_dir(_APP_NAME_), _APP_CONFIG_),
    help="Name of '*.ini' file to use.",
)
@click.pass_context
def main(ctx, ini: str = ''):
    """Check and log <some test> and related metrics.

    This tool can check and log the <some crazy stats> on demand. To continuously
    check and log <some crazy stats>, simply use cron (or similar) to run
    the '<appname> xxxxxxxx' command on a regular basis.
    """
    ctx.obj = {
        'globals': {
            'appName': _APP_NAME_,
            'configFName': os.path.expanduser(ini),
            'appMinRuns': _APP_MIN_RUNS_,
            'appMaxRuns': _APP_MAX_RUNS_,
            'appHistory': _APP_HISTORY_,
            'appSleep': _APP_SLEEP_,
            'dbName': _DB_NAME_,
            'dbTable': _DB_TABLE_,
        }
    }

    return 0


# ---------------------------------------------------------
#                   S u b - C o m m a n d s
# ---------------------------------------------------------
# CMD: debug
# ---------------------------------------------------------
@main.command()
@click.option(
    '--msg',
    default='Testing 1-2-3',
    show_default=True,
    help='Display debug/test message on STDOUT or other attached screen.',
)
@click.pass_context
def debug(ctx, msg: str):
    """
    Show debug message.
    """
    click.echo("\n--------------------- [ DEBUG ] --------------------\n")
    click.echo(msg)
    click.echo("\n----------------------------------------------------")
    click.echo("App Configuration:\n >> '{}'".format(ctx.obj['globals']['configFName']))
    click.echo("----------------------------------------------------\n")


# ---------------------------------------------------------
# CMD: config
# ---------------------------------------------------------
@main.command()
@click.option(
    '--section',
    type=click.Choice(['data', 'test', 'all'], case_sensitive=False),
    default='all',
    show_default=True,
    help='Config file section name.',
)
@click.option(
    '--set/--show', 'update',
    default=True,
    help='Set and (save) application settings for a given section, or just show/display current settings.',
)
@click.option(
    '--force',
    is_flag=True,
    help='Works with \'--set\' flag and overwrites an existing config file.',
)
@click.option(
    '--verify',
    is_flag=True,
    help='Works with \'--section\' flag and verifies that the system is configured properly.',
)
@click.pass_context
def config(ctx, section: str, update: bool, force: bool, verify: bool):
    """
    Define and store configuration values for a given section in the config file.
    """
    try:
        if update and not verify:
            save_settings(ctx.obj['globals'], section.lower(), force)
        else:
            show_settings(ctx.obj['globals'], section.lower(), verify)

    except (OSError, ValueError) as e:
        click.echo("\nERROR! {}\n".format(e))
        sys.exit(1)


# ---------------------------------------------------------
# CMD: <main test or action>
# ---------------------------------------------------------
@main.command()
@click.option(
    '--display',
    type=click.Choice(['stdout', 'epaper', 'none'], case_sensitive=False),
    default='stdout', show_default=True,
    help='Display speed test data on STDOUT or ePaper screen.',
)
@click.option(
    '--save/--no-save', 'save',
    default=True,
    help='Save speed test data to data storage.',
)
@click.option(
    '--summary/--details', 'summary_only',
    default=True,
    help='Show summary or details from SpeedTest run.',
)
@click.option(
    '--count', 'cntr',
    default=1, show_default=True,
    help='Number of tests to run in sequence, or records to retrieve for review.',
)
@click.option(
    '--history',
    is_flag=True,
    help="Show history of given number (using 'count') of previously saved speed tests.",
)
@click.option(
    '--first/--last', 'first',
    default=True,
    help="Show 'first' or 'last' 'count' number of previously saved speed tests.",
)
@click.pass_context
def dothing(ctx, display: str, save: bool, summary_only: bool, cntr: int, history: bool, first: bool):
    """This is the main thing that this app does.

    Replace this text with whatever this things does :-)

    \b
    Speed data samples are retrieved/stored as follows:
        'time'      Unix timestamp
        'ping'      Ping response time (ms)
        'download'  Download speed (Mbit/s)
        'upload'    Upload speed (Mbit/s)
    """
    ctx.obj['settings'] = read_settings(ctx.obj['globals'])
    if not isvalid_settings(ctx.obj['settings']):
        raise click.ClickException("Invalid and/or incomplete config info!")

    unit = ctx.obj['settings']['speedtest'].get('unit', _APP_BITS_)

    # Show historic data
    if history:
        if cntr < 1 or cntr > ctx.obj['globals']['appHistory']:
            cntr = click.prompt(
                "Enter number of data records to retrieve:",
                type=click.IntRange(1, ctx.obj['globals']['appHistory'], clamp=True),
                default='1',
                show_default=True,
            )

        historic_speed_data(ctx.obj['settings']['speedtest'], cntr, unit, first)

    # Collect new data
    else:
        if cntr < ctx.obj['globals']['appMinRuns'] or cntr > ctx.obj['globals']['appMaxRuns']:
            cntr = click.prompt(
                "Enter number of test cycle runs:",
                type=click.IntRange(ctx.obj['globals']['appMinRuns'], ctx.obj['globals']['appMaxRuns'], clamp=True),
                default=ctx.obj['globals']['appMinRuns'],
                show_default=True,
            )

        new_speed_data(ctx.obj['settings']['speedtest'], cntr, unit, display, summary_only, save)


# =========================================================
#              A P P   S T A R T   S E C T I O N
# =========================================================
if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
