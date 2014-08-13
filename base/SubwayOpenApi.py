__author__ = 'aj'
# -*- coding: UTF-8 -*-

import httplib
from packet.BasePacket import BasePacketRes

URI_N = "/"

# Service params specification
class SB_API_PARAM:
    def __init__(self):
        return
    # 상/하행선 :  UP/IN=상행,내선 DOWN/OUT=하행/외선
    class INOUT_TAG:
        def __init__(self):
            return
        UP = "1"
        DOWN = "2"
        IN = UP
        OUT = DOWN

# Service response data parameter's key
class SB_API_DATA_KEY:
    def __init__(self):
        return
    # 요청시작/종료 위치(INDEX)
    INDEX_START    = "START_INDEX"
    INDEX_END      = "END_INDEX"
    # 전철역 코드(내부)
    STATION_CD     = "STATION_CD"


# Subway Service
class SB_API_SERVICE_CODE:

    def __init__(self):
        return

    # Service-Subject : 역코드로 지하철역별 열차 도착 정보 검색(역명포함)
    # Service-Desc : 역코드로 지하철역별 열차 도착 정보를 검색할 수 있도록 하는 API입니다.※ 역별 지하철 시각표를 기준으로 제공하는 정보이며 실제 도착시간과 다를 수 있습니다.
    class SEARCH_ARRIVAL_TIME_OF_LINE2SUBWAY_BYID:
        SVC_CODE = 000; SVC_CMD = "SearchArrivalTimeOfLine2SubwayByIDService"
        START_INDEX = 0; END_INDEX = 0
        STATION_CD = None
        INOUT_TAG = SB_API_PARAM.INOUT_TAG.IN

        def __init__(self):
            return
        # Format : /SearchArrivalTimeOfLine2SubwayByIDService/1/100/0201/1/1
        def encodeURI(self):
            return \
                self.SVC_CMD        + URI_N +\
                str(self.START_INDEX)+ URI_N +\
                str(self.END_INDEX)  + URI_N +\
                self.STATION_CD     + URI_N +\
                self.INOUT_TAG


class SbOpenApi:

    SB_API_KEY = "597569647a6e657437346555704e5a"
    # http://openapi.seoul.go.kr:8088/597569647a6e657437346555704e5a/json/SearchArrivalTimeOfLine2SubwayByIDService/1/100/0201/1/1
    @staticmethod
    def MAKE_URI(uri):
        return "/"+SbOpenApi.SB_API_KEY+"/json/"+uri

    API_HOST = "openapi.seoul.go.kr:8088"

    def __init__(self):
        return

    @staticmethod
    def getServiceData(service_):
        uri = service_.encodeURI()
        conn = httplib.HTTPConnection(SbOpenApi.API_HOST)
        conn.request("GET", SbOpenApi.MAKE_URI(uri))
        resp = conn.getresponse()
        print resp.status, resp.reason

        resObj = BasePacketRes()
        resObj.parse(resp)
        conn.close()
        return resObj

