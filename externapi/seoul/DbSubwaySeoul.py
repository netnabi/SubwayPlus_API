__author__ = 'yjkim'
# -*- coding: UTF-8 -*-

from base import logger, baseutil

import unittest
from base.dbmysql import DbManager
import mysql.connector as mdb
from mysql.connector import errorcode
from externapi.seoul.SubwayOpenApi import *

_log = logger.get_logger(baseutil.get_filename(__file__))


def _make_apidata_table_name(svc_nm):
    return "API_DATA_"+svc_nm.upper()

_TABLES = {}
_TABLES[SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE] = (
    "CREATE TABLE `"+_make_apidata_table_name(SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE)+"` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")

_TABLES[SB_SERVICE.SVC_SEARCHARRIVALTIMEOFLINE2SUBWAYBYIDSERVICE] = (
    "CREATE TABLE `"+_make_apidata_table_name(SB_SERVICE.SVC_SEARCHARRIVALTIMEOFLINE2SUBWAYBYIDSERVICE)+"` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")


class DbSeoulSubway:

    _dbm = None

    def __init__(self):
        self._dbm = DbManager()
        return

    def init_api_service_tables(self):

        conn = self._dbm.get_connection_apidata_subway()
        if conn is None:
            _log.info("Failed to init api service by connection is invalid")
            return False
        cursor = conn.cursor()

        for name, ddl in _TABLES.iteritems():
            try:
                _log.info("Creating table {}: ".format(name))
                cursor.execute(ddl)
            except mdb.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    _log.warn("Table {} is already exists.".format(name))
                else:
                    _log.error(err)
            else:
                _log.info("Table Created success. {}".format(name))

        cursor.close()
        conn.close()


# Test Class : OpenServiceDataImporter 를 테스트한다.
#
class DbSubwaySeoulTest(unittest.TestCase):
    def test_init_api_service_tables(self):
        ds = DbSeoulSubway()
        ds.init_api_service_tables()
        return


if __name__ == "__main__":
    unittest.main()
