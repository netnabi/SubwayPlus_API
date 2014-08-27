__author__ = 'yjkim'
# -*- coding: UTF-8 -*-

from base import logger, baseutil
import pymysql as mdb
from base.bo import BoException
import unittest
from base.dbmysql import DbManager
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

_DDL_SVC_SEARCHSTNTIMETABLEBYIDSERVICE = (
    " CREATE TABLE `{}` (  "
    "   `LINE_NUM` char(2) DEFAULT NULL COMMENT 'Line Number of Subway',  "
    "   `FR_CODE` char(6) DEFAULT NULL COMMENT 'USC for Foreign (Alias)',  "
    "   `STATION_CD` char(6) NOT NULL DEFAULT '0' COMMENT 'Unique Station Code',  "
    "   `STATION_NM` char(60) DEFAULT NULL COMMENT 'Subway Station Name',  "

    "   `TRAIN_NO` char(10) DEFAULT NULL COMMENT 'Train No',  "
    "   `ARRIVETIME` char(8) DEFAULT NULL COMMENT 'Train ArriveTime',  "
    "   `LEFTTIME` char(8) DEFAULT NULL COMMENT 'Train LeaveTime from Station',  "
    "   `ORIGINSTATION` char(6) DEFAULT NULL COMMENT 'Train Origin Station Code',  "
    "   `DESTSTATION` char(6) DEFAULT NULL COMMENT 'Train Dest Station Code',  "

    "   `SUBWAYSNAME` char(60) DEFAULT NULL COMMENT 'Subway Origin Station Name',  "
    "   `SUBWAYENAME` char(60) DEFAULT NULL COMMENT 'Subway Dest Station Name',  "

    "   `WEEK_TAG` char(2) DEFAULT NULL COMMENT 'Weeks Codes',  "
    "   `INOUT_TAG` char(2) DEFAULT NULL COMMENT 'Arrow INOUT',  "
    "   `FL_FLAG` char(2) DEFAULT NULL COMMENT 'FLAG',  "
    "   `DESTSTATION2` char(2) DEFAULT NULL COMMENT 'Dest Station Code 2',  "
    "   `EXPRESS_YN` char(2) DEFAULT NULL COMMENT 'Rapid or not',  "
    "   `BRANCH_LINE` char(20) DEFAULT NULL COMMENT 'Branch Line'  "

    " ) ENGINE=InnoDB DEFAULT CHARSET=utf8; ")




_TABLES = {}

# ## _DDL_SVC_SEARCHSTNBYSUBWAYLINESERVICE
_TABLES[SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE +_NEW] = (
    _DDL_SVC_SEARCHSTNBYSUBWAYLINESERVICE
    .format(_make_apidata_table_name(SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE, True)) )
_TABLES[SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE +_CUR] = (
    _DDL_SVC_SEARCHSTNBYSUBWAYLINESERVICE
    .format(_make_apidata_table_name(SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE, False)) )

# ## _DDL_SVC_SEARCHSTNTIMETABLEBYIDSERVICE
_TABLES[SB_SERVICE.SVC_SEARCHSTNTIMETABLEBYIDSERVICE +_NEW] = (
    _DDL_SVC_SEARCHSTNTIMETABLEBYIDSERVICE
    .format(_make_apidata_table_name(SB_SERVICE.SVC_SEARCHSTNTIMETABLEBYIDSERVICE, True)) )
_TABLES[SB_SERVICE.SVC_SEARCHSTNTIMETABLEBYIDSERVICE +_CUR] = (
    _DDL_SVC_SEARCHSTNTIMETABLEBYIDSERVICE
    .format(_make_apidata_table_name(SB_SERVICE.SVC_SEARCHSTNTIMETABLEBYIDSERVICE, False)) )


# TODO : Not Used Now. need Fix.
# _TABLES[SB_SERVICE.SVC_SEARCHARRIVALTIMEOFLINE2SUBWAYBYIDSERVICE] = ()


# DML Tools
# ###############################################################################
_DML_INSERT_ = {}

