__author__ = 'yjkim'
# -*- coding: UTF-8 -*-

import unittest
import _mysql
import bo

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
        db = _DB_NAME_API_DATA_SUBWAY
        con = _mysql.connect(host=db["host"], db=db["db"], user=db["user"], passwd=db["passwd"])
        return con

# Test Class : OpenServiceDataImporter 를 테스트한다.
#
class DbManagerTest(unittest.TestCase):

    def test_connect_API_DATA_SUBWAY(self):
        dbm = DbManager()
        testcon = dbm.get_connection_apidata_subway()
        self.assertNotEqual(testcon, None)
        self.assertEqual(testcon.error(), '')   # is None-Error in Python
        testcon.close()

if __name__ == "__main__":
    unittest.main()