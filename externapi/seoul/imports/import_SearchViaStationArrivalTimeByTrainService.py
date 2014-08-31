__author__ = 'aj'
# -*- coding: UTF-8 -*-

from externapi.seoul.imports.import_base import *
from externapi.seoul.SubwayOpenApi import *
from externapi.seoul.DbSubwaySeoul import DbSeoulSubway
import unittest
from base import logger

_log = logger.get_logger("IMPORTER-SEOUL")

# 모든 지하철역 코드와 WEEK, INOUT 을 조합하여 REST 요청하고, 해당결과를 DB 에 저장한다.
def importStart():

    dss = DbSeoulSubway()
    if dss.open_api_service_connection() is False:
        raise OpenServiceDataImporterException("Can't not Open Database Connection")

    svc_nm = SB_SERVICE.SVC_SEARCHVIASTNARRIVALTIMEBYTRAINSERVICE
    dss.tables_truncate(svc_nm)

    trains      = dss.get_all_train_no()
    inouts      = SB_API_PARAM.INOUT_TAG.list()
    weeks       = SB_API_PARAM.WEEK_TAG.list()


    for train in trains:
        for inout in inouts:
            for week in weeks:
                sub_result = _importSpecific(dss, svc_nm, train, week, inout)
                if sub_result is False:
                    raise OpenServiceDataImporterException("SVC_SEARCHVIASTNARRIVALTIMEBYTRAINSERVICE ImportFailed...")

    dss.close_api_service_connection(True)
    return True

def _importSpecific(dss, svc_nm, TRAIN_NO_, WEEK_, INOUT_):

    req_loop = SB_API_RequestMaker.get_request_byservice(svc_nm)
    req_loop.START_INDEX = 0
    req_loop.END_INDEX = -1
    req_loop.TRAIN_NO   = TRAIN_NO_
    req_loop.INOUT_TAG  = INOUT_[K_KEY]
    req_loop.WEEK_TAG   = WEEK_[K_KEY]

    _log.debug("IMPORT-(%s):TRAIN_NO(%s),INOUT(%s), WEEK(%s)", svc_nm, TRAIN_NO_, INOUT_, WEEK_)
    _Save2Db(svc_nm, req_loop, dss, TRAIN_NO_)
    return True


def _Save2Db(svc_nm, req_loop, dss, TRAIN_NO_):
    _REQ_DATA_SIZE = 1000
    while True :
        req_loop.START_INDEX = (req_loop.END_INDEX + 1)
        req_loop.END_INDEX = req_loop.START_INDEX + (_REQ_DATA_SIZE-1)

        resp = SbOpenApi.getServiceData(req_loop)
        totalcnt = resp.list_total_count
        if resp.row.__len__() == 0:
            return

        # Insert Parameter into result.
        rows = resp.row
        for row in rows:
            row["TRAIN_NO"]=TRAIN_NO_

        # Save to Database
        dss.import_api_service_data(svc_nm, rows)

        # Last phase
        if req_loop.END_INDEX+1 >= totalcnt:
            return



if __name__ == "__main__":
    unittest.main()