from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'Nearest fast functions',
  ext_modules = cythonize("_nearest.pyx"),
)