_DML_INSERT_[SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE] = (
    " INSERT INTO `{}` "
    " (`STATION_CD`, `FR_CODE`, `STATION_NM`, `LINE_NUM`) "
    " VALUES  "
    " ( %(STATION_CD)s, %(FR_CODE)s, %(STATION_NM)s, %(LINE_NUM)s );  "
    .format(_make_apidata_table_name(SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE, True)) )

_DML_INSERT_[SB_SERVICE.SVC_SEARCHSTNTIMETABLEBYIDSERVICE] = (
    " INSERT INTO `{}` "
    " (`LINE_NUM`,`FR_CODE`,`STATION_CD`,`STATION_NM`,`TRAIN_NO`,`ARRIVETIME`,`LEFTTIME`,`ORIGINSTATION`,`DESTSTATION`,`SUBWAYSNAME`,`SUBWAYENAME`,`WEEK_TAG`,`INOUT_TAG`,`FL_FLAG`,`DESTSTATION2`,`EXPRESS_YN`,`BRANCH_LINE`) "
    " VALUES  "
    " ( %(LINE_NUM)s,%(FR_CODE)s,%(STATION_CD)s,%(STATION_NM)s,%(TRAIN_NO)s,%(ARRIVETIME)s,%(LEFTTIME)s,%(ORIGINSTATION)s,%(DESTSTATION)s,%(SUBWAYSNAME)s,%(SUBWAYENAME)s,%(WEEK_TAG)s,%(INOUT_TAG)s,%(FL_FLAG)s,%(DESTSTATION2)s,%(EXPRESS_YN)s,%(BRANCH_LINE)s );  "
    .format(_make_apidata_table_name(SB_SERVICE.SVC_SEARCHSTNTIMETABLEBYIDSERVICE, True)) )






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
                      'STATION_CD': x["STATION_CD"],            # 전철역코드
                      'FR_CODE':    x["FR_CODE"],               # 외부코드
                      'STATION_NM': x["STATION_NM"],            # 전철역명
                      'LINE_NUM':   x["LINE_NUM"],              # 호선
                    }
                    _log.debug(_DML_INSERT_[svc_name], param)
                    cursor.execute(_DML_INSERT_[svc_name], param)
                elif svc_name == SB_SERVICE.SVC_SEARCHARRIVALTIMEOFLINE2SUBWAYBYIDSERVICE:
                    # TODO :  You Have todo....this.
                    """
                    """
                elif svc_name == SB_SERVICE.SVC_SEARCHSTNTIMETABLEBYIDSERVICE:
                    param = {
                      'LINE_NUM'    : x["LINE_NUM"],            # 호선
                      'FR_CODE'     : x["FR_CODE"],             # 외부코드
                      'STATION_CD'  : x["STATION_CD"],          # 전철역코드
                      'STATION_NM'  : x["STATION_NM"],          # 전철역명
                      'TRAIN_NO'    : x["TRAIN_NO"],            # 열차번호

                      'ARRIVETIME'      : x["ARRIVETIME"],      # 도착시간
                      'LEFTTIME'        : x["LEFTTIME"],        # 출발시간
                      'ORIGINSTATION'   : x["ORIGINSTATION"],   # 출발지하철역코드
                      'DESTSTATION'     : x["DESTSTATION"],     # 도착지하철역코드

                      'SUBWAYSNAME'     : x["SUBWAYSNAME"],     # 출발지하철역명
                      'SUBWAYENAME'     : x["SUBWAYENAME"],     # 도착지하철역명

                      'WEEK_TAG'        : x["WEEK_TAG"],        # 요일
                      'INOUT_TAG'       : x["INOUT_TAG"],       # 상/하행선
                      'FL_FLAG'         : x["FL_FLAG"],         # 플러그
                      'DESTSTATION2'    : x["DESTSTATION2"],    # 도착역 코드2
                      'EXPRESS_YN'      : x["EXPRESS_YN"],      # 급행선
                      'BRANCH_LINE'     : x["BRANCH_LINE"],     # 지선
                    }
                    _log.debug(_DML_INSERT_[svc_name], param)
                    cursor.execute(_DML_INSERT_[svc_name], param)
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
