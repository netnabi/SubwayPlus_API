__author__ = 'aj'

API_KEY="597569647a6e657437346555704e5a"
def M_URI(uri):
    return "/"+API_KEY+"/"+"/json/"+uri

class SbOpenApi:

    _API_HOST="openapi.seoul.go.kr:8088"
    def getApiHost(self):
        return self._API_HOST

