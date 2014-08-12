__author__ = 'aj'
import httplib
from base import SubwayOpenApi

openApi = SbOpenApi()
host=openApi.getApiHost()
conn_1 = httplib.HTTPConnection(host)
conn_1.close()

#
# conn = httplib.HTTPConnection(OPEN_API_HOST)
# conn.request("GET", M_URI("SearchArrivalTimeOfLine2SubwayByIDService/1/100/0201/1/1"))
# r1 = conn.getresponse()
# print r1.status, r1.reason
# data1 = r1.read()
# print data1
# conn.request("GET", "/parrot.spam")
# r2 = conn.getresponse()
# print r2.status, r2.reason
# data2 = r2.read()
# print data2
# conn.close()