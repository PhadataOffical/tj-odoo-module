import json
import requests

# API_BASE_URL = "https://ca-server.dev.tdaas.phadata.net/"
API_BASE_URL = "https://ca.tdaas.dev.phadata.net/"


def sealSignature(x: int, y: int, w: int, h: int, pdfUrl: str, identNo: str, uniqueCode: str, serialnumber: str, callBackUrl: str):
    datas = {
        'sealType': "coordinate",
        'data': {
            'pdfUrl': pdfUrl,
            'identNo':  identNo,
            'uniqueCode':  uniqueCode,
            'serialnumber': serialnumber,
            'sealType': 'coordinate',

            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'page': 0,

            'isImg': 'false',
            'userType': 0,

            'notifyUrl': API_BASE_URL + 'api/v1/seal/sign/receive',
            'callBackUrl': callBackUrl
        }
    }
    print('=================================================================')
    print(API_BASE_URL + "api/v1/seal/signature")
    print('=================================================================')
    print(datas)
    datas = json.dumps(datas).encode(encoding='utf-8')
    headers = {"Content-Type": "application/json"}
    result = requests.post(API_BASE_URL + "api/v1/seal/signature", data=datas, headers=headers)
    result = json.loads(result.content)
    return result

def getSealSignResult(resultId: str):
    print('=================================================================')
    print(API_BASE_URL + "api/v1/seal/getSealSignResult?resultId=" + resultId)
    print('=================================================================')
    result = requests.get(API_BASE_URL + "api/v1/seal/getSealSignResult?resultId=" + resultId)
    result = json.loads(result.content)
    return result
