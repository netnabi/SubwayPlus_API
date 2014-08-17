__author__ = 'aj'
# -*- coding: UTF-8 -*-

from externapi.seoul.SubwayOpen2db import OpenServiceDataImporter

#
# openApi = SubwayOpenApi.SbOpenApi()
# host = openApi.getApiHost()
#
#
# resp_packet = BasePacket.BasePacketRes()
# resp_packet.parse()


#

# service = SB_API_RequestMaker.SEARCH_STATION_BY_SUBWAYLINE()
# service.START_INDEX=0
# service.END_INDEX=5
# service.LINE_NUM = SB_API_PARAM.LINE_NUM.LINE_1[K_KEY]
# resp = SbOpenApi.getServiceData(service)

importer = OpenServiceDataImporter()
importer.req_service_SEARCHSTNBYSUBWAYLINESERVICE()

