import uuid
import pprint
from inspect import getframeinfo

import pytest


# =========================================================
#                      H E L P E R S
# =========================================================
class Helpers:
    @staticmethod
    def pp(capsys, data, frame=None):
        with capsys.disabled():
            _PP_ = pprint.PrettyPrinter(indent=4)
            print('\n')
            if frame is not None:
                print('LINE #: {}\n'.format(getframeinfo(frame).lineno))
            _PP_.pprint(data)


# =========================================================
#        G L O B A L   P Y T E S T   F I X T U R E S
# =========================================================
@pytest.fixture()
def new_config_file(tmpdir_factory):
    """Only create the filename, but not the actual file."""
    testDir = tmpdir_factory.mktemp('test')
    configFile = testDir.join(uuid.uuid4().hex + '.ini')

    return str(configFile)
