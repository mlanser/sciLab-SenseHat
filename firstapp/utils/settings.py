import os
import re
import click

from configparser import ConfigParser, ExtendedInterpolation, Error
from sys import modules as sysmods

#from .speedtest import get_speed_data

_DB_NAME_:    str = 'scilab'
_DB_TABLE_:   str = 'SpeedTest'

_CSV_:        str = 'csv'
_JSON_:       str = 'json'
_SQLite_:     str = 'sqlite'
_API_:        str = 'api'

_SCTN_DATA_:  str = 'data'
_SCTN_MAIN_:  str = 'main'


# =========================================================
#              H E L P E R   F U N C T I O N S
# =========================================================
def _get_option_val(settings, section, option=None, verify=False):
    outStr = '> Missing!' if verify else '- n/a -'

    if section is not None and option is not None:
        try:
            if settings.has_option(section, option):
                outStr = str(settings[section][option])
        except Error:
            outStr = '- Invalid setting! -'

    return outStr


# ---------------------------------------------------------
#                  Manage Data Settings
# ---------------------------------------------------------
#
# [data]
# retain = [-1,0,1-MAX]                     - default num rec's to retain in data store
#                                                 -1 = retain ALL
#                                                  0 = retain none (same as permanent 'no-save')
#                                              1-MAX = max records to retain in data store
#
# history = [1-MAX]                         - default num rec's to retrieve
# sort = [first|last]                       - retrieve first or last 'count' items
#
def _get_data_settings(ctxGlobals):
    retain = click.prompt(
        "Enter default for number of data records to retain in data store:",
        type=click.IntRange(-1, ctxGlobals['appHistory'], clamp=True),
        default='-1',
        show_default=True,
    )
    history = click.prompt(
        "Enter default for number of data records to retrieve:",
        type=click.IntRange(1, ctxGlobals['appHistory'], clamp=True),
        default='1',
        show_default=True,
    )
    sort = click.prompt(
        "Select default history list/sort order",
        type=click.Choice(['first', 'last'], case_sensitive=False),
        default='first',
    )
    settings = {
        _SCTN_DATA_: {
            'retain': retain,
            'history': history,
            'sort': sort.lower(),
            }
        }
    
    return settings


def _validate_data_settings(settings):
    # 
    # @NOTE - there are no required items in this section 
    #         and we're only keeping this function to be 
    #         consistent with other config sections.
    # 
    return True


# ---------------------------------------------------------
#                Manage MAIN Settings
# ---------------------------------------------------------
#
# [<name of test tool section>]
# count = [1-100]                       - num test cycle runs
# sleep = [1-60]                        - seconds between each test run
#
# threads = single|multi                - run single or multiple threads
# unit = bits|bytes                     - display speeds in Mbits/s or MB/s 
# share = yes|no                        - share test results
# location = <some location name>       - name of location where test computer is located
# locationTZ = <TZ name>                - Time zone at location (e.g. 'America/New York')
#
# storage = CSV|JSON|SQLite|API         - data storage type. Note: API not yet implemented.
#
# host = <hostname or file path>        - data storage host. If file-based (i.e. CSV, JSON, SQLite),
#                                         then this is a path/filename)
#   Ex:     ~/speedtest.csv
#           ~/speedtest.json
#           ~/ntwkmgr.sqlite            - SQLite file can hold several tables
#
def _get_speedtest_settings(ctxGlobals):
    defaults = {
        'count': 1, 'sleep': 60, 'threads': 'multi', 'unit': 'bits', 'share': False, 
        'location': None, 'locationTZ': None, 
        'host': None, 'ssl': False, 
    }
    
    count = click.prompt(
        "Enter default for number of test cycle runs:",
        type=click.IntRange(ctxGlobals['appMinRuns'], ctxGlobals['appMaxRuns'], clamp=True),
        default=ctxGlobals['appMinRuns'],
        show_default=True,
    )
    sleep = click.prompt(
        "Enter wait time (in seconds) between test cycle runs:",
        type=click.IntRange(1, 60, clamp=True),
        default='60',
        show_default=True,
    )
    
    threads = click.prompt(
        "Number of threads for SpeedTest", 
        type=click.Choice(['single', 'multi'], case_sensitive=False),
        default='multi',
        show_default=True,
    )
    unit = click.prompt(
        "Select speed rate unit per second", 
        type=click.Choice(['bits', 'bytes'], case_sensitive=False),
        default='bits',
        show_default=True,
    )
    share = click.prompt(
        "Share test results", 
        type=click.Choice(['yes', 'no'], case_sensitive=False),
        default='no',
        show_default=True,
    )
    location = click.prompt(
        "Name of location where test is run", 
    )
    locationTZ = click.prompt(
        "Name of (PYTZ) timezone for location", 
        default='America/New_York',
        show_default=True,
    )
    
    storage = click.prompt(
        "Enter data storage type", 
        type=click.Choice(['CSV', 'JSON', 'SQLite', 'API'], case_sensitive=False),
        default='SQLite',
        show_default=True,
    )
    
    if storage.lower() == _CSV_:
        settings = _get_speedtest_settings_CSV(defaults, ctxGlobals)
        
    elif storage.lower() == _JSON_:
        settings = _get_speedtest_settings_JSON(defaults, ctxGlobals)
        
    elif storage.lower() == _SQLite_:
        settings = _get_speedtest_settings_SQLite(defaults, ctxGlobals)
        
    # elif storage.lower() == _API_:
    #    settings = _get_speedtest_settings_API(defaults, ctxGlobals)
        
    else:
        raise ValueError("Invalid storage type '{}'".format(storage))
        
    settings.update([
        ('count', count),
        ('sleep', sleep),
        ('threads', ('multi' if threads.lower() != 'single' else 'single')),
        ('unit', ('bits' if unit.lower() != 'bytes' else 'bytes')),
        ('share', (False if share.lower() != 'yes' else True)), 
        ('location', location),
        ('locationTZ', locationTZ),
        ('storage', storage),
    ])

    return {_SCTN_SPEED_: settings}


