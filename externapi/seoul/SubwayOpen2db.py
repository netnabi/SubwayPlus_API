__author__ = 'yjkim'
# -*- coding: UTF-8 -*-


import unittest
from imports import import_SeachStationBySubwayLineService
from imports import import_SearchStationTimeTableByIdService


# Class : 해당 서비스에 대한 임포트를 요청하면, OpenAPI Call을 이용하여 DB 에 저장한다.
#
class OpenServiceDataImporter:
    def __init__(self):
        return

    def searchStationBySubwayLineService(self):
        return import_SeachStationBySubwayLineService.importStart()
    def searchStationTimeTableByIdService(self):
        return import_SearchStationTimeTableByIdService.importStart()


# Test Class : OpenServiceDataImporter 를 테스트한다.
#
class OpenServiceDataImporterTest(unittest.TestCase):

    def test_req_service_searchStationTimeTableByIdService(self):
        imp = OpenServiceDataImporter()
        result = imp.searchStationTimeTableByIdService()
        self.assertEqual(result, True)

    @unittest.skip("testing skipping")
    def test_req_service_searchStationBySubwayLineService(self):
        imp = OpenServiceDataImporter()
        result = imp.searchStationBySubwayLineService()
        self.assertEqual(result, True)



if __name__ == "__main__":
    unittest.main()
