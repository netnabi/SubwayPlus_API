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

class BasePacketRes(bo.BaseObject):


    _status = ""
    _reason = ""

    # Parse result of _rawData
    _list_total_count = 0
    _result = {"code":API_RESPONSE_CODE_EMPTY, "msg":""}
    _raw_list = []

    def __init__(self):
        bo.BaseObject.__init__(self)

    def parse(self, response):
        self._status = response.status
        self._reason = response.reason
        _raw_data = response.read()
        self._parse(_raw_data)
        return

    def _parse(self, raw_data):
        self._raw_list = []
        print raw_data
        dec2=json.dumps(raw_data)
        print dec2
        # js_obj = json.loads(raw_data)
        # dec=urllib.unquote(js_obj).decode('utf8')
        # print(dec)
        return

    def getstatus(self):
        return self._status

