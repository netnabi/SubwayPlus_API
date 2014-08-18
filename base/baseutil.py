__author__ = 'yjkim'

import os

# input : __file__
def get_filename(_args__file__):
    _dirname, _filename = os.path.split( os.path.abspath(_args__file__) )
    return _filename

# input : __file__
def get_directory(_args__file__):
    _dirname, _filename = os.path.split( os.path.abspath(_args__file__) )
    return _dirname