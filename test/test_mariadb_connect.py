__author__ = 'aj'
# -*- coding: UTF-8 -*-

# Use MySQL Connector Module : pyMySQL (0.6.2)
import pymysql
import unittest
from base import baseutil
from base import logger

_log = logger.get_logger(baseutil.get_filename(__file__))



# Test Class : OpenServiceDataImporter 를 테스트한다.
#
class _DbConnectionTest(unittest.TestCase):

    def test_dbConnectionTest(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='subway', passwd='subway', db='apidata_subway')
        cur = conn.cursor()
        cur.execute("SELECT vid,value FROM testTable")
        print(cur.description)
        print()
        for row in cur:
           print(row)

        cur.close()
        conn.close()
        # self.assertNotEqual(None, None)


if __name__ == "__main__":
    unittest.main()