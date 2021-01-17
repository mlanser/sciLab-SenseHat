import os

import random
import string
import uuid

import pytest


# =========================================================
#                      G L O B A L S
# =========================================================


# =========================================================
#        G L O B A L   P Y T E S T   F I X T U R E S
# =========================================================
@pytest.fixture()
def new_config_file(tmpdir_factory):
    """Only create the filename, but not the actual file."""
    testDir = tmpdir_factory.mktemp('test')
    configFile = testDir.join(uuid.uuid4().hex + '.ini')
    
    return str(configFile)
  