def _get_speedtest_settings_CSV(defaults, ctxGlobals):
    host = click.prompt(
        "Enter path to CSV data file",
        type=click.Path(),
        default=os.path.join(click.get_app_dir(ctxGlobals['appName']), ctxGlobals['dbTable'].lower() + '.csv'),
        show_default=True,
    )

    defaults.update([('host', host)])
    return defaults
    
    
def _get_speedtest_settings_JSON(defaults, ctxGlobals):
    host = click.prompt(
        "Enter path to JSON data file",
        type=click.Path(),
        default=os.path.join(click.get_app_dir(ctxGlobals['appName']), ctxGlobals['dbTable'].lower() + '.json'),
        show_default=True,
    )

    defaults.update([('host', host)])
    return defaults


def _get_speedtest_settings_SQLite(defaults, ctxGlobals):
    host = click.prompt(
        "Enter path to SQLite database.\nNote: ':memory:' is not supported.",
        type=click.Path(),
        default=os.path.join(click.get_app_dir(ctxGlobals['appName']), ctxGlobals['dbName'].lower() + '.sqlite'),
        show_default=True,
    )
    dbtable = click.prompt(
        "Enter name of database table",
        default=ctxGlobals['dbTable'],
        show_default=True,
    )

    defaults.update([('host', host), ('dbtable', dbtable)])
    return defaults


def _get_speedtest_settings_API(defaults, ctxGlobals):
    pass
#    host = click.prompt(
#        "Enter database URL (protocal, host, and port)",
#        default='http://localhost:8086',
#        show_default=True,
#    )
#    dbuser = click.prompt("Enter database user name")
#    dbpswd = click.prompt("Enter database user password", default='', hide_input=True)
#    dbtable = click.prompt(
#        "Enter name of database table",
#        default=defaults['dbtable'],
#        show_default=True,
#    )
#    dbname = click.prompt(
#        "Enter name of database",
#        default=defaults['dbname'],
#        show_default=True,
#    )

#    defaults.update([
#        ('host', host), ('dbtable', dbtable), ('dbname', dbname),
#        ('dbuser', dbuser), ('dbpswd', dbpswd)
#    ])
#    return defaults


def _validate_speedtest_settings(settings):
    #
    # @NOTE - we can only verify that values are stored
    #         in config, but not that they're correct.
    #
    if not settings.has_option(_SCTN_SPEED_, 'host'):
        return False

    return True


def _verify_datastore(settings):
    if not settings.has_section(_SCTN_SPEED_):
        return "- Data store not defined in '{}' section".format(_SCTN_SPEED_)

    try:
        get_speed_data(settings[_SCTN_SPEED_], 1, True)
    except OSError:
        return "- Unable to access data store '{}'".format(settings[_SCTN_SPEED_].get('host'))

    return '- Data store OK!'


