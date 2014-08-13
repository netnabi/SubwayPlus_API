__author__ = 'aj'
# -*- coding: UTF-8 -*-

from base.SubwayOpenApi import *


#
# openApi = SubwayOpenApi.SbOpenApi()
# host = openApi.getApiHost()
#
#
# resp_packet = BasePacket.BasePacketRes()
# resp_packet.parse()


#

service = SB_API_SERVICE_CODE.SEARCH_ARRIVAL_TIME_OF_LINE2SUBWAY_BYID()
service.START_INDEX=0
service.END_INDEX=5
service.STATION_CD="0201"
resp = SbOpenApi.getServiceData(service)