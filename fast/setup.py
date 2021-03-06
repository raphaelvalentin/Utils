from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


extensions = [
    Extension("_nearest", ["_nearest.pyx"]),
    ]

setup(
    ext_modules = cythonize(extensions)
)