def _verify_epaper():
    reqMods = [
        'numpy',
        'waveshare_epd',
        'PIL',
        'spidev',
        'RPi.GPIO',
    ]
    availMods = list(sysmods.keys())

    outStr = '- Required modules installed for ePaper display'
    errStr = ''
    success = True

    for mod in reqMods:
        pattern = re.compile("{}\\.*".format(str(mod).replace('.', '\\.')))
        if not any(pattern.match(line) for line in availMods):
            success = False
            errStr += "- '{}' module missing\n".format(mod)

    return outStr if success else errStr


# ---------------------------------------------------------
#                  Manage Data/Settings
# ---------------------------------------------------------
def isvalid_settings(settings):
    """Validate (to some degree) that application settings (e.g. ensure that
    that required options are present, etc.).
    
    Args:
        settings: Settings to validate
        
    Returns:
        TRUE if settings pass all tests, else FALSE.
    """
    #
    # Need to put in some actual tests here
    #

    if not _validate_wifi_settings(settings):
        return False

    if not _validate_data_settings(settings):
        return False

    if not _validate_speedtest_settings(settings):
        return False
    
    if not _validate_sometest_settings(settings):
        return False

    return True


def read_settings(ctxGlobals):
    """Read/parse all application settings from config file.
    
    Args:
        ctxGlobals: List of misc global values stored in CTX app object
        
    Returns:
        Config object with all settings
        
    Raises:
        OSError:    If unable to read config file 
    """
    
    if os.path.exists(ctxGlobals['configFName']):
        try:
            config = ConfigParser(interpolation=ExtendedInterpolation(), allow_no_value=True)
            config.read(ctxGlobals['configFName'])
        except Error as e:
            raise ValueError("Invalid configuration settings!\n{}".format(e))
    else:
        raise OSError("Config file '{}' does NOT exist or cannot be accessed!".format(ctxGlobals['configFName']))

    return config
        
        
def save_settings(ctxGlobals, section, overwrite=False):
    """Save application settings to config file.
    
    Args:
        ctxGlobals: List of misc global values stored in CTX app object
        section:    Name of section to update. Or use 'all' to update all settings.
        overwrite:  If true, create config file if it does not already exist.
        
    Raises:
        ValueError: If invalid section name.
        OSError:    If config file already exists.
    """

    if not section.lower() in [_SCTN_WIFI_, _SCTN_DATA_, 'test', 'all']:
        raise ValueError("Invalid section '{}'".format(section))

    config = ConfigParser(interpolation=ExtendedInterpolation(), allow_no_value=True)

    if not os.path.exists(ctxGlobals['configFName']):
        path = os.path.dirname(os.path.abspath(ctxGlobals['configFName']))
        if not os.path.exists(path):
            os.makedirs(path)
    elif overwrite:
        config.read(ctxGlobals['configFName'])
    else:
        raise OSError("Config file '{}' already exists.\n\nPlease use '--force' flag to overwrite it.".format(ctxGlobals['configFName']))

    if section in ['all', _SCTN_WIFI_]:
        config.read_dict(_get_wifi_settings(ctxGlobals))

    if section in ['all', _SCTN_DATA_]:
        config.read_dict(_get_data_settings(ctxGlobals))

    if section in ['all', 'test']:
        config.read_dict(_get_speedtest_settings(ctxGlobals))
        config.read_dict(_get_sometest_settings(ctxGlobals))

    with open(ctxGlobals['configFName'], 'w') as configFile:
        config.write(configFile)


