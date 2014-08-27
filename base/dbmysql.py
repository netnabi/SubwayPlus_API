__author__ = 'yjkim'
# -*- coding: UTF-8 -*-

import unittest
import pymysql as mdb
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
_DB_NAME_API_DATA_SUBWAY = {
    "host":"localhost",
    "port":3306,
    "db":"apidata_subway",
    "user":"subway",
    "passwd":"subway",
    "charset":"utf8"
}


class DbManager(bo.BaseObject):


    # Return MySQL Connection of _DB_NAME_API_DATA_SUBWAY
    def get_connection_apidata_subway(self):
        try:
            db = _DB_NAME_API_DATA_SUBWAY
            con = mdb.connect(host=db["host"],
                              port=db["port"],
                              db=db["db"],
                              user=db["user"],
                              passwd=db["passwd"],
                              charset=db["charset"])
        except mdb.Error as _err:
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