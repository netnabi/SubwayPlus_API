__author__ = 'yjkim'
# -*- coding: UTF-8 -*-

from base.bo import BoException
import unittest
from externapi.seoul.SubwayOpenApi import *
from externapi.seoul.DbSubwaySeoul import DbSeoulSubway


class OpenServiceDataImporterException(BoException):
    """
    """


# Class : 해당 서비스에 대한 임포트를 요청하면, OpenAPI Call을 이용하여 DB 에 저장한다.
#
class OpenServiceDataImporter:
    def __init__(self):
        return

    REQ_DATA_SIZE = 100

    # 모든 라인의 지하철역 목록을 REST 요청하고, 해당결과를 DB 에 저장한다.
    def req_service_SEARCHSTNBYSUBWAYLINESERVICE(self):

        dss = DbSeoulSubway()
        if dss.open_api_service_connection() is False:
            raise OpenServiceDataImporterException("Can't not Open Database Connection")

        svc_nm = SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE

        lines = SB_API_PARAM.LINE_NUM.get_all_line_nums()
        for line in lines:
            req_loop = SB_API_RequestMaker.get_request_byservice(svc_nm)
            req_loop.START_INDEX = 0
            req_loop.END_INDEX = -1
            req_loop.LINE_NUM = line[K_KEY]

            self._req_service_SEARCHSTNBYSUBWAYLINESERVICE_line(svc_nm, req_loop, dss)

        dss.close_api_service_connection(True)
        return True

    # 지하철라인별로 REST 서비스를 요청한다.
    def _req_service_SEARCHSTNBYSUBWAYLINESERVICE_line(self, svc_nm, req_loop, dss):
        while True :
            req_loop.START_INDEX = (req_loop.END_INDEX + 1)
            req_loop.END_INDEX = req_loop.START_INDEX + (self.REQ_DATA_SIZE-1)

            resp = SbOpenApi.getServiceData(req_loop)
            totalcnt = resp.list_total_count
            if resp.row.__len__() == 0:
                return

            # Save to Database
            dss.import_api_service_data(svc_nm, resp.row)

            # Last phase
            if req_loop.END_INDEX+1 >= totalcnt:
                return


# Test Class : OpenServiceDataImporter 를 테스트한다.
#
class OpenServiceDataImporterTest(unittest.TestCase):

    def test_req_service_SEARCHSTNBYSUBWAYLINESERVICE(self):
        imp = OpenServiceDataImporter()
        result = imp.req_service_SEARCHSTNBYSUBWAYLINESERVICE()
        self.assertEqual(result, True)


if __name__ == "__main__":
    unittest.main()
