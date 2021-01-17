import random

import pprint
import pytest
from inspect import currentframe, getframeinfo


# =========================================================
#       L I T T L E   H E L P E R   F U N C T I O N S
# =========================================================
def pp(capsys, data, frame=None):  
    with capsys.disabled():
        _PP_ = pprint.PrettyPrinter(indent=4)
        print('\n')
        if frame is not None:
            print('LINE #: {}\n'.format(getframeinfo(frame).lineno))
        _PP_.pprint(data)
