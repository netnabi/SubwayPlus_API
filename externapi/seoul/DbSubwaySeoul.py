__author__ = 'yjkim'
# -*- coding: UTF-8 -*-

import unittest
from base.dbmysql import DbManager
from externapi.seoul.SubwayOpenApi import *

class DbSeoulSubway:

    def __init__(self):
        return

    @staticmethod
    def make_apidata_table_name(svc_nm):
        return "API_DATA_"+svc_nm;

    def init_api_service_table(self, svc_nm):
        if svc_nm == SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE :
            conn = DbManager().get_connection_apidata_subway()
            conn.close()
        return



# Test Class : OpenServiceDataImporter 를 테스트한다.
#
class DbSubwaySeoulTest(unittest.TestCase):
    def test(self):
        return

    def test2(self, a, b):
        return a+b


if __name__ == "__main__":
    unittest.main()
