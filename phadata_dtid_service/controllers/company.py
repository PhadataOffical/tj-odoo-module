
import requests

COMPANY_SERVICE_URL = 'https://sczt.test.phadata.net'
GET_QR_CODE_API = COMPANY_SERVICE_URL + '/company/get/code'
SCAN_CODE_RESULT_API = COMPANY_SERVICE_URL + '/company/getScanResult'


def get_qr_code():
    resp = requests.get(url=GET_QR_CODE_API)
    return resp


def scan_code_result(qrId):
    resp = requests.get(url=SCAN_CODE_RESULT_API, params={'qrId': qrId})
    return resp

def get_license_b64(imageurl) -> str:
    resp = requests.get(url=imageurl)
    result = resp.json()
    message_header = result['message_header']
    errorCode = message_header['errorCode']
    if errorCode == '0':
        message_content = result['message_content']
        licencePDF = message_content['licencePDF']
        return licencePDF