def show_settings(ctxGlobals, section, verify=False):
    """Retrieve and display application settings from config file.
    
    Args:
        ctxGlobals: List of misc global values stored in CTX app object
        section:    Name of section to display. Or use 'all' to view all settings.
        verify:     If true, verify settings for a given 'section' in config file.

    Raises:
        ValueError: If invalid section name.
        OSError:    If unable to read config file.
    """

    if not section.lower() in [_SCTN_WIFI_, _SCTN_DATA_, 'test', 'all']:
        raise ValueError("Invalid section '{}'".format(section))

    settings = read_settings(ctxGlobals)

    if section in ['all', _SCTN_WIFI_]:
        #
        # [wifi]
        # ssid = <some SSID>
        # security = WPA|WPA2|WEP
        # password = <some wifi password>
        #
        click.echo("\n--- [Settings: wifi] ----------")
        click.echo("SSID:               {}".format(_get_option_val(settings, _SCTN_WIFI_, 'ssid', verify)))
        click.echo("Security:           {}".format(_get_option_val(settings, _SCTN_WIFI_, 'security', verify)))
        click.echo("Password:           {}".format(_get_option_val(settings, _SCTN_WIFI_, 'password', verify)))

    if section in ['all', _SCTN_DATA_]:
        # [data]
        # history = [1-100]                     - default num rec's to retrieve
        # sort = [first|last]                   - retrieve first or last 'count' items
        #
        click.echo("\n--- [Settings: data] ----------")
        click.echo("Default Retain:     {}".format(_get_option_val(settings, _SCTN_DATA_, 'retain', verify)))
        click.echo("Default History:    {}".format(_get_option_val(settings, _SCTN_DATA_, 'history', verify)))
        click.echo("Default Sort:       {}".format(_get_option_val(settings, _SCTN_DATA_, 'sort', verify)))

    if section in ['all', 'test']:
        click.echo("\n--- [Settings: tests] ---------")
        # [<name of test tool section>]
        # uri = <uri/path to test tool>         - USED AS NEEDED -
        # params = <any test tool params>       - USED AS NEEDED -
        #
        # count = [1-100]                       - num test cycle runs
        # sleep = [1-60]                        - seconds between each test run
        #
        # threads = single|multi                - run single or multiple threads
        # unit = bits|bytes                     - display speeds in Mbits/s or MB/s 
        # share = yes|no                        - share test results
        # location = <some location name>       - name of location where test computer is located
        # locationTZ = <TZ name>                - Time zone at location (e.g. 'America/New York')
        #
        # storage = CSV|JSON|SQLite|API         - data storage type
        #
        # host = <hostname or file path>        - data storage host. If file-based (i.e. CSV, JSON, SQLite),
        #                                         then this is a path/filename)
        #   Ex:     ~/speedtest.csv
        #           ~/speedtest.json
        #           ~/ntwkmgr.sqlite            - SQLite file can hold several tables
        #
        # dbtable = <db table name>             - Used for SQLite
        # dbname = <db name>                    - Used for SQLite
        #
        click.echo("SpeedTest Settings")
        click.echo("  Test Run Count:   {}".format(_get_option_val(settings, _SCTN_SPEED_, 'count', verify)))
        click.echo("  Sleep/Wait Time:  {}".format(_get_option_val(settings, _SCTN_SPEED_, 'sleep', verify)))
        click.echo("  Threads:          {}".format(_get_option_val(settings, _SCTN_SPEED_, 'threads', verify)))
        click.echo("  Speed Rate Unit:  {}".format(_get_option_val(settings, _SCTN_SPEED_, 'unit', verify)))
        click.echo("  Share Results:    {}".format(_get_option_val(settings, _SCTN_SPEED_, 'share', verify)))
        click.echo("  Location Name:    {}".format(_get_option_val(settings, _SCTN_SPEED_, 'location', verify)))
        click.echo("  Location TZ:      {}".format(_get_option_val(settings, _SCTN_SPEED_, 'locationTZ', verify)))
        click.echo("  DB Storage Type:  {}".format(_get_option_val(settings, _SCTN_SPEED_, 'storage', verify)))
        click.echo("  DB Host:          {}".format(_get_option_val(settings, _SCTN_SPEED_, 'host', verify)))
        click.echo("  DB Table:         {}".format(_get_option_val(settings, _SCTN_SPEED_, 'dbtable', verify)))
        click.echo("  DB Name:          {}".format(_get_option_val(settings, _SCTN_SPEED_, 'dbname', verify)))

        click.echo("\nSome Other Test Settings")
        click.echo("  CLI URI:          {}".format(_get_option_val(settings, 'sometest', 'uri', verify)))
        click.echo("  CLI params:       {}".format(_get_option_val(settings, 'sometest', 'params', verify)))

    if verify:
        #
        # General requirements:
        #  - ePaper support
        #  - Data store access
        #
        click.echo("\n--- [General Requirements] ----")
        click.echo("ePaper Support:\n{}".format(_verify_epaper()))
        click.echo("Datastore Access:\n{}".format(_verify_datastore(settings)))

    click.echo("\n-------------------------------")
    click.echo("CONFIG: '{}'\n".format(ctxGlobals['configFName']))
