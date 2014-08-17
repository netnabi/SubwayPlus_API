__author__ = 'yjkim'
# -*- coding: UTF-8 -*-

from externapi.seoul.SubwayOpenApi import *

# Func : 해당 서비스에 대한 임포트를 요청하면, OpenAPI Call을 이용하여 DB 에 저장한다.
#
class OpenServiceDataImporter:
    def __init__(self):
        return

    REQ_DATA_SIZE = 100

    # Get Recursive Service Data And Save to Database.
    def req_service_SEARCHSTNBYSUBWAYLINESERVICE(self):

        req_loop = SB_API_RequestMaker.get_request_byservice(SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE)
        req_loop.START_INDEX = 0
        req_loop.END_INDEX = -1
        req_loop.LINE_NUM = SB_API_PARAM.LINE_NUM.LINE_1[K_KEY]

        while True :
            req_loop.START_INDEX = (req_loop.END_INDEX + 1)
            req_loop.END_INDEX = req_loop.START_INDEX + (self.REQ_DATA_SIZE-1)

            resp = SbOpenApi.getServiceData(req_loop)
            totalcnt = resp.list_total_count
            if resp.row.__len__() == 0:
                return True

            # Save to Database

            # Last phase
            if req_loop.END_INDEX+1 >= totalcnt:
                return True

