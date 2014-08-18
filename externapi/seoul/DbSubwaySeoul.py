__author__ = 'yjkim'
# -*- coding: UTF-8 -*-

from base import logger, baseutil

from base.bo import BoException
import unittest
from base.dbmysql import DbManager
import mysql.connector as mdb
from mysql.connector import errorcode
from externapi.seoul.SubwayOpenApi import *


_log = logger.get_logger(baseutil.get_filename(__file__))

class DbSeoulSubwayException(BoException):
    """
    """



# DDL Tools
# ###############################################################################

_NEW = "_NOW"   # Latest downloaded from REST API
_CUR = "_CUR"   # Current Loaded and Distributed Data

def _make_apidata_table_name(svc_nm, is_new):
    if  is_new is True:
        return "API_DATA_"+svc_nm.upper()+_NEW
    else:
        return "API_DATA_"+svc_nm.upper()+_CUR

# List of DDL
_DDL_SVC_SEARCHSTNBYSUBWAYLINESERVICE = (
    " CREATE TABLE `{}` (  "
    "   `STATION_CD` char(6) NOT NULL DEFAULT '0' COMMENT 'Unique Station Code',  "
    "   `FR_CODE` char(6) DEFAULT NULL COMMENT 'USC for Foreign (Alias)',  "
    "   `STATION_NM` char(60) DEFAULT NULL COMMENT 'Subway Station Name',  "
    "   `LINE_NUM` char(2) DEFAULT NULL COMMENT 'Line Number of Subway',  "
    "   PRIMARY KEY (`STATION_CD`)  "
    " ) ENGINE=InnoDB DEFAULT CHARSET=utf8; ")



_TABLES = {}

_TABLES[SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE +_NEW] = (
    _DDL_SVC_SEARCHSTNBYSUBWAYLINESERVICE
    .format(_make_apidata_table_name(SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE, True)) )
_TABLES[SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE +_CUR] = (
    _DDL_SVC_SEARCHSTNBYSUBWAYLINESERVICE
    .format(_make_apidata_table_name(SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE, False)) )


# TODO : Not Used Now. need Fix.
_TABLES[SB_SERVICE.SVC_SEARCHARRIVALTIMEOFLINE2SUBWAYBYIDSERVICE] = ()


# DML Tools
# ###############################################################################
_DML_INSERT_ = {}

_DML_INSERT_[SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE] = (
    " INSERT INTO `{}` "
    " (`STATION_CD`, `FR_CODE`, `STATION_NM`, `LINE_NUM`) "
    " VALUES  "
    " ( %(STATION_CD)s, %(FR_CODE)s, %(STATION_NM)s, %(LINE_NUM)s );  "
    .format(_make_apidata_table_name(SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE, True)) )







# Classes
# ###############################################################################

class DbSeoulSubway:

    _dbm = None
    _tempConn = None

    def __init__(self):
        self._dbm = DbManager()
        return

    # API 용 테이블들을 생성한다. 없을시에만 생성.
    def init_api_service_tables(self):

        conn = self._dbm.get_connection_apidata_subway()
        if conn is None:
            _log.error("Failed to init api service by connection is invalid")
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
        return True

    # Open DbConnection For batch
    def open_api_service_connection(self):
        self._tempConn = self._dbm.get_connection_apidata_subway()
        if self._tempConn is None:
            _log.error("Failed to init api service by connection is invalid")
            return False
        return True

    # Close DbConnection For batch
    def close_api_service_connection(self, with_commit=False):
        if self._tempConn is None:
            self._tempConn = None
            return
        if with_commit is True:
            self._tempConn.commit()
        self._tempConn.close()


    # Service 별로 데이타를 INSERT 한다.
    def import_api_service_data(self, svc_name, rows):

        if self._tempConn is None:
            raise DbSeoulSubwayException("Need call open_api_service_connection(), first")

        cursor = self._tempConn.cursor()

        try:
            for x in rows :
                if svc_name == SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE:
                    param = {
                      'STATION_CD': x["STATION_CD"],
                      'FR_CODE':    x["FR_CODE"],
                      'STATION_NM': x["STATION_NM"],
                      'LINE_NUM':   x["LINE_NUM"],
                    }
                    _log.debug(_DML_INSERT_[svc_name], param)
                    cursor.execute(_DML_INSERT_[svc_name], param)
                elif svc_name == SB_SERVICE.SVC_SEARCHARRIVALTIMEOFLINE2SUBWAYBYIDSERVICE:
                    # TODO :  You Have todo....this.
                    """
                    """
                else:
                    raise DbSeoulSubwayException("This Service is undefined.", svc_name)
        except mdb.Error as err:
            _log.warn("MySQL Data Insert Failed: {}, {}"
                      .format(err, DbSeoulSubway.import_api_service_data.func_code) )

        cursor.close()



# Test Class : DbSeoulSubway
#
class DbSubwaySeoulTest(unittest.TestCase):
    def test_init_api_service_tables(self):
        ds = DbSeoulSubway()
        ds.init_api_service_tables()
        return


if __name__ == "__main__":
    unittest.main()
