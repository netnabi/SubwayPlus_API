__author__ = 'aj'
# -*- coding: UTF-8 -*-

from externapi.seoul.imports.import_base import *
from externapi.seoul.SubwayOpenApi import *
from externapi.seoul.DbSubwaySeoul import DbSeoulSubway
import unittest

# 모든 라인의 지하철역 목록을 REST 요청하고, 해당결과를 DB 에 저장한다.
def importStart():

    dss = DbSeoulSubway()
    if dss.open_api_service_connection() is False:
        raise OpenServiceDataImporterException("Can't not Open Database Connection")

    svc_nm = SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE

    lines = SB_API_PARAM.LINE_NUM.list()
    for line in lines:
        req_loop = SB_API_RequestMaker.get_request_byservice(svc_nm)
        req_loop.START_INDEX = 0
        req_loop.END_INDEX = -1
        req_loop.LINE_NUM = line[K_KEY]

        _Save2Db(svc_nm, req_loop, dss)

    dss.close_api_service_connection(True)
    return True

# 지하철라인별로 REST 서비스를 요청한다.
def _Save2Db(svc_nm, req_loop, dss):
    _REQ_DATA_SIZE = 100
    while True :
        req_loop.START_INDEX = (req_loop.END_INDEX + 1)
        req_loop.END_INDEX = req_loop.START_INDEX + (_REQ_DATA_SIZE-1)

        resp = SbOpenApi.getServiceData(req_loop)
        totalcnt = resp.list_total_count
        if resp.row.__len__() == 0:
            return

        # Save to Database
        dss.import_api_service_data(svc_nm, resp.row)

        # Last phase
        if req_loop.END_INDEX+1 >= totalcnt:
            return

if __name__ == "__main__":
    unittest.main()