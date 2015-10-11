import os
######
SHELL = os.environ.get('PY_NGSPICE_SHELL', '/bin/tcsh')
NGSPICE = os.environ.get('PY_NGSPICE_SIMULATOR', 'ngspice')
TEXT_EDITOR = os.environ.get('PY_NGSPICE_EDIT', 'nedit')
TMP = os.environ.get('PY_NGSPICE_TMP', '/tmp')
PREFIX = os.environ.get('PY_NGSPICE_PREFIX', 'ngspice_')
MAX_HISTORY = os.environ.get('PY_NGSPICE_MAX_HISTORY', 10)
