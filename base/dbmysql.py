__author__ = 'yjkim'
# -*- coding: UTF-8 -*-

import unittest
import mysql.connector as mdb
from mysql.connector import errorcode
import bo
import logger
import baseutil


_log = logger.get_logger(baseutil.get_filename(__file__))

#
# MySQL - Manual :
# http://mysql-python.sourceforge.net/MySQLdb.html#mysql-c-api-translation
# http://www.mikusa.com/python-mysql-docs/docs/MySQLdb.connections.html
#

# List of database
_DB_NAME_API_DATA_SUBWAY = {"host":"localhost", "db":"apidata_subway","user":"subway","passwd":"subway"}


class DbManager(bo.BaseObject):


    # Return MySQL Connection of _DB_NAME_API_DATA_SUBWAY
    def get_connection_apidata_subway(self):
        try:
            db = _DB_NAME_API_DATA_SUBWAY
            con = mdb.connect(host=db["host"], database=db["db"], user=db["user"], password=db["passwd"])
        except mdb.Error as _err:
            if _err.errno == errorcode.ER_ACCESS_DENIED_CHANGE_USER_ERROR:
                _log.error("Something is wrong with your user name or password")
            elif _err.errno == errorcode.ER_BAD_DB_ERROR:
                _log.error("Database does not exists")
            else:
                _log.error(_err)
            return None
        else:
            _log.info("database connected ='%s'", db["db"])
            return con

    def get_dbname_apidata_subway(self):
        db = _DB_NAME_API_DATA_SUBWAY
        return db["db"]


# Test Class : OpenServiceDataImporter 를 테스트한다.
#
class _DbManagerTest(unittest.TestCase):

    def test_connect_API_DATA_SUBWAY(self):
        dbm = DbManager()
        testcon = dbm.get_connection_apidata_subway()
        self.assertNotEqual(testcon, None)
        testcon.close()

if __name__ == "__main__":
    unittest.main()