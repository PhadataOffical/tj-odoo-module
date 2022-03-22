import requests
from . import api

APPLET_SERVER = 'https://sczt.test.phadata.net'
APPLET_GET_CODE_URI = APPLET_SERVER + '/get/qid'
APPLET_GET_RESULT_URI = APPLET_SERVER + '/code/result'


def get_applet_code():
    resp = requests.get(url=APPLET_GET_CODE_URI)
    if resp.status_code == api.HTTP_OK:
        api_result = api.parser(resp.json())
        if api_result.code == api.SUCCESS:
            return api_result.payload


def get_scan_code_result(qrId):
    resp = requests.get(url=APPLET_GET_RESULT_URI, params={'qId': qrId})
    return resp
