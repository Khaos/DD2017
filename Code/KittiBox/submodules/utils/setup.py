#!/usr/bin/python  
# python version: 3.5  
# Filename: setup.py  

# Run as:    
#    python setup.py build_ext #--inplace    

import sys

sys.path.insert(0, "..")

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

# ext_module = cythonize("stitch_wrapper.pyx")    
ext_module = Extension(
    "stitch_wrapper",
    ['stitch_wrapper.pyx', 'stitch_rects.cpp', 'hungarian/hungarian.cpp'],
    language="c++",
    # extra_compile_args=["/openmp"],
    # extra_link_args=["/openmp"],
)

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[ext_module],
)

#########3
# from distutils.core import setup
# from Cython.Build import cythonize
# from distutils.extension import Extension
# 
# sourcefiles = ['stitch_wrapper.pyx', 'stitch_rects.cpp', 'hungarian/hungarian.cpp']
# 
# extensions = [Extension("utils.stitch_wrapper", sourcefiles)]
# 
# setup(ext_modules = cythonize(Extension("utils.stitch_wrapper", ['stitch_wrapper.pyx', 'stitch_rects.cpp', 'hungarian/hungarian.cpp']),language="c++",))
# 
#


