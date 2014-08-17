__author__ = 'benjamin kim'
# -*- coding: UTF-8 -*-

import urllib
import json

from base import bo

API_RESPONSE_CODE_SUC = 1
API_RESPONSE_CODE_EMPTY = 0
API_RESPONSE_CODE_FAIL = -1
API_RESPONSE_CODE_ERR = -2

API_RESPONSE_CODE = \
    {
        "NOT-DEFINE": API_RESPONSE_CODE_EMPTY,
        "INFO-000"  : API_RESPONSE_CODE_SUC,  # 정상 처리되었습니다
        "INFO-100"  : API_RESPONSE_CODE_FAIL, # 인증키가 유효하지 않습니다.
        "INFO-200"  : API_RESPONSE_CODE_FAIL, # 해당하는 데이터가 없습니다.

        "ERROR-300" : API_RESPONSE_CODE_ERR,
        "ERROR-301" : API_RESPONSE_CODE_ERR,
        "ERROR-310" : API_RESPONSE_CODE_ERR,
        "ERROR-331" : API_RESPONSE_CODE_ERR,
        "ERROR-332" : API_RESPONSE_CODE_ERR,
        "ERROR-333" : API_RESPONSE_CODE_ERR,
        "ERROR-334" : API_RESPONSE_CODE_ERR,
        "ERROR-335" : API_RESPONSE_CODE_ERR,
        "ERROR-336" : API_RESPONSE_CODE_ERR,

        "ERROR-500" : API_RESPONSE_CODE_ERR,
        "ERROR-600" : API_RESPONSE_CODE_ERR,
        "ERROR-601" : API_RESPONSE_CODE_ERR,
    }


# Service response data parameter's key
class _DATA_KEY:
    def __init__(self):
        return
    # 결과 총 카운트
    LIST_TOTAL_COUNT = "list_total_count"
    API_RESULT = "RESULT"
    API_RESULT_CODE = "CODE"
    API_RESULT_MSG = "MESSAGE"
    API_RESULT_ROW = "row"


class SeoulApiPacketRes(bo.BaseObject):

    status = ""
    reason = ""

    # Parse result of _rawData
    svc_name = ""
    list_total_count = 0
    result_code = API_RESPONSE_CODE_EMPTY
    result_code_raw = ""
    result_msg  = ""
    row    = []

    def __init__(self):
        bo.BaseObject.__init__(self)

    def parse(self, response, svc_name):
        self.status = response.status
        self.reason = response.reason
        self.svc_name = svc_name
        _raw_data = response.read()
        self._parse(_raw_data)
        return

    """
    # Example Parsing Format.
    {
    "SearchSTNBySubwayLineService": {
        "list_total_count": 101,
        "RESULT": {
            "CODE": "INFO-000",
            "MESSAGE": "정상 처리되었습니다"
        },
        "row": [{
            "STATION_CD": "1916",
            "STATION_NM": "소요산",
            "LINE_NUM": "1",
            "FR_CODE": "100"
        }, {
            "STATION_CD": "1915",
            "STATION_NM": "동두천",
            "LINE_NUM": "1",
            "FR_CODE": "101"
        }]
    }
    }
    """
    def _parse(self, raw_data):
        js_obj = json.loads(raw_data)
        svc_dt = js_obj[self.svc_name]
        result_dt = svc_dt[_DATA_KEY.API_RESULT]

        self.list_total_count   = svc_dt[_DATA_KEY.LIST_TOTAL_COUNT]
        self.result_code_raw    = result_dt[_DATA_KEY.API_RESULT_CODE]
        self.result_code        = API_RESPONSE_CODE[self.result_code_raw]
        self.result_msg         = result_dt[_DATA_KEY.API_RESULT_MSG]
        self.row                = svc_dt[_DATA_KEY.API_RESULT_ROW]

        return