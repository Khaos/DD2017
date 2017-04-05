from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

sourcefiles = ['stitch_wrapper.pyx', 'stitch_rects.cpp', 'hungarian/hungarian.cpp']

extensions = [Extension("utils.stitch_wrapper", sourcefiles)]

setup(ext_modules = cythonize(Extension("utils.stitch_wrapper", ['stitch_wrapper.pyx', 'stitch_rects.cpp', 'hungarian/hungarian.cpp']),language="c++",))


