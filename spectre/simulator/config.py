import os

SHELL = os.environ.get('PY_SPECTRE_SHELL', '/bin/tcsh')
SPECTRE = os.environ.get('PY_SPECTRE_SIMULATOR', 'spectre -64')
SETMMSIM = os.environ.get('PY_SPECTRE_ENVIRON','/home/raphael/tool/setmmsim10')
TEXT_EDITOR = os.environ.get('PY_SPECTRE_EDIT', 'nedit')
MAX_HISTORY = os.environ.get('PY_SPECTRE_MAX_HISTORY', 10)
TMP = os.environ.get('PY_SPECTRE_TMP', '/tmp')
PREFIX = os.environ.get('PY_SPECTRE_PREFIX', 'spectre_')
CONFIG_ENVIRON = { # Path of veriloga compilation directory
                   'CDS_AHDLCMI_SIMDB_DIR':os.environ.get('CDS_AHDLCMI_SIMDB_DIR', TMP),
                 }





