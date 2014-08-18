__author__ = 'aj'
# -*- coding: UTF-8 -*-

import httplib
from externapi.seoul.BasePacket import SeoulApiPacketRes

URI_N = "/"
K_DESC = "desc"
K_KEY = "key"


# Service params specification
class SB_API_PARAM:
    def __init__(self):
        return
    # 상/하행선 :  UP/IN=상행,내선 DOWN/OUT=하행/외선
    class INOUT_TAG:
        def __init__(self):
            return
        UP      = {K_DESC:"상행", K_KEY:"1"}
        DOWN    = {K_DESC:"하행", K_KEY:"2"}
        IN      = {K_DESC:"내선", K_KEY:"1"}
        OUT     = {K_DESC:"외선", K_KEY:"2"}

    class LINE_NUM:
        def __init__(self):
            return
        # 1~9: 1~9호선, I: 인천1호선, K: 경의선, B: 분당선, J: 중앙선, A: 공항철도, G: 경춘선, S:신분당선, SU:수인선
        LINE_1 = {K_DESC:"1호선",K_KEY:"1"}
        LINE_2 = {K_DESC:"2호선",K_KEY:"2"}
        LINE_3 = {K_DESC:"3호선",K_KEY:"3"}
        LINE_4 = {K_DESC:"4호선",K_KEY:"4"}
        LINE_5 = {K_DESC:"5호선",K_KEY:"5"}
        LINE_6 = {K_DESC:"6호선",K_KEY:"6"}
        LINE_7 = {K_DESC:"7호선",K_KEY:"7"}
        LINE_8 = {K_DESC:"8호선",K_KEY:"8"}
        LINE_9 = {K_DESC:"9호선",K_KEY:"9"}
        INCHEON_1 = {K_DESC:"인천1호선",K_KEY:"I"}
        GYEONGUI  = {K_DESC:"경의선",K_KEY:"K"}
        BUNDANG   = {K_DESC:"분당선",K_KEY:"B"}
        JUNGANG   = {K_DESC:"중앙선",K_KEY:"J"}
        GONGHANG  = {K_DESC:"공항철도",K_KEY:"A"}
        GYEONGCHUN = {K_DESC:"경춘선",K_KEY:"G"}
        SINBUNDANG = {K_DESC:"신분당선",K_KEY:"S"}
        SUIN       = {K_DESC:"수인선",K_KEY:"SU"}

        @staticmethod
        def get_all_line_nums():
            return [
                SB_API_PARAM.LINE_NUM.LINE_1,
                SB_API_PARAM.LINE_NUM.LINE_2,
                SB_API_PARAM.LINE_NUM.LINE_3,
                SB_API_PARAM.LINE_NUM.LINE_4,
                SB_API_PARAM.LINE_NUM.LINE_5,
                SB_API_PARAM.LINE_NUM.LINE_6,
                SB_API_PARAM.LINE_NUM.LINE_7,
                SB_API_PARAM.LINE_NUM.LINE_8,
                SB_API_PARAM.LINE_NUM.LINE_9,

                SB_API_PARAM.LINE_NUM.INCHEON_1,
                SB_API_PARAM.LINE_NUM.GYEONGUI,
                SB_API_PARAM.LINE_NUM.BUNDANG,
                SB_API_PARAM.LINE_NUM.JUNGANG,
                SB_API_PARAM.LINE_NUM.GONGHANG,
                SB_API_PARAM.LINE_NUM.GYEONGCHUN,
                SB_API_PARAM.LINE_NUM.SINBUNDANG,
                SB_API_PARAM.LINE_NUM.SUIN,
            ]


# Seoul Subway OpenAPI Service List
# descript : SVC_CODE for switch iterator
class SB_SERVICE:

    SVC_SEARCHSTNBYSUBWAYLINESERVICE                = "SearchSTNBySubwayLineService"
    SVC_SEARCHARRIVALTIMEOFLINE2SUBWAYBYIDSERVICE   = "SearchArrivalTimeOfLine2SubwayByIDService"

    # SB_SERVICE["ServiceCmd(orName)"] return SVC_CODE
    CMD = \
    {
        SVC_SEARCHSTNBYSUBWAYLINESERVICE:001,
        SVC_SEARCHARRIVALTIMEOFLINE2SUBWAYBYIDSERVICE:002,
    }
    NAME = CMD # For Aliase

    def __init__(self):
        return

# Service-Subject : 역코드로 지하철역별 열차 도착 정보 검색(역명포함)
# Service-Desc : 역코드로 지하철역별 열차 도착 정보를 검색할 수 있도록 하는 API입니다.※ 역별 지하철 시각표를 기준으로 제공하는 정보이며 실제 도착시간과 다를 수 있습니다.
class Req_SEARCH_ARRIVAL_TIME_OF_LINE2SUBWAY_BYID:
    SVC_CMD = SB_SERVICE.SVC_SEARCHARRIVALTIMEOFLINE2SUBWAYBYIDSERVICE
    SVC_CODE = SB_SERVICE.CMD[SVC_CMD]
    START_INDEX = 0; END_INDEX = 0
    STATION_CD = None
    INOUT_TAG = SB_API_PARAM.INOUT_TAG.IN[K_KEY]

    def __init__(self):
        return
    def get_service_name(self):
        return self.SVC_CMD

    # Format : /SearchArrivalTimeOfLine2SubwayByIDService/1/100/0201/1/1
    def encodeURI(self):
        return \
            self.SVC_CMD        + URI_N +\
            str(self.START_INDEX)+ URI_N +\
            str(self.END_INDEX)  + URI_N +\
            self.STATION_CD     + URI_N +\
            self.INOUT_TAG

# Service-Subject : 노선별 지하철역 검색 기능
# Service-Desc : 노선별 지하철역을 검색할 수 있도록 하는 API입니다.
class Req_SEARCH_STATION_BY_SUBWAYLINE:
    SVC_CMD = SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE
    SVC_CODE = SB_SERVICE.CMD[SVC_CMD]
    START_INDEX = 0; END_INDEX = 0
    LINE_NUM = SB_API_PARAM.LINE_NUM.LINE_1[K_KEY]

    def __init__(self):
        return
    def get_service_name(self):
        return self.SVC_CMD

    # Format : /SearchSTNBySubwayLineService/1/5/1/
    def encodeURI(self):
        return \
            self.SVC_CMD        + URI_N +\
            str(self.START_INDEX)+ URI_N +\
            str(self.END_INDEX)  + URI_N +\
            self.LINE_NUM


# Subway Service Request Maker.
class SB_API_RequestMaker:

    def __init__(self):
        return

    @staticmethod
    def get_request_byservice(svc_nm):
        if svc_nm == SB_SERVICE.SVC_SEARCHSTNBYSUBWAYLINESERVICE :
            return Req_SEARCH_STATION_BY_SUBWAYLINE()
        if svc_nm == SB_SERVICE.SVC_SEARCHARRIVALTIMEOFLINE2SUBWAYBYIDSERVICE :
            return Req_SEARCH_ARRIVAL_TIME_OF_LINE2SUBWAY_BYID()



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

        resObj = SeoulApiPacketRes()
        resObj.parse(resp, service_.get_service_name())
        conn.close()
        return resObj

