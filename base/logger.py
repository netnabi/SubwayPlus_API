__author__ = 'yjkim'
# -*- coding: UTF-8 -*-

import os
import unittest
import logging
import logging.handlers


_dirname, _filename = os.path.split( os.path.abspath(__file__) )
_log_directory = _dirname+"/../logs/"

if not os.path.exists(_log_directory):
    os.makedirs(_log_directory)

def get_logger(log_name):

   if log_name == '':
       log_name = 'default'

   _LOG_FILENAME = _log_directory+log_name+'.log'
   print("Logger FileName = "+_LOG_FILENAME)

   # Set up a specific logger with our desired output level
   _LOGGER = logging.getLogger(log_name)
   _LOGGER.setLevel(logging.DEBUG)

   # Add the log message handler to the logger
   _handler = logging.handlers.RotatingFileHandler(
                 _LOG_FILENAME, maxBytes=(10*1024*1024*1024), backupCount=5)

   # Format : 2005-03-19 15:10:26,618 - simple_example - DEBUG - debug message
   _formatter = logging.Formatter("%(asctime)s - %(name)15s - %(levelname)-05s - %(message)s")
   _handler.setFormatter(_formatter)
   _LOGGER.addHandler(_handler)

   return _LOGGER



# Test Class : OpenServiceDataImporter 를 테스트한다.
#
class _get_loggerTest(unittest.TestCase):

    def test_SimpleInfo(self):
        logger = get_logger("test_logger")
        logger.info("information:%s",'test')
        return


if __name__ == "__main__":
    unittest.main()