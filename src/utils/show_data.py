# =========================================================
#             G E N E R I C   F U N C T I O N S
# =========================================================
def show_current():
    pass


def show_history():
    pass


# VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
# import speedtest

_DB_ORDER_: str = 'timestamp|ASC'
_DB_FLDS_ = {
    'raw': {'timestamp': str, 'location': str, 'locationTZ': str, 'ping': float, 'download': float, 'upload': float},
    'csv': {'timestamp': None, 'location': None, 'locationTZ': None, 'ping': None, 'download': None, 'upload': None},
    'json': {'timestamp': None, 'location': None, 'locationTZ': None, 'ping': None, 'download': None, 'upload': None},
    'sql': {'timestamp': 'TEXT|idx', 'location': 'TEXT|idx', 'locationTZ': 'TEXT|idx', 'ping': 'REAL',
            'download': 'REAL', 'upload': 'REAL'}
}


# =========================================================
#                D A T A   F U N C T I O N S
# =========================================================
def get_speed_data(settings, numRecs, first=True):
    """Retrieve SpeedTest data records from preferred data store as defined in application settings.

    Args:
        settings: List with data store settings
        numRecs:  Number of records to retrieve
                  NOTE: for InfluxDB v2.x this represents last X hours

        first:    If TRUE, retrieve first 'numRec' records, else retrieve last 'numRec' records
                  NOTE: this is not used for InfluxDB v2.x

    Returns:
        List of data records

    Raises:
        OSError: If data store is not supported and/or cannot be accessed.
    """

    if settings.get('storage').lower() == 'csv':
        from .datastore.csv import get_data
        return get_data(settings.get('host'), _DB_FLDS_['raw'], numRecs, first)

    elif settings.get('storage').lower() == 'json':
        from .datastore.json import get_data
        return get_data(settings.get('host'), _DB_FLDS_['raw'], numRecs, first)

    elif settings.get('storage').lower() == 'sqlite':
        from .datastore.sqlite import get_data
        return get_data(settings.get('host'), _DB_FLDS_['raw'], settings.get('dbtable'), _DB_ORDER_, numRecs, first)

    else:
        raise OSError("Data storage type '{}' is not supported!".format(str(settings.get('storage'))))